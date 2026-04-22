
from flask import Blueprint, request, jsonify

from parsers.docx_parser import parse_docx
from parsers.pdf_parser import parse_pdf
from utils.helpers import save_uploaded_file, cleanup_file, get_file_extension

parse_bp = Blueprint("parse", __name__, url_prefix="/api")


@parse_bp.route("/parse", methods=["POST"])
def parse_document():

    if "file" not in request.files:
        return jsonify({"error": "No file provided. Use 'file' field in form-data."}), 400

    file = request.files["file"]

    if not file.filename:
        return jsonify({"error": "Uploaded file has no filename."}), 400

    filepath = None
    try:
        filepath = save_uploaded_file(file)
        extension = get_file_extension(file.filename)

        parsed_data = _route_to_parser(filepath, extension)

        # Build structured response — exclude raw full_text dump
        response_data = {k: v for k, v in parsed_data.items() if k != "full_text"}

        return jsonify({
            "success": True,
            "filename": file.filename,
            "file_type": extension,
            "data": response_data,
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

    finally:
        cleanup_file(filepath)


def _route_to_parser(filepath: str, extension: str) -> dict:
    if extension == "docx":
        return parse_docx(filepath)
    elif extension == "pdf":
        return parse_pdf(filepath)
    else:
        raise ValueError(f"Unsupported file type: .{extension}")
