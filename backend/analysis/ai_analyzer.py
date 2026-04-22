import json
import math
import requests
import logging

from groq import Groq

from config import Config
from utils.helpers import truncate_text


_DEFAULT_CONTENT_CLASSIFICATION = {
    "document_type": "Unknown",
    "domain": "Unknown",
    "audience_type": "General Public",
    "content_format": "Unknown",
    "is_evergreen": False,
    "is_versioned": False,
}

_DEFAULT_TONE_ANALYSIS = {
    "detected_tone": "Unknown",
    "tone_consistency": "Unknown",
    "passive_voice_ratio_percent": 0,
    "first_person_usage": False,
    "brand_voice_alignment": "Neutral",
}

_DEFAULT_CONTENT_DEBT = {
    "outdated_references_detected": [],
    "unresolved_placeholders": [],
    "abbreviations_without_definition": [],
    "broken_concept_references": 0,
    "content_debt_score": 0,
}

_DEFAULT_VISUAL_CONTENT_ANALYSIS = {
    "image_to_text_ratio": "Low",
    "images_likely_decorative": 0,
    "images_likely_informational": 0,
    "chart_heavy_sections": [],
    "accessibility_risk": "Low",
    "images_with_alt_text": 0,
    "migration_recommendation": "No recommendation available.",
}


def analyze_document(parsed_data: dict, metrics: dict) -> dict:
    """
    Perform AI-driven analysis on a parsed document.

    Sends document content and metrics to the Groq LLaMA model
    for comprehensive quality and migration readiness evaluation.

    Args:
        parsed_data: Output dictionary from a parser module.
        metrics: Output dictionary from the metrics extractor.

    Returns:
        Dictionary containing AI analysis results with all original
        and new analysis blocks.

    Raises:
        ConnectionError: If the Groq API is unreachable.
        ValueError: If the API key is not configured.
    """
    _validate_api_key()

    prompt = _build_analysis_prompt(parsed_data, metrics)
    system_prompt = _build_system_prompt()

    raw_response = _call_ai_api(system_prompt, prompt)
    analysis = _parse_ai_response(raw_response, metrics)
    return analysis


def _call_ai_api(system_prompt: str, prompt: str) -> str:
    """Try Groq first, fallback to OpenRouter on failure."""
    try:
        return _call_groq_api(system_prompt, prompt)
    except Exception as e:
        logging.warning(f"Groq API failed, attempting OpenRouter fallback: {str(e)}")
        if Config.OPENROUTER_API_KEY:
            try:
                return _call_openrouter_api(system_prompt, prompt)
            except Exception as e2:
                raise ConnectionError(f"Both AI APIs failed. Groq: {str(e)}, OpenRouter: {str(e2)}")
        else:
            raise ConnectionError(f"Groq API failed and no OpenRouter key provided. Error: {str(e)}")


def _validate_api_key() -> None:
    if not Config.GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY is not set. Please set it in your .env file."
        )


def _build_system_prompt() -> str:
    return (
        "You are a senior documentation migration specialist with 10+ years "
        "of experience migrating enterprise content to Document360. You analyze "
        "documents for migration readiness, content quality, and information "
        "architecture fit. You are precise, critical, and actionable — you "
        "never give vague suggestions.\n\n"
        "You MUST respond with ONLY a valid JSON object (no markdown, no code "
        "blocks, no preamble, no explanation). The JSON must follow this exact "
        "schema:\n\n"
        + _get_json_schema()
    )


