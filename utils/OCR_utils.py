import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os
import tempfile
import mimetypes

def ocr_image(image_path):
    text = pytesseract.image_to_string(Image.open(image_path))
    return text

def process_pdf(file_path):
    poppler_path = r"C:\Users\wsi\poppler-24.08.0\Library\bin"  
    images = convert_from_path(file_path, poppler_path=poppler_path)
    all_text = ''

    for image in images:
        all_text += pytesseract.image_to_string(image)

    return all_text, len(images)


def get_file_metadata(file_path):
    file_stat = os.stat(file_path)
    # Forcer l'extension en minuscule pour la détection mime
    ext = os.path.splitext(file_path)[1].lower()
    # Simuler un nom de fichier avec l'extension en minuscule pour guess_type
    fake_file = "file" + ext
    file_type, _ = mimetypes.guess_type(fake_file)
    return {
        "file_path": file_path,
        "file_size": file_stat.st_size,
        "file_type": file_type
    }
