import os
import mimetypes
import pytesseract
from pdf2image import convert_from_path
from docx import Document as DocxDocument
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


def extract_text(file_path):
    mime, _ = mimetypes.guess_type(file_path)

    if mime and 'pdf' in mime:
        images = convert_from_path(file_path, poppler_path=r"C:\Users\wsi\poppler-24.08.0\Library\bin")
        return "\n".join(pytesseract.image_to_string(img) for img in images)

    elif mime == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = DocxDocument(file_path)
        return "\n".join(p.text for p in doc.paragraphs if p.text)

    elif "image" in mime:
        return pytesseract.image_to_string(Image.open(file_path))

    elif "text" in mime:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    raise ValueError(f"Unsupported file type: {mime}")