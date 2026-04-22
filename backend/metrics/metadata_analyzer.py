"""
Analysis modules for Freshness and Language.
(Absorbed into metadata_analyzer)
"""
import re



# ====================================================================
# Freshness Analyzer Logic
# ====================================================================

from datetime import datetime, date

def analyze_freshness(metadata, file_type, warnings=None):
    if warnings is None:
        warnings = []

    try:
        created_str = metadata.get("created", "")
        modified_str = metadata.get("modified", "")

        created_date = _parse_date(created_str, file_type)
        modified_date = _parse_date(modified_str, file_type)

        reference_date = modified_date or created_date
        days_since = _compute_days_since(reference_date)
        staleness = _classify_staleness(days_since)

        return {
            "document_created": _format_date(created_date),
            "last_modified": _format_date(modified_date),
            "days_since_last_update": days_since,
            "staleness_risk": staleness,
        }
    except Exception as e:
        warnings.append(f"Content freshness analysis failed: {str(e)}")
        return get_freshness_default()

def _parse_date(date_str, file_type):
    if not date_str or date_str.strip() == "" or date_str.strip().lower() == "none":
        return None

    date_str = date_str.strip()

    if date_str.startswith("D:"):
        return _parse_pdf_date(date_str)

    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%d/%m/%Y",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str[:len(fmt) + 5], fmt)
        except (ValueError, IndexError):
            continue
    return None

def _parse_pdf_date(date_str):
    cleaned = date_str[2:]
    cleaned = re.sub(r"[+\-Z].*$", "", cleaned)
    if len(cleaned) < 8:
        return None
    try:
        if len(cleaned) >= 14:
            return datetime.strptime(cleaned[:14], "%Y%m%d%H%M%S")
        elif len(cleaned) >= 8:
            return datetime.strptime(cleaned[:8], "%Y%m%d")
    except ValueError:
        pass
    return None

def _compute_days_since(reference_date):
    if reference_date is None:
        return 0
    today = datetime.now()
    if reference_date.tzinfo is not None:
        reference_date = reference_date.replace(tzinfo=None)
    delta = today - reference_date
    return max(0, delta.days)

def _classify_staleness(days):
    if days == 0:
        return "Unknown"
    if days < 180:
        return "Low"
    if days <= 365:
        return "Medium"
    return "High"

def _format_date(dt):
    if dt is None:
        return None
    return dt.strftime("%Y-%m-%d")

def get_freshness_default():
    return {
        "document_created": None,
        "last_modified": None,
        "days_since_last_update": 0,
        "staleness_risk": "Unknown",
    }


# ====================================================================
# Language Detector Logic
# ====================================================================

from langdetect import detect, detect_langs, LangDetectException

RTL_LANGUAGES = {"ar", "he", "fa", "ur", "yi", "ps", "sd", "ku", "ug"}

def detect_language(full_text, warnings=None):
    if warnings is None:
        warnings = []

    try:
        if not full_text or len(full_text.strip()) < 20:
            return get_language_default()

        primary = _detect_primary_language(full_text)
        secondary = _detect_secondary_languages(full_text)
        rtl = _has_rtl_content(primary, secondary)

        return {
            "primary_language": primary,
            "secondary_languages_detected": secondary,
            "rtl_content_detected": rtl,
        }
    except Exception as e:
        warnings.append(f"Language detection failed: {str(e)}")
        return get_language_default()

def _detect_primary_language(text):
    try:
        return detect(text)
    except LangDetectException:
        return "unknown"

def _detect_secondary_languages(text):
    primary = _detect_primary_language(text)
    chunks = _split_into_chunks(text, num_chunks=10)

    detected_languages = set()
    for chunk in chunks:
        if len(chunk.strip()) < 20:
            continue
        try:
            lang = detect(chunk)
            if lang != primary:
                detected_languages.add(lang)
        except LangDetectException:
            continue

    return sorted(list(detected_languages))

def _split_into_chunks(text, num_chunks=10):
    if not text:
        return []
    words = text.split()
    if len(words) < num_chunks:
        return [text]

    chunk_size = len(words) // num_chunks
    chunks = []
    for i in range(num_chunks):
        start = i * chunk_size
        end = start + chunk_size if i < num_chunks - 1 else len(words)
        chunk = " ".join(words[start:end])
        chunks.append(chunk)

    return chunks

def _has_rtl_content(primary, secondary_languages):
    all_languages = {primary} | set(secondary_languages)
    return bool(all_languages & RTL_LANGUAGES)

def get_language_default():
    return {
        "primary_language": "unknown",
        "secondary_languages_detected": [],
        "rtl_content_detected": False,
    }

