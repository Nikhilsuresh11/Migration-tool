from flask import Blueprint, request, jsonify

from services.metrics_service import extract_metrics
from utils.helpers import save_uploaded_file, cleanup_file, get_file_extension

metrics_bp = Blueprint("metrics", __name__, url_prefix="/api")


@metrics_bp.route("/metrics", methods=["POST"])
def get_metrics():

    if "file" not in request.files:
        return jsonify({"error": "No file provided. Use 'file' field in form-data."}), 400

    file = request.files["file"]

    if not file.filename:
        return jsonify({"error": "Uploaded file has no filename."}), 400

    filepath = None
    try:
        filepath = save_uploaded_file(file)
        extension = get_file_extension(file.filename)

        result = extract_metrics(filepath, extension)

        return jsonify({
            "success": True,
            "filename": file.filename,
            "file_type": extension,
            "metrics": result["metrics"],
            "extraction_warnings": result["extraction_warnings"],
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

    finally:
        cleanup_file(filepath)
