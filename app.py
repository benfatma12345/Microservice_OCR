from flask import Flask, request, jsonify, render_template_string
import tempfile
import webbrowser
import os
from utils import ocr_image, process_pdf, get_file_metadata

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    files = request.files.getlist("files")
    results = []

    for file in files:
        ext = os.path.splitext(file.filename)[1]  # extension originale
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
        file.save(temp_file.name)
        file_path = temp_file.name
        file_name = file.filename

        metadata = get_file_metadata(file_path)
        file_type = metadata['file_type']

        if file_type and 'pdf' in file_type:
            text, num_pages = process_pdf(file_path)
        elif file_type and 'image' in file_type:
            text = ocr_image(file_path)
            num_pages = 1
        else:
            return jsonify({"error": f"Unsupported file type: {file_type}"}), 400

        result = {
            "file_name": file_name,
            "file_path": file_path,
            "file_size": metadata["file_size"],
            "file_type": file_type,
            "extracted_text": text,
            "number_of_pages": num_pages
        }
        results.append(result)

    return jsonify(results)

@app.route('/upload-form')
def upload_form():
    return render_template_string("""
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>OCR File Upload</title>
    </head>
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
