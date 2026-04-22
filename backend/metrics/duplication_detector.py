from difflib import SequenceMatcher
from collections import Counter


def detect_duplicates(paragraphs, warnings=None):

    if warnings is None:
        warnings = []

    try:
        if not paragraphs or len(paragraphs) < 2:
            return get_default()

        duplicate_count = _find_duplicate_pairs(paragraphs, threshold=0.85)
        boilerplate_ratio = _compute_boilerplate_ratio(duplicate_count, len(paragraphs))
        repeated_phrases = _find_repeated_phrases(paragraphs, min_words=3, min_count=4, top_n=5)

        return {
            "duplicate_section_count": duplicate_count,
            "boilerplate_ratio_percent": boilerplate_ratio,
            "repeated_phrases": repeated_phrases,
        }
    except Exception as e:
        warnings.append(f"Duplication detection failed: {str(e)}")
        return get_default()


def _find_duplicate_pairs(paragraphs, threshold=0.85):

    substantial = [p for p in paragraphs if len(p.split()) >= 10]

    if len(substantial) < 2:
        return 0

    max_compare = min(len(substantial), 200)
    candidates = substantial[:max_compare]

    duplicate_count = 0
    seen_pairs = set()

    for i in range(len(candidates)):
        for j in range(i + 1, len(candidates)):
            pair_key = (i, j)
            if pair_key in seen_pairs:
                continue

            ratio = SequenceMatcher(
                None,
                candidates[i].lower(),
                candidates[j].lower(),
            ).ratio()

            if ratio >= threshold:
                duplicate_count += 1
                seen_pairs.add(pair_key)

    return duplicate_count


def _compute_boilerplate_ratio(duplicate_count, total_paragraphs):

    if total_paragraphs == 0:
        return 0.0

    involved = min(duplicate_count * 2, total_paragraphs)
    ratio = (involved / total_paragraphs) * 100
    return round(ratio, 2)


def _find_repeated_phrases(paragraphs, min_words=3, min_count=4, top_n=5):

    all_text = " ".join(paragraphs).lower()
    words = all_text.split()

    if len(words) < min_words:
        return []

    # Generate n-grams
    ngrams = _generate_ngrams(words, min_words)
    counter = Counter(ngrams)

    # Filter by minimum count and sort by frequency
    frequent = [
        {"phrase": phrase, "count": count}
        for phrase, count in counter.most_common(top_n * 3)
        if count >= min_count
    ]

    # Filter out generic/stop-word-heavy phrases
    filtered = _filter_meaningful_phrases(frequent)

    return filtered[:top_n]


def _generate_ngrams(words, n):
    """Generate n-grams from a list of words as joined strings."""
    ngrams = []
    for i in range(len(words) - n + 1):
        ngram = " ".join(words[i:i + n])
        # Skip ngrams that are mostly punctuation
        alpha_chars = sum(1 for c in ngram if c.isalpha())
        if alpha_chars > len(ngram) * 0.5:
            ngrams.append(ngram)
    return ngrams


def _filter_meaningful_phrases(phrases):
    """Filter out phrases that are mostly stop words."""
    stop_words = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been",
        "being", "have", "has", "had", "do", "does", "did", "will",
        "shall", "would", "could", "should", "may", "might", "must",
        "can", "to", "of", "in", "for", "on", "with", "at", "by",
        "from", "as", "into", "about", "and", "or", "but", "not",
        "this", "that", "these", "those", "it", "its",
    }

    filtered = []
    for item in phrases:
        words = item["phrase"].split()
        non_stop = [w for w in words if w not in stop_words]
        # Keep phrase if at least one word is not a stop word
        if len(non_stop) >= 1:
            filtered.append(item)

    return filtered


def get_default():
    return {
        "duplicate_section_count": 0,
        "boilerplate_ratio_percent": 0.0,
        "repeated_phrases": [],
    }
