"""
Document360 migration readiness scoring module.

Computes a readiness score (0–100), grade (A–D), auto-migration
eligibility, estimated manual effort, and lists specific blockers
and warnings based on all other extracted metrics.
"""


def compute_readiness_score(all_metrics, warnings=None):
    """
    Compute the Document360 migration readiness score.

    Must be called last after all other metrics are computed.
    Evaluates the document holistically and produces an actionable
    readiness assessment.

    Args:
        all_metrics: Dictionary containing all computed metrics
                     including extended analysis results.
        warnings: Shared list to append warning messages to.

    Returns:
        Dictionary with score, auto_migratable, blockers, and warnings.
    """
    if warnings is None:
        warnings = []

    try:
        score = 100
        blockers = []
        soft_warnings = []
        effort_hours = 1.0

        # --- Deductions ---

        score, blockers, soft_warnings = _apply_link_deductions(
            all_metrics, score, blockers, soft_warnings
        )

        score, blockers, soft_warnings = _apply_media_deductions(
            all_metrics, score, blockers, soft_warnings
        )

        score, blockers, soft_warnings = _apply_table_deductions(
            all_metrics, score, blockers, soft_warnings
        )

        score, blockers, soft_warnings = _apply_freshness_deductions(
            all_metrics, score, blockers, soft_warnings
        )

        score, blockers, soft_warnings = _apply_content_deductions(
            all_metrics, score, blockers, soft_warnings
        )

        score, blockers, soft_warnings = _apply_readability_deductions(
            all_metrics, score, blockers, soft_warnings
        )

        # Clamp score
        score = max(0, min(100, score))
        auto_migratable = _is_auto_migratable(score, blockers)

        return {
            "score": score,
            "auto_migratable": auto_migratable,
            "blockers": blockers,
            "warnings": soft_warnings,
        }
    except Exception as e:
        if warnings:
            warnings.append(f"Readiness scoring failed: {str(e)}")
        return get_default()


def _apply_link_deductions(metrics, score, blockers, soft_warnings):
    """Apply deductions for broken links."""
    links = metrics.get("links", {})
    broken = links.get("broken_links", 0)

    if broken > 0:
        deduction = min(broken * 5, 20)
        score -= deduction
        blockers.append(
            f"{broken} broken link(s) detected — must be fixed before migration"
        )

    return score, blockers, soft_warnings


def _apply_media_deductions(metrics, score, blockers, soft_warnings):
    """Apply deductions for external image references."""
    media = metrics.get("media", {})
    external_images = media.get("images_referenced_external", 0)

    if external_images > 0:
        score -= 10
        soft_warnings.append(
            f"{external_images} externally referenced image(s) — may break after migration"
        )

    return score, blockers, soft_warnings


def _apply_table_deductions(metrics, score, blockers, soft_warnings):
    """Apply deductions for complex tables."""
    tables = metrics.get("tables", {})
    complex_tables = tables.get("complex_tables", 0)

    if complex_tables > 0:
        deduction = min(complex_tables * 5, 15)
        score -= deduction
        blockers.append(
            f"{complex_tables} complex table(s) (>6 cols or >20 rows) — may need restructuring"
        )

    return score, blockers, soft_warnings


def _apply_freshness_deductions(metrics, score, blockers, soft_warnings):
    """Apply deductions for stale content."""
    content_age = metrics.get("content_age", {})
    staleness = content_age.get("staleness_risk", "Unknown")

    if staleness == "High":
        score -= 15
        blockers.append(
            "Document is over 1 year old — content review recommended before migration"
        )
    elif staleness == "Medium":
        score -= 5
        soft_warnings.append(
            "Document is 6–12 months old — verify content is still current"
        )

    return score, blockers, soft_warnings


def _apply_content_deductions(metrics, score, blockers, soft_warnings):
    """Apply deductions for content quality issues."""
    # Boilerplate ratio
    duplication = metrics.get("duplication", {})
    boilerplate = duplication.get("boilerplate_ratio_percent", 0)

    if boilerplate > 20:
        score -= 10
        soft_warnings.append(
            f"High boilerplate ratio ({boilerplate}%) — contains significant duplicate content"
        )

    # Average words per paragraph
    avg_wpp = metrics.get("avg_words_per_paragraph", 0)
    if avg_wpp > 80:
        score -= 5
        soft_warnings.append(
            f"Long paragraphs (avg {avg_wpp} words) — consider breaking into smaller sections"
        )

    return score, blockers, soft_warnings


def _apply_readability_deductions(metrics, score, blockers, soft_warnings):
    """Apply deductions for poor readability."""
    flesch = metrics.get("flesch_reading_ease", 0)

    if flesch < 30:
        score -= 10
        soft_warnings.append(
            f"Low readability score ({flesch}) — content is very complex, "
            "consider simplifying language"
        )

    return score, blockers, soft_warnings


def _is_auto_migratable(score, blockers):
    """
    Determine if the document can be auto-migrated.

    Auto-migration is possible if score >= 75 and there are no blockers.
    """
    return score >= 75 and len(blockers) == 0


def get_default():
    """Return the default structure for readiness scoring."""
    return {
        "score": 0,
        "auto_migratable": False,
        "blockers": ["Readiness scoring could not be completed"],
        "warnings": [],
    }