def _get_json_schema() -> str:
    return """{
    "readability_level": "Easy | Medium | Complex",
    "readability_explanation": "Brief explanation of why this readability level was assigned",
    "content_clarity": {
        "score": 1-10,
        "assessment": "Brief assessment of content clarity and consistency"
    },
    "structural_quality": {
        "score": 1-10,
        "assessment": "well-organized | moderately-organized | fragmented",
        "details": "Explanation of the document's structural quality"
    },
    "migration_readiness": {
        "status": "Ready | Needs Minor Fixes | Needs Major Restructuring",
        "details": "Explanation of migration readiness"
    },
    "content_issues": [
        "List of specific content issues found"
    ],
    "suggestions": [
        "Each suggestion MUST cite a specific section title, metric value, or acronym found in this document. Example: 'Section \"Financial Highlights\" has avg 120 words/paragraph — split into sub-sections.' No generic advice like 'improve readability'."
    ],
    "summary": "A 2-3 sentence overall summary of the document quality and migration readiness",

    "content_classification": {
        "document_type": "e.g. Annual Report, API Guide, User Manual, Policy Doc",
        "domain": "e.g. Finance, Engineering, HR, Product",
        "audience_type": "e.g. Executive, Developer, End User, General Public",
        "content_format": "e.g. Data-heavy narrative, Step-by-step guide, Reference material",
        "is_evergreen": true/false,
        "is_versioned": true/false
    },

    "tone_analysis": {
        "detected_tone": "Formal | Conversational | Technical | Marketing",
        "tone_consistency": "Consistent | Inconsistent | Mixed",
        "passive_voice_ratio_percent": 0-100,
        "first_person_usage": true/false,
        "brand_voice_alignment": "Neutral | Aligned | Misaligned"
    },

    "content_debt": {
        "outdated_references_detected": ["ONLY relative time phrases like 'last year', 'next quarter', 'recently', or past events presented as current. Never include years used as data labels or column headers."],
        "unresolved_placeholders": [{"text": "the placeholder text e.g. [TBD]", "context": "~20 words surrounding the placeholder"}],
        "abbreviations_without_definition": ["list of acronyms used without prior expansion"],
        "broken_concept_references": 0,
        "content_debt_score": 1-10
    },

    "visual_content_analysis": {
        "image_to_text_ratio": "Low | Medium | High",
        "images_likely_decorative": 0,
        "images_likely_informational": 0,
        "chart_heavy_sections": ["section titles where charts/figures are likely dense"],
        "accessibility_risk": "Low | Medium | High",
        "images_with_alt_text": 0,
        "migration_recommendation": "one actionable sentence about image migration"
    }
}"""


def _build_analysis_prompt(parsed_data: dict, metrics: dict) -> str:
    full_text = parsed_data.get("full_text", "")
    truncated_text = truncate_text(full_text, max_length=12000)

    headings = parsed_data.get("headings", [])
    heading_list = _format_headings_for_prompt(headings)

    # Build a clean metrics JSON block for context
    metrics_context = {
        "total_pages": metrics.get("total_pages", 0),
        "word_count": metrics.get("word_count", 0),
        "paragraph_count": metrics.get("paragraph_count", 0),
        "heading_count": metrics.get("heading_count", 0),
        "sentence_count": metrics.get("sentence_count", 0),
        "avg_words_per_paragraph": metrics.get("avg_words_per_paragraph", 0),
        "avg_words_per_sentence": metrics.get("avg_words_per_sentence", 0),
        "flesch_reading_ease": metrics.get("flesch_reading_ease", 0),
        "table_count": metrics.get("table_count", 0),
        "images_count": metrics.get("images_count", 0),
        "estimated_reading_time_minutes": metrics.get("estimated_reading_time_minutes", 0),
        "heading_distribution": metrics.get("heading_distribution", {}),
    }

    metrics_json = json.dumps(metrics_context, indent=2)

    prompt = f"""Analyze the following document for migration readiness to Document360.

## Document Metrics
```json
{metrics_json}
```

## Document Structure (Headings)
{heading_list}

## Document Content (first ~6000 tokens)
{truncated_text}

## Analysis Instructions

Be specific — quote actual section titles, list actual acronyms found, name actual outdated references. Do not give generic advice.

For suggestions: EVERY suggestion MUST cite a specific section title, metric value, or acronym found in this document. Bad: "Improve readability". Good: "Section 'Risk Management' averages 135 words per paragraph — split into sub-sections with sub-headings."

For content_classification: identify the document type, domain, intended audience, and content format from the actual content. Check if the content is evergreen (not time-bound) and whether it references specific versions or releases.

For tone_analysis: assess the actual writing style. Estimate the passive voice percentage. Check for first-person pronouns (I, we, our). Evaluate tone consistency across sections.

For content_debt.outdated_references_detected: ONLY flag relative time phrases ("last year", "next quarter", "recently", "current year") or past events described as if they are current/upcoming. NEVER flag specific years used as data point labels, column headers in tables, or historical dates that are factual references (e.g. "FY2024" as a column header is NOT outdated).

For content_debt.unresolved_placeholders: return each as an object with "text" (the placeholder itself) and "context" (approximately 20 words surrounding the placeholder for reviewability).

For content_debt: also scan for actual acronyms used without prior definition in the document. Count cross-references ("as mentioned above", "see section X") that may break after migration.

For visual_content_analysis: use the images_count ({metrics_context['images_count']}) and word_count ({metrics_context['word_count']}) to assess image-to-text ratio. Estimate how many images are likely decorative vs informational based on context clues in the text. Identify sections that appear chart/figure heavy. Assess accessibility risk.



Respond ONLY with the valid JSON object following the schema in your instructions."""

    return prompt


