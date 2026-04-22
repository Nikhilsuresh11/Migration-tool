"""
Link analysis module.

Extracts hyperlinks from DOCX and PDF documents, classifies them
as internal or external, checks for broken links concurrently,
and detects cross-document references via regex patterns.
"""

import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from docx import Document
import fitz


def analyze_links(filepath, file_type, full_text, warnings=None):
    """
    Extract and analyze all hyperlinks from a document.

    Args:
        filepath: Path to the document file.
        file_type: 'docx' or 'pdf'.
        full_text: Full extracted text of the document.
        warnings: Shared list to append warning messages to.

    Returns:
        Dictionary with internal_links, external_links,
        broken_links, and cross_document_references counts.
    """
    if warnings is None:
        warnings = []

    try:
        urls = _extract_urls(filepath, file_type)

        internal = [u for u in urls if _classify_link(u) == "internal"]
        external = [u for u in urls if _classify_link(u) == "external"]

        broken = _count_broken_links(external)
        cross_refs = _count_cross_references(full_text)

        return {
            "internal_links": len(internal),
            "external_links": len(external),
            "broken_links": broken,
            "cross_document_references": cross_refs,
        }
    except Exception as e:
        warnings.append(f"Link analysis failed: {str(e)}")
        return get_default()


def _extract_urls(filepath, file_type):
    """Route URL extraction to the appropriate parser."""
    if file_type == "docx":
        return _extract_links_docx(filepath)
    elif file_type == "pdf":
        return _extract_links_pdf(filepath)
    return []


def _extract_links_docx(filepath):
    """Extract all hyperlink URLs from a DOCX file."""
    doc = Document(filepath)
    urls = []

    WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

    for para in doc.paragraphs:
        for hyperlink in para._element.findall(f"{{{WORD_NS}}}hyperlink"):
            r_id = hyperlink.get(f"{{{REL_NS}}}id")
            if r_id:
                rel = doc.part.rels.get(r_id)
                if rel and rel.is_external:
                    urls.append(rel.target_ref)
            else:
                anchor = hyperlink.get(f"{{{WORD_NS}}}anchor")
                if anchor:
                    urls.append(f"#{anchor}")

    return urls


def _extract_links_pdf(filepath):
    """Extract all hyperlink URLs from a PDF file."""
    doc = fitz.open(filepath)
    urls = []

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        links = page.get_links()
        for link in links:
            uri = link.get("uri")
            if uri:
                urls.append(uri)

    doc.close()
    return urls


def _classify_link(url):
    """
    Classify a URL as internal or external.

    Internal: relative paths, fragment links (#), bookmarks.
    External: absolute URLs with http/https/ftp/mailto schemes.
    """
    if not url:
        return "internal"

    url_lower = url.strip().lower()

    if url_lower.startswith("#"):
        return "internal"

    if url_lower.startswith(("http://", "https://", "ftp://", "mailto:")):
        return "external"

    return "internal"


def _count_broken_links(urls, timeout=3, max_workers=10):
    """
    Check external URLs for broken links using concurrent HEAD requests.

    Only counts links that return non-200 HTTP status.
    Links that are unreachable (timeout/network error) are skipped.
    """
    if not urls:
        return 0

    # Deduplicate URLs before checking
    unique_urls = list(set(urls))
    broken = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(_check_single_url, url, timeout): url
            for url in unique_urls
        }
        for future in as_completed(futures):
            result = future.result()
            if result is False:  # Explicitly non-200 (not None/unreachable)
                broken += 1

    return broken


def _check_single_url(url, timeout=3):
    """
    Check if a single URL is reachable with a HEAD request.

    Returns:
        True: URL returned 200.
        False: URL returned non-200.
        None: URL is unreachable (timeout, DNS failure, etc.) — skipped.
    """
    try:
        req = Request(url, method="HEAD")
        req.add_header("User-Agent", "DocumentAnalyzer/1.0")
        response = urlopen(req, timeout=timeout)
        return response.status == 200
    except HTTPError:
        return False
    except (URLError, OSError, Exception):
        return None


def _count_cross_references(text):
    """
    Count cross-document references using regex patterns.

    Detects phrases like 'see page 5', 'refer to section 3',
    'as described in chapter 2', etc.
    """
    if not text:
        return 0

    patterns = [
        r"\bsee\s+(page|section|chapter|appendix|figure|table)\s+[\w\d]+",
        r"\brefer\s+to\s+(page|section|chapter|appendix|figure|table)\s+[\w\d]+",
        r"\bas\s+described\s+in\s+(page|section|chapter|appendix|figure|table)\s+[\w\d]+",
        r"\bmentioned\s+in\s+(page|section|chapter|appendix|figure|table)\s+[\w\d]+",
        r"\bsee\s+above\b",
        r"\bsee\s+below\b",
        r"\bcross[\s-]?reference",
        r"\bpage\s+\d+\b",
    ]

    total = 0
    text_lower = text.lower()
    for pattern in patterns:
        matches = re.findall(pattern, text_lower)
        total += len(matches)

    return total


def get_default():
    """Return the default empty structure for link analysis."""
    return {
        "internal_links": 0,
        "external_links": 0,
        "broken_links": 0,
        "cross_document_references": 0,
    }
