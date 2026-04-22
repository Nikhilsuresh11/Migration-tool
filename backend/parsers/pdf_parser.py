import fitz  # PyMuPDF

from utils.helpers import clean_text


def parse_pdf(filepath: str) -> dict:

    try:
        doc = fitz.open(filepath)
    except Exception as e:
        raise ValueError(f"Failed to open PDF file: {str(e)}")

    if doc.page_count == 0:
        doc.close()
        raise ValueError("The PDF document has no pages.")

    pages = extract_pages(doc)
    full_text = build_full_text(pages)
    headings = extract_headings(doc)
    paragraphs = extract_paragraphs(full_text)
    images_count = count_images(doc)
    tables = extract_tables_pdf(doc)
    metadata = extract_metadata(doc)
    total_pages = doc.page_count

    doc.close()

    return {
        "file_type": "pdf",
        "full_text": full_text,
        "headings": headings,
        "paragraphs": paragraphs,
        "pages": pages,
        "total_pages": total_pages,
        "images_count": images_count,
        "tables": tables,
        "metadata": metadata,
    }


def extract_pages(doc: fitz.Document) -> list:

    pages = []
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text = clean_text(page.get_text("text"))
        pages.append({
            "page_number": page_num + 1,
            "text": text,
            "word_count": len(text.split()) if text else 0,
        })
    return pages


def build_full_text(pages: list) -> str:
    all_text = [page["text"] for page in pages if page["text"]]
    return "\n\n".join(all_text)


def extract_headings(doc: fitz.Document) -> list:
    toc = doc.get_toc()

    if toc:
        return _headings_from_toc(toc)

    return _headings_from_font_analysis(doc)


def _headings_from_toc(toc: list) -> list:
    headings = []
    for entry in toc:
        level = entry[0]
        title = entry[1].strip()
        if title:
            headings.append({"text": title, "level": level})
    return headings


def _headings_from_font_analysis(doc: fitz.Document) -> list:

    headings = []
    font_sizes = []

    max_pages = min(doc.page_count, 10)

    for page_num in range(max_pages):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)["blocks"]
        for block in blocks:
            if block.get("type") == 0:  # Text block
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        font_sizes.append(span.get("size", 12))

    if not font_sizes:
        return headings

    sorted_sizes = sorted(font_sizes)
    median_size = sorted_sizes[len(sorted_sizes) // 2]
    heading_threshold = median_size * 1.2

    for page_num in range(max_pages):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)["blocks"]
        for block in blocks:
            if block.get("type") == 0:
                for line in block.get("lines", []):
                    line_text = ""
                    max_font = 0
                    for span in line.get("spans", []):
                        line_text += span.get("text", "")
                        max_font = max(max_font, span.get("size", 12))

                    line_text = line_text.strip()
                    if line_text and max_font >= heading_threshold:
                        level = _font_size_to_level(max_font, median_size)
                        headings.append({"text": line_text, "level": level})

    return headings


def _font_size_to_level(font_size: float, median_size: float) -> int:
    ratio = font_size / median_size
    if ratio >= 2.0:
        return 1
    elif ratio >= 1.6:
        return 2
    elif ratio >= 1.3:
        return 3
    return 4


def extract_paragraphs(full_text: str) -> list:

    if not full_text:
        return []

    raw_paragraphs = full_text.split("\n\n")
    paragraphs = []

    for para in raw_paragraphs:
        cleaned = clean_text(para)
        if cleaned and len(cleaned.split()) >= 3:  # Skip very short fragments
            paragraphs.append(cleaned)

    return paragraphs


def extract_tables_pdf(doc: fitz.Document) -> list:

    tables = []
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        try:
            tabs = page.find_tables()
            for table in tabs.tables:
                extracted = table.extract()
                if extracted:
                    tables.append(extracted)
        except AttributeError:
            pass  # find_tables not in this fitz version
    return tables


def count_images(doc: fitz.Document) -> int:
    total = 0
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        total += len(page.get_images(full=True))
    return total


def extract_metadata(doc: fitz.Document) -> dict:
    meta = doc.metadata or {}
    return {
        "author": meta.get("author", ""),
        "title": meta.get("title", ""),
        "subject": meta.get("subject", ""),
        "creator": meta.get("creator", ""),
        "producer": meta.get("producer", ""),
        "created": meta.get("creationDate", ""),
        "modified": meta.get("modDate", ""),
    }
