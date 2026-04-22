import hashlib
import json
import time
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor, TimeoutError

from flask import Blueprint, request, jsonify, make_response

from services.metrics_service import extract_metrics
from services.analysis_service import run_ai_analysis
from utils.helpers import save_uploaded_file, cleanup_file, get_file_extension

report_bp = Blueprint("report", __name__, url_prefix="/api")


_REPORT_CACHE_MAX = 20
_report_cache: OrderedDict = OrderedDict()


def _cache_report(report_id: str, report_data: dict) -> None:
    if report_id in _report_cache:
        _report_cache.move_to_end(report_id)
    else:
        if len(_report_cache) >= _REPORT_CACHE_MAX:
            _report_cache.popitem(last=False)
        _report_cache[report_id] = report_data


def _get_cached_report(report_id: str) -> dict | None:
    if report_id in _report_cache:
        _report_cache.move_to_end(report_id)
        return _report_cache[report_id]
    return None



def build_summary(
    filename: str,
    file_type: str,
    metrics: dict,
    analysis: dict | None,
) -> dict:

    d360 = metrics.get("document360_readiness", {})
    effort = (analysis or {}).get("migration_effort_breakdown", {})
    blockers = d360.get("blockers", [])
    warnings = d360.get("warnings", [])
    score = d360.get("score", 0)
    grade = d360.get("grade", "D")
    person_days = effort.get("estimated_person_days", 0)
    overall_effort = effort.get("overall_effort", "Unknown")

    if score >= 90:
        status_label = "Clean"
    elif score >= 70:
        status_label = "Needs minor fixes"
    else:
        status_label = "Major rework required"

    return {
        "filename": filename,
        "file_type": file_type,
        "readiness_grade": grade,
        "readiness_score": score,
        "auto_migratable": d360.get("auto_migratable", False),
        "overall_effort": overall_effort,
        "person_days": person_days,
        "status_label": status_label,
        "blocker_count": len(blockers),
        "warning_count": len(warnings),
        "top_blockers": blockers[:3],
        "top_warnings": warnings[:3],
    }


@report_bp.route("/report", methods=["POST"])
def generate_report():

    start_time = time.time()

    if "file" not in request.files:
        return jsonify({
            "success": False,
            "error": "unsupported_file",
            "detail": "No file provided. Use 'file' field in form-data.",
        }), 400

    file = request.files["file"]

    if not file.filename:
        return jsonify({
            "success": False,
            "error": "unsupported_file",
            "detail": "Uploaded file has no filename.",
        }), 400

    extension = get_file_extension(file.filename)
    if extension not in ("pdf", "docx"):
        return jsonify({
            "success": False,
            "error": "unsupported_file",
            "detail": f"Unsupported file type: .{extension}. Only .pdf and .docx are accepted.",
        }), 400

    filepath = None
    try:
        filepath = save_uploaded_file(file)

        file_hash = _compute_file_hash(filepath)
        report_id = file_hash[:12]

        try:
            metrics_result = extract_metrics(filepath, extension)
        except ValueError as e:
            return jsonify({
                "success": False,
                "error": "unsupported_file",
                "detail": str(e),
            }), 400
        except Exception as e:
            return jsonify({
                "success": False,
                "error": "metrics_extraction_failed",
                "detail": str(e),
            }), 422

        parsed_data = metrics_result["parsed_data"]
        metrics = metrics_result["metrics"]
        extraction_warnings = list(metrics_result["extraction_warnings"])

        ai_analysis = None
        with ThreadPoolExecutor(max_workers=1) as executor:
            analysis_future = executor.submit(
                run_ai_analysis, parsed_data, metrics
            )
            try:
                analysis_result = analysis_future.result(timeout=60)
                ai_analysis = analysis_result["analysis"]
                extraction_warnings.extend(analysis_result["ai_warnings"])
            except TimeoutError:
                extraction_warnings.append(
                    "AI analysis failed: Request timed out after 60 seconds"
                )
            except Exception as e:
                extraction_warnings.append(
                    f"AI analysis failed: {str(e)}"
                )

        summary = build_summary(
            file.filename, extension, metrics, ai_analysis
        )

        processing_time = round(time.time() - start_time, 3)

        response_body = {
            "success": True,
            "report_id": report_id,
            "summary": summary,
            "metrics": metrics,
            "analysis": ai_analysis,
            "file_type": extension,
            "filename": file.filename,
            "extraction_warnings": extraction_warnings,
        }

        _cache_report(report_id, response_body)

        response = make_response(jsonify(response_body), 200)
        response.headers["X-Processing-Time"] = str(processing_time)
        response.headers["X-Readiness-Grade"] = summary["readiness_grade"]
        response.headers["X-Auto-Migratable"] = str(
            summary["auto_migratable"]
        ).lower()

        return response

    finally:
        cleanup_file(filepath)



@report_bp.route("/report/<report_id>", methods=["GET"])
def get_report(report_id: str):

    cached = _get_cached_report(report_id)

    if cached is None:
        return jsonify({
            "success": False,
            "error": "report_not_found",
            "detail": f"No cached report found for ID '{report_id}'. "
                      "Reports are cached temporarily (max 20) and may "
                      "have been evicted.",
        }), 404

    return jsonify(cached), 200


def _compute_file_hash(filepath: str) -> str:
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()