def _format_headings_for_prompt(headings: list) -> str:
    if not headings:
        return "No headings detected in the document."

    lines = []
    for h in headings:
        indent = "  " * (h.get("level", 1) - 1)
        lines.append(f"{indent}- [H{h.get('level', 1)}] {h.get('text', '')}")

    return "\n".join(lines)


def _call_groq_api(system_prompt: str, user_prompt: str) -> str:
    """
    Send a request to the Groq API and return the response text.

    Args:
        system_prompt: The system-level instruction for the model.
        user_prompt: The user message containing document data.

    Returns:
        Raw text response from the AI model.

    Raises:
        ConnectionError: If the API call fails.
    """
    client = Groq(api_key=Config.GROQ_API_KEY)

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        model=Config.GROQ_MODEL,
        max_tokens=Config.GROQ_MAX_TOKENS,
        temperature=Config.GROQ_TEMPERATURE,
        response_format={"type": "json_object"},
    )

    return chat_completion.choices[0].message.content


def _call_openrouter_api(system_prompt: str, user_prompt: str) -> str:
    """Call OpenRouter API as a fallback."""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://localhost:3000", # Required by OpenRouter
        "X-Title": "Galaxy Dashboard Analyzer"
    }
    
    payload = {
        "model": Config.OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": Config.GROQ_TEMPERATURE,
        "max_tokens": Config.GROQ_MAX_TOKENS,
        "reasoning": {"enabled": True}
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=90)
    response.raise_for_status()
    
    data = response.json()
    if "choices" in data and len(data["choices"]) > 0:
        return data["choices"][0]["message"]["content"]
    
    raise ValueError(f"OpenRouter returned unexpected format: {json.dumps(data)}")


def _parse_ai_response(raw_response: str, metrics: dict) -> dict:

    if not raw_response:
        raise ValueError("Empty response from AI model.")

    cleaned = raw_response.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    if cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()

    try:
        parsed = json.loads(cleaned)
        return _validate_and_normalize(parsed, metrics)
    except json.JSONDecodeError:
        raise ValueError("AI returned a non-JSON response. Raw output preserved.")


def _validate_and_normalize(parsed: dict, metrics: dict) -> dict:

    extraction_warnings = []

    original_defaults = {
        "readability_level": "Medium",
        "readability_explanation": "No explanation provided.",
        "content_clarity": {"score": 5, "assessment": "Not assessed."},
        "structural_quality": {
            "score": 5,
            "assessment": "moderately-organized",
            "details": "Not assessed.",
        },
        "migration_readiness": {
            "status": "Needs Minor Fixes",
            "details": "Not assessed.",
        },
        "content_issues": [],
        "suggestions": [],
        "summary": "Analysis incomplete.",
    }

    for key, default_value in original_defaults.items():
        if key not in parsed:
            parsed[key] = default_value
        elif isinstance(default_value, dict):
            for sub_key, sub_default in default_value.items():
                if sub_key not in parsed[key]:
                    parsed[key][sub_key] = sub_default

    new_blocks = {
        "content_classification": _DEFAULT_CONTENT_CLASSIFICATION,
        "tone_analysis": _DEFAULT_TONE_ANALYSIS,
        "content_debt": _DEFAULT_CONTENT_DEBT,
        "visual_content_analysis": _DEFAULT_VISUAL_CONTENT_ANALYSIS,
    }

    for block_key, default_structure in new_blocks.items():
        if block_key not in parsed:
            parsed[block_key] = dict(default_structure)
            extraction_warnings.append(
                f"AI did not return '{block_key}' — filled with defaults."
            )
        else:
            block = parsed[block_key]
            if isinstance(block, dict) and isinstance(default_structure, dict):
                for sub_key, sub_default in default_structure.items():
                    if sub_key not in block:
                        block[sub_key] = (
                            dict(sub_default) if isinstance(sub_default, dict)
                            else list(sub_default) if isinstance(sub_default, list)
                            else sub_default
                        )

    if "migration_readiness" in parsed and "score" in parsed["migration_readiness"]:
        del parsed["migration_readiness"]["score"]


    if extraction_warnings:
        parsed["_extraction_warnings"] = extraction_warnings

    return parsed
