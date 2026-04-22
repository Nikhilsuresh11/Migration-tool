
from docx import Document
import fitz


def analyze_media(filepath, file_type, warnings=None):

    if warnings is None:
        warnings = []

    try:
        if file_type == "docx":
            return _analyze_docx_media(filepath)
        elif file_type == "pdf":
            return _analyze_pdf_media(filepath)
        return get_default()
    except Exception as e:
        warnings.append(f"Media analysis failed: {str(e)}")
        return get_default()


def _analyze_docx_media(filepath):
    doc = Document(filepath)

    images_count = 0
    images_embedded = 0
    images_external = 0
    image_formats = {}
    total_size_bytes = 0
    videos = 0
    attachments = 0

    for rel in doc.part.rels.values():
        rel_type = rel.reltype.lower()

        if "image" in rel_type:
            images_count += 1
            if rel.is_external:
                images_external += 1
            else:
                images_embedded += 1
                _process_docx_image_part(
                    rel, image_formats, total_size_bytes_ref=[total_size_bytes]
                )
                # Update total_size from ref
                total_size_bytes = _get_docx_image_size(rel, total_size_bytes)

        elif "video" in rel_type or "media" in rel_type:
            videos += 1

        elif "oleObject" in rel_type or "package" in rel_type:
            attachments += 1

    # Extract image format from part names
    image_formats = _count_docx_image_formats(doc)

    return {
        "images_count": images_count,
        "images_embedded_base64": images_embedded,
        "images_referenced_external": images_external,
        "image_formats": image_formats,
        "total_media_size_mb": round(total_size_bytes / (1024 * 1024), 2),
        "videos_embedded": videos,
        "attachments_count": attachments,
    }


def _get_docx_image_size(rel, current_total):
    try:
        if not rel.is_external and hasattr(rel, "target_part"):
            blob = rel.target_part.blob
            if blob:
                return current_total + len(blob)
    except Exception:
        pass
    return current_total


def _count_docx_image_formats(doc):
    formats = {}
    for rel in doc.part.rels.values():
        if "image" not in rel.reltype.lower():
            continue
        if rel.is_external:
            continue
        try:
            part_name = str(rel.target_part.partname).lower()
            ext = part_name.rsplit(".", 1)[-1] if "." in part_name else "unknown"
            # Normalize common extensions
            ext = _normalize_image_ext(ext)
            formats[ext] = formats.get(ext, 0) + 1
        except Exception:
            formats["unknown"] = formats.get("unknown", 0) + 1
    return formats


def _analyze_pdf_media(filepath):
    doc = fitz.open(filepath)

    seen_xrefs = set()
    image_formats = {}
    total_size_bytes = 0
    videos = 0
    attachments = 0

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)

        # Count images
        for img_info in page.get_images(full=True):
            xref = img_info[0]
            if xref in seen_xrefs:
                continue
            seen_xrefs.add(xref)

            ext, size = _extract_pdf_image_info(doc, xref)
            ext = _normalize_image_ext(ext)
            image_formats[ext] = image_formats.get(ext, 0) + 1
            total_size_bytes += size

        # Check for video/multimedia annotations
        annots = page.annots()
        if annots:
            for annot in annots:
                annot_type = annot.type[1].lower() if annot.type else ""
                if "movie" in annot_type or "screen" in annot_type:
                    videos += 1

    # Count embedded file attachments
    attachments = _count_pdf_attachments(doc)

    images_count = len(seen_xrefs)
    doc.close()

    return {
        "images_count": images_count,
        "images_embedded_base64": images_count,
        "images_referenced_external": 0,
        "image_formats": image_formats,
        "total_media_size_mb": round(total_size_bytes / (1024 * 1024), 2),
        "videos_embedded": videos,
        "attachments_count": attachments,
    }


def _extract_pdf_image_info(doc, xref):
    try:
        img_dict = doc.extract_image(xref)
        ext = img_dict.get("ext", "unknown")
        size = len(img_dict.get("image", b""))
        return ext, size
    except Exception:
        return "unknown", 0


def _count_pdf_attachments(doc):
    count = 0
    try:
        if doc.embfile_count() > 0:
            count = doc.embfile_count()
    except Exception:
        pass
    return count


def _normalize_image_ext(ext):
    ext = ext.lower().strip()
    mapping = {
        "jpg": "jpeg",
        "jpe": "jpeg",
        "tif": "tiff",
        "svgz": "svg",
    }
    return mapping.get(ext, ext)


def _process_docx_image_part(rel, image_formats, total_size_bytes_ref):
    try:
        if hasattr(rel, "target_part"):
            part = rel.target_part
            part_name = str(part.partname).lower()
            ext = part_name.rsplit(".", 1)[-1] if "." in part_name else "unknown"
            ext = _normalize_image_ext(ext)
            image_formats[ext] = image_formats.get(ext, 0) + 1
            if hasattr(part, "blob") and part.blob:
                total_size_bytes_ref[0] += len(part.blob)
    except Exception:
        pass


def get_default():
    """Return the default empty structure for media analysis."""
    return {
        "images_count": 0,
        "images_embedded_base64": 0,
        "images_referenced_external": 0,
        "image_formats": {},
        "total_media_size_mb": 0.0,
        "videos_embedded": 0,
        "attachments_count": 0,
    }
