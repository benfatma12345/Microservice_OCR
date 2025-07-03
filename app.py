from flask import Flask, request, jsonify, render_template_string
import tempfile
import webbrowser
import os
from utils.OCR_utils import ocr_image, process_pdf, get_file_metadata
from utils.LLM_utils import classify_text_with_llm

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    files = request.files.getlist("files")
    results = []

    for file in files:
        # 1. Sauvegarde temporaire
        ext = os.path.splitext(file.filename)[1]
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
        file.save(temp_file.name)
        file_path = temp_file.name
        file_name = file.filename

        # 2. Métadonnées
        metadata = get_file_metadata(file_path)
        file_type = metadata['file_type']

   
        if file_type and 'pdf' in file_type:
             text, number_of_pages = process_pdf(file_path)
        elif file_type and 'image' in file_type:
             text = ocr_image(file_path)

             
 
        else:
            return jsonify({"error": f"Unsupported file type: {file_type}"}), 400


        file_class = classify_text_with_llm(text)

        # 5. Résultat
        result = {
            "file_name": file_name,
            "file_path": file_path,
            "file_size": metadata["file_size"],
            "file_type": file_type,
            "extracted_text": text,
            "number_of_pages": number_of_pages,
            "file_class": file_class
        }
        results.append(result)

    return jsonify(results)


@app.route('/upload-form')
def upload_form():
    return render_template_string("""
    <!doctype html>
    <html lang="en">
    <head><meta charset="UTF-8"><title>OCR File Upload</title></head>
    <body>
      <h1>Upload an image or PDF</h1>
      <form method="post" enctype="multipart/form-data" action="/upload">
        <input type="file" name="files" multiple><br><br>
        <input type="submit" value="Upload and Extract Text">
      </form>
    </body>
    </html>
    """)


if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5000/upload-form")
    app.run(debug=True)
