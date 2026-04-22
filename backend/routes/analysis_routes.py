

from flask import Blueprint, request, jsonify

from services.metrics_service import extract_metrics
from services.analysis_service import run_ai_analysis
from utils.helpers import save_uploaded_file, cleanup_file, get_file_extension

analysis_bp = Blueprint("analysis", __name__, url_prefix="/api")


@analysis_bp.route("/analyze", methods=["POST"])
def analyze():

    if "file" not in request.files:
        return jsonify({"error": "No file provided. Use 'file' field in form-data."}), 400

    file = request.files["file"]

    if not file.filename:
        return jsonify({"error": "Uploaded file has no filename."}), 400

    filepath = None
    try:
        filepath = save_uploaded_file(file)
        extension = get_file_extension(file.filename)

        metrics_result = extract_metrics(filepath, extension)
        parsed_data = metrics_result["parsed_data"]
        metrics = metrics_result["metrics"]
        extraction_warnings = metrics_result["extraction_warnings"]

        analysis_result = run_ai_analysis(parsed_data, metrics)
        ai_analysis = analysis_result["analysis"]
        extraction_warnings.extend(analysis_result["ai_warnings"])

        return jsonify({
            "success": True,
            "filename": file.filename,
            "file_type": extension,
            "metrics": metrics,
            "analysis": ai_analysis,
            "extraction_warnings": extraction_warnings,
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except ConnectionError as e:
        return jsonify({"error": f"AI service error: {str(e)}"}), 503

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

    finally:
        cleanup_file(filepath)


@analysis_bp.route("/analyze/full", methods=["POST"])
def full_report():

    if "file" not in request.files:
        return jsonify({"error": "No file provided. Use 'file' field in form-data."}), 400

    file = request.files["file"]

    if not file.filename:
        return jsonify({"error": "Uploaded file has no filename."}), 400

    filepath = None
    try:
        filepath = save_uploaded_file(file)
        extension = get_file_extension(file.filename)

        metrics_result = extract_metrics(filepath, extension)
        parsed_data = metrics_result["parsed_data"]
        metrics = metrics_result["metrics"]
        extraction_warnings = metrics_result["extraction_warnings"]

        analysis_result = run_ai_analysis(parsed_data, metrics)
        ai_analysis = analysis_result["analysis"]
        extraction_warnings.extend(analysis_result["ai_warnings"])

        report = _build_full_report(
            file.filename, extension, parsed_data, metrics, ai_analysis
        )

        return jsonify({
            "success": True,
            "report": report,
            "extraction_warnings": extraction_warnings,
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except ConnectionError as e:
        return jsonify({"error": f"AI service error: {str(e)}"}), 503

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

    finally:
        cleanup_file(filepath)


def _build_full_report(
    filename: str,
    file_type: str,
    parsed_data: dict,
    metrics: dict,
    ai_analysis: dict,
) -> dict:

    return {
        "document_info": {
            "filename": filename,
            "file_type": file_type,
            "metadata": parsed_data.get("metadata", {}),
        },
        "structure": {
            "headings": parsed_data.get("headings", []),
            "paragraph_count": metrics.get("paragraph_count", 0),
            "table_count": metrics.get("table_count", 0),
            "images_count": metrics.get("images_count", 0),
        },
        "metrics": metrics,
        "ai_analysis": ai_analysis,
        "migration_verdict": {
            "ready": ai_analysis.get("migration_readiness", {}).get("status", "Unknown"),
            "readability": ai_analysis.get("readability_level", "Unknown"),
            "top_suggestions": ai_analysis.get("suggestions", [])[:5],
        },
    }
