"""
Metrics service module.

Provides a single entry point for parsing a document and extracting
all quantitative metrics. Encapsulates parser routing + metrics
extraction so that any route handler can call it without duplicating
the parse → extract pipeline.
"""

from parsers.docx_parser import parse_docx
from parsers.pdf_parser import parse_pdf
from metrics.extractor import extract_all_metrics


def extract_metrics(filepath: str, file_type: str) -> dict:
    """
    Parse a document and extract all metrics.

    Args:
        filepath: Absolute path to the uploaded file on disk.
        file_type: File extension ('docx' or 'pdf').

    Returns:
        Dictionary with keys:
            - parsed_data: raw parser output (text, headings, etc.)
            - metrics: computed metrics dict
            - extraction_warnings: list of warning strings

    Raises:
        ValueError: If the file type is unsupported or the file
                    cannot be parsed.
    """
    parsed_data = _route_to_parser(filepath, file_type)

    metrics, extraction_warnings = extract_all_metrics(
        parsed_data, filepath=filepath, file_type=file_type
    )

    return {
        "parsed_data": parsed_data,
        "metrics": metrics,
        "extraction_warnings": extraction_warnings,
    }


def _route_to_parser(filepath: str, file_type: str) -> dict:
    """Route the file to the appropriate parser based on extension."""
    if file_type == "docx":
        return parse_docx(filepath)
    elif file_type == "pdf":
        return parse_pdf(filepath)
    else:
        raise ValueError(f"Unsupported file type: .{file_type}")
