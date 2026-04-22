"""
Utility helper functions for the document analysis tool.

Provides shared functionality for file validation, text cleaning,
and common operations used across modules.
"""

import os
import re
import uuid

from werkzeug.utils import secure_filename

from config import Config


def is_allowed_file(filename: str) -> bool:
    """Check if the uploaded file has an allowed extension."""
    if "." not in filename:
        return False
    extension = filename.rsplit(".", 1)[1].lower()
    return extension in Config.ALLOWED_EXTENSIONS


def get_file_extension(filename: str) -> str:
    """Extract and return the lowercase file extension."""
    if "." not in filename:
        return ""
    return filename.rsplit(".", 1)[1].lower()


def generate_unique_filename(original_filename: str) -> str:
    """Generate a unique filename to prevent collisions."""
    extension = get_file_extension(original_filename)
    safe_name = secure_filename(original_filename)
    base_name = safe_name.rsplit(".", 1)[0] if "." in safe_name else safe_name
    unique_id = uuid.uuid4().hex[:8]
    return f"{base_name}_{unique_id}.{extension}"


def save_uploaded_file(file) -> str:
    """
    Save an uploaded file to the uploads directory.

    Args:
        file: Werkzeug FileStorage object from the request.

    Returns:
        Absolute path to the saved file.

    Raises:
        ValueError: If the file has no name or an invalid extension.
    """
    if not file or not file.filename:
        raise ValueError("No file provided or file has no name.")

    if not is_allowed_file(file.filename):
        raise ValueError(
            f"File type not allowed. Accepted types: {', '.join(Config.ALLOWED_EXTENSIONS)}"
        )

    Config.init_upload_folder()
    unique_name = generate_unique_filename(file.filename)
    filepath = os.path.join(Config.UPLOAD_FOLDER, unique_name)
    file.save(filepath)
    return filepath


def cleanup_file(filepath: str) -> None:
    """Remove a file from disk if it exists."""
    try:
        if filepath and os.path.exists(filepath):
            os.remove(filepath)
    except OSError:
        pass


def clean_text(text: str) -> str:
    """
    Clean extracted text by normalizing whitespace and removing
    non-printable characters while preserving paragraph structure.
    """
    if not text:
        return ""

    # Remove non-printable characters except newlines and tabs
    text = re.sub(r"[^\S\n\t]+", " ", text)

    # Normalize multiple newlines to double newlines (paragraph separator)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def truncate_text(text: str, max_length: int = 15000) -> str:
    """
    Truncate text to a maximum character length for AI analysis.

    Ensures the truncation happens at a word boundary to avoid
    sending partial words to the AI model.
    """
    if not text or len(text) <= max_length:
        return text

    truncated = text[:max_length]
    last_space = truncated.rfind(" ")
    if last_space > max_length * 0.8:
        truncated = truncated[:last_space]

    return truncated + "\n\n[Content truncated for analysis...]"


def count_words(text: str) -> int:
    """Count the number of words in a text string."""
    if not text:
        return 0
    return len(text.split())


def count_sentences(text: str) -> int:
    """Count the approximate number of sentences in a text string."""
    if not text:
        return 0
    # Split on sentence-ending punctuation
    sentences = re.split(r"[.!?]+", text)
    # Filter out empty strings
    return len([s for s in sentences if s.strip()])
