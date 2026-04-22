import re
import math

from utils.helpers import count_words, count_sentences

from metrics.link_analyzer import analyze_links
from metrics.media_analyzer import analyze_media
from metrics.metadata_analyzer import analyze_freshness, detect_language
from metrics.duplication_detector import detect_duplicates
from metrics.table_analyzer import analyze_tables
from metrics.code_detector import detect_code
from metrics.readiness_scorer import compute_readiness_score

# Default fallback imports for safe extraction
from metrics.link_analyzer import get_default as link_default
from metrics.media_analyzer import get_default as media_default
from metrics.metadata_analyzer import get_freshness_default as freshness_default
from metrics.metadata_analyzer import get_language_default as language_default
from metrics.duplication_detector import get_default as duplication_default
from metrics.table_analyzer import get_default as table_default
from metrics.code_detector import get_default as code_default
from metrics.readiness_scorer import get_default as readiness_default


def extract_all_metrics(parsed_data, filepath=None, file_type=None):
    warnings = []

    full_text = parsed_data.get("full_text", "")
    paragraphs = parsed_data.get("paragraphs", [])
    headings = parsed_data.get("headings", [])
    tables = parsed_data.get("tables", [])
    images_count = parsed_data.get("images_count", 0)

    # --- Core metrics (unchanged) ---
    word_count = compute_word_count(full_text)
    paragraph_count = compute_paragraph_count(paragraphs)
    heading_count = compute_heading_count(headings)
    sentence_count = compute_sentence_count(full_text)
    table_count = compute_table_count(tables)

    avg_words_per_paragraph = compute_avg_words_per_paragraph(paragraphs)
    avg_words_per_sentence = compute_avg_words_per_sentence(full_text)
    avg_sentence_length = compute_avg_sentence_length(full_text)

    heading_distribution = compute_heading_distribution(headings)
    readability_score = compute_flesch_reading_ease(full_text)
    content_density = compute_content_density(word_count, paragraph_count)

    total_pages = parsed_data.get("total_pages", estimate_page_count(word_count))

    metrics = {
        "total_pages": total_pages,
        "word_count": word_count,
        "paragraph_count": paragraph_count,
        "heading_count": heading_count,
        "sentence_count": sentence_count,
        "table_count": table_count,
        "images_count": images_count,
        "avg_words_per_paragraph": avg_words_per_paragraph,
        "avg_words_per_sentence": avg_words_per_sentence,
        "avg_sentence_length": avg_sentence_length,
        "heading_distribution": heading_distribution,
        "flesch_reading_ease": readability_score,
        "readability_level": classify_readability(readability_score),
        "content_density_score": content_density,
        "estimated_reading_time_minutes": estimate_reading_time(word_count),
    }

    # --- Extended metrics (require filepath) ---
    if filepath and file_type:
        _run_extended_analysis(
            metrics, warnings, filepath, file_type,
            full_text, paragraphs, tables, parsed_data
        )

    return metrics, warnings


def _run_extended_analysis(
    metrics, warnings, filepath, file_type,
    full_text, paragraphs, tables, parsed_data
):

    metadata = parsed_data.get("metadata", {})

    # 1. Link Analysis
    metrics["links"] = _safe_call(
        analyze_links, link_default, warnings,
        filepath, file_type, full_text, warnings
    )

    # 2. Media & Asset Breakdown
    metrics["media"] = _safe_call(
        analyze_media, media_default, warnings,
        filepath, file_type, warnings
    )

    # 3. Content Freshness
    metrics["content_age"] = _safe_call(
        analyze_freshness, freshness_default, warnings,
        metadata, file_type, warnings
    )

    # 4. Duplicate & Boilerplate Detection
    metrics["duplication"] = _safe_call(
        detect_duplicates, duplication_default, warnings,
        paragraphs, warnings
    )

    # 5. Table Quality Analysis
    metrics["tables"] = _safe_call(
        analyze_tables, table_default, warnings,
        filepath, file_type, tables, warnings
    )

    # 6. Language Detection
    metrics["language"] = _safe_call(
        detect_language, language_default, warnings,
        full_text, warnings
    )

    # 7. Code Block Detection
    metrics["code_content"] = _safe_call(
        detect_code, code_default, warnings,
        filepath, file_type, full_text, warnings
    )



    # 9. Document360 Readiness Score (MUST be last)
    metrics["document360_readiness"] = _safe_call(
        compute_readiness_score, readiness_default, warnings,
        metrics, warnings
    )


def _safe_call(func, default_func, warnings, *args):

    try:
        return func(*args)
    except Exception as e:
        warnings.append(f"{func.__name__} (outer): {str(e)}")
        return default_func()


def compute_word_count(text):
    return count_words(text)


def compute_paragraph_count(paragraphs):
    return len(paragraphs)


def compute_heading_count(headings):
    return len(headings)


def compute_sentence_count(text):
    return count_sentences(text)


def compute_table_count(tables):
    return len(tables)


def compute_avg_words_per_paragraph(paragraphs):
    if not paragraphs:
        return 0.0
    total_words = sum(count_words(p) for p in paragraphs)
    return round(total_words / len(paragraphs), 2)


def compute_avg_words_per_sentence(text):
    sentences = count_sentences(text)
    words = count_words(text)
    if sentences == 0:
        return 0.0
    return round(words / sentences, 2)


def compute_avg_sentence_length(text):
    if not text:
        return 0.0
    sentences = re.split(r"[.!?]+", text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if not sentences:
        return 0.0
    total_chars = sum(len(s) for s in sentences)
    return round(total_chars / len(sentences), 2)


def compute_heading_distribution(headings):
    distribution = {}
    for heading in headings:
        level = str(heading.get("level", 1))
        distribution[level] = distribution.get(level, 0) + 1
    return distribution


def compute_flesch_reading_ease(text):
    words = count_words(text)
    sentences = count_sentences(text)
    if words == 0 or sentences == 0:
        return 0.0
    syllables = _count_syllables(text)
    score = 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)
    return round(max(0, min(100, score)), 2)


def _count_syllables(text):
    words = text.lower().split()
    return sum(_syllables_in_word(w) for w in words)


def _syllables_in_word(word):
    word = re.sub(r"[^a-z]", "", word.lower())
    if not word or len(word) <= 3:
        return 1
    vowel_groups = re.findall(r"[aeiouy]+", word)
    count = len(vowel_groups)
    if word.endswith("e") and count > 1:
        count -= 1
    if word.endswith("le") and len(word) > 2 and word[-3] not in "aeiouy":
        count += 1
    return max(1, count)


def classify_readability(score):
    if score >= 80:
        return "Easy"
    elif score >= 50:
        return "Medium"
    return "Complex"


def compute_content_density(word_count, paragraph_count):
    if paragraph_count == 0:
        return 0.0
    avg = word_count / paragraph_count
    if 80 <= avg <= 200:
        density = 100.0
    elif avg < 80:
        density = (avg / 80) * 100
    else:
        density = max(0, 100 - ((avg - 200) / 5))
    return round(min(100, max(0, density)), 2)


def estimate_page_count(word_count, words_per_page=250):
    if word_count == 0:
        return 0
    return max(1, math.ceil(word_count / words_per_page))


def estimate_reading_time(word_count, wpm=200):
    if word_count == 0:
        return 0.0
    return round(word_count / wpm, 1)
