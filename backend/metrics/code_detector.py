"""
Code block detection module.

Detects code blocks and inline code instances in DOCX and PDF
documents by analyzing paragraph styles, font families, and
PyMuPDF font metadata. Uses Pygments for code language detection.
"""

from docx import Document
import fitz

try:
    from pygments.lexers import guess_lexer, ClassNotFound
    PYGMENTS_AVAILABLE = True
except ImportError:
    PYGMENTS_AVAILABLE = False


# Fonts commonly used for code/monospace content
MONOSPACE_FONTS = {
    "courier", "courier new", "consolas", "lucida console",
    "monaco", "menlo", "source code pro", "fira code",
    "jetbrains mono", "dejavu sans mono", "liberation mono",
    "cascadia code", "cascadia mono", "inconsolata",
    "ubuntu mono", "droid sans mono", "roboto mono",
}

# DOCX style names that indicate code content
CODE_STYLE_KEYWORDS = {"code", "listing", "source", "preformatted", "verbatim"}


def detect_code(filepath, file_type, full_text, warnings=None):
    """
    Detect code blocks and inline code in a document.

    Args:
        filepath: Path to the document file.
        file_type: 'docx' or 'pdf'.
        full_text: Full extracted text (for language detection).
        warnings: Shared list to append warning messages to.

    Returns:
        Dictionary with code_blocks_count, languages_detected,
        and inline_code_instances.
    """
    if warnings is None:
        warnings = []

    try:
        if file_type == "docx":
            result = _detect_docx_code(filepath)
        elif file_type == "pdf":
            result = _detect_pdf_code(filepath)
        else:
            return get_default()

        # Try to detect programming languages from code blocks
        if result.get("_code_texts"):
            languages = _detect_code_languages(result.pop("_code_texts"))
            result["languages_detected"] = languages

        return result
    except Exception as e:
        warnings.append(f"Code detection failed: {str(e)}")
        return get_default()


def _detect_docx_code(filepath):
    """Detect code blocks and inline code in a DOCX file."""
    doc = Document(filepath)

    code_blocks = 0
    inline_code = 0
    code_texts = []

    for para in doc.paragraphs:
        style_name = (para.style.name or "").lower()
        is_code_style = any(kw in style_name for kw in CODE_STYLE_KEYWORDS)

        if is_code_style:
            code_blocks += 1
            if para.text.strip():
                code_texts.append(para.text.strip())
            continue

        # Check individual runs for monospace fonts (inline code)
        para_has_code_run = False
        for run in para.runs:
            font_name = (run.font.name or "").lower()
            if _is_monospace_font(font_name):
                if not para_has_code_run:
                    # Check if the entire paragraph is monospace
                    all_mono = _is_entire_paragraph_monospace(para)
                    if all_mono:
                        code_blocks += 1
                        if para.text.strip():
                            code_texts.append(para.text.strip())
                        break
                    else:
                        inline_code += 1
                        para_has_code_run = True

    return {
        "code_blocks_count": code_blocks,
        "languages_detected": [],
        "inline_code_instances": inline_code,
        "_code_texts": code_texts,
    }


def _detect_pdf_code(filepath):
    """Detect code blocks and inline code in a PDF file."""
    doc = fitz.open(filepath)

    code_blocks = 0
    inline_code = 0
    code_texts = []

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE).get("blocks", [])

        for block in blocks:
            if block.get("type") != 0:  # Only text blocks
                continue

            block_is_code = _is_pdf_block_code(block)

            if block_is_code:
                code_blocks += 1
                block_text = _extract_block_text(block)
                if block_text:
                    code_texts.append(block_text)
            else:
                # Check for inline code spans
                inline_code += _count_inline_code_spans(block)

    doc.close()

    return {
        "code_blocks_count": code_blocks,
        "languages_detected": [],
        "inline_code_instances": inline_code,
        "_code_texts": code_texts,
    }


def _is_pdf_block_code(block):
    """
    Determine if an entire PDF text block is code based on font analysis.

    A block is likely code if the majority of its text uses monospace fonts.
    """
    total_chars = 0
    mono_chars = 0

    for line in block.get("lines", []):
        for span in line.get("spans", []):
            text = span.get("text", "")
            font_name = span.get("font", "").lower()
            char_count = len(text)
            total_chars += char_count

            if _is_monospace_font(font_name):
                mono_chars += char_count

    if total_chars == 0:
        return False

    return (mono_chars / total_chars) >= 0.7


def _count_inline_code_spans(block):
    """Count individual monospace spans in a non-code block."""
    count = 0
    for line in block.get("lines", []):
        for span in line.get("spans", []):
            font_name = span.get("font", "").lower()
            text = span.get("text", "").strip()
            if text and _is_monospace_font(font_name):
                count += 1
    return count


def _extract_block_text(block):
    """Extract all text from a PDF text block."""
    parts = []
    for line in block.get("lines", []):
        line_text = ""
        for span in line.get("spans", []):
            line_text += span.get("text", "")
        parts.append(line_text.strip())
    return "\n".join(parts)


def _is_monospace_font(font_name):
    """Check if a font name corresponds to a monospace font."""
    if not font_name:
        return False
    font_lower = font_name.lower()
    return any(mono in font_lower for mono in MONOSPACE_FONTS) or "mono" in font_lower


def _is_entire_paragraph_monospace(para):
    """Check if all runs in a DOCX paragraph use monospace fonts."""
    if not para.runs:
        return False

    for run in para.runs:
        font_name = (run.font.name or "").lower()
        if not _is_monospace_font(font_name):
            return False
    return True


def _detect_code_languages(code_texts):
    """
    Detect programming languages from code text samples using Pygments.

    Returns a deduplicated list of detected language names.
    """
    if not PYGMENTS_AVAILABLE or not code_texts:
        return []

    detected = set()

    # Sample up to 10 code blocks
    samples = code_texts[:10]

    for text in samples:
        if len(text.strip()) < 10:
            continue
        lang = _guess_language(text)
        if lang:
            detected.add(lang)

    return sorted(list(detected))


def _guess_language(text):
    """Guess the programming language of a code snippet."""
    try:
        lexer = guess_lexer(text)
        name = lexer.name.lower()
        # Filter out generic/unhelpful results
        if name in ("text", "text only", "output"):
            return None
        return lexer.name
    except (ClassNotFound, Exception):
        return None


def get_default():
    """Return the default empty structure for code detection."""
    return {
        "code_blocks_count": 0,
        "languages_detected": [],
        "inline_code_instances": 0,
    }
