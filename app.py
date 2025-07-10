from flask import Flask, request, jsonify, render_template_string
import tempfile
import webbrowser
import os
from db import init_db, Session
from db_models import DocumentChunk
from utils.document_utils import extract_text, get_file_metadata
from utils.embedding_utils import split_text, generate_embeddings

app = Flask(__name__)
init_db()

@app.route('/process-documents', methods=['POST'])
def process_documents():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    uploaded_file = request.files['file']
    filename = uploaded_file.filename
    file_path = os.path.join(tempfile.gettempdir(), filename)
    uploaded_file.save(file_path)

    try:
        text = extract_text(file_path)
        chunks = split_text(text)
        embeddings = generate_embeddings(chunks)
        metadata = get_file_metadata(file_path)

        session = Session()
        for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
            doc = DocumentChunk(
                file_name=filename,
                chunk_index=i,
                text_chunk=chunk,
                embedding=emb,
                doc_metadata=metadata 
            )
            session.add(doc)
        session.commit()
        session.close()

        return jsonify({
            "file": filename,
            "chunks": len(chunks),
            "status": "success"
        })

    except Exception as e:
        return jsonify({
            "file": filename,
            "error": str(e),
            "status": "failed"
        }), 500


if __name__ == '__main__':
    app.run(debug=True)
