import os
import mimetypes
import pytesseract
from pdf2image import convert_from_path
from docx import Document as DocxDocument

def get_file_metadata(file_path):
    stat = os.stat(file_path)
    mime, _ = mimetypes.guess_type(file_path)
    return {
        "file_type": mime,
        "file_size": stat.st_size
    }
def extract_text_from_docx(file_path):
    doc = DocxDocument(file_path)
    return "\n".join(p.text for p in doc.paragraphs if p.text)

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)


def extract_text(file_path):
    file_type = get_file_metadata(file_path)["file_type"]

    if file_type and 'pdf' in file_type:
        images = convert_from_path(file_path, poppler_path=r"C:\Users\wsi\poppler-24.08.0\Library\bin")
        return "\n".join(pytesseract.image_to_string(img) for img in images)

    elif file_type and 'msword' in file_type:
        # Type for .doc (very old Word files, optional)
        return extract_text_from_docx(file_path)

    elif file_type and 'text' in file_type:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    elif "vnd.openxmlformats-officedocument.wordprocessingml.document" in file_type:
        return extract_text_from_docx(file_path)

    elif "image" in file_type:
        return extract_text_from_image(file_path)

    else:
        raise ValueError(f"Unsupported file type: {file_type}")