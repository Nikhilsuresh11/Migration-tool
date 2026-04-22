"""
Analysis service module.

Provides a single entry point for running AI-driven document analysis.
Wraps the ai_analyzer call and handles extraction warning merging so
that route handlers don't need to manage internal warning keys.
"""

from analysis.ai_analyzer import analyze_document


def run_ai_analysis(
    parsed_data: dict,
    metrics: dict,
) -> dict:
    """
    Run AI-driven analysis on a parsed document.

    Args:
        parsed_data: Output dictionary from a parser module
                     (must contain 'full_text', 'headings', etc.).
        metrics: Computed metrics dictionary from the metrics extractor.

    Returns:
        Dictionary with keys:
            - analysis: the AI analysis result dict
            - ai_warnings: list of warning strings from the AI layer

    Raises:
        ConnectionError: If the Groq API call fails.
        ValueError: If the API key is not configured.
    """
    ai_analysis = analyze_document(parsed_data, metrics)

    # Pop internal warnings key and surface separately
    ai_warnings = ai_analysis.pop("_extraction_warnings", [])

    return {
        "analysis": ai_analysis,
        "ai_warnings": ai_warnings,
    }
