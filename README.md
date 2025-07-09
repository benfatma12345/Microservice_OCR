# Document Preparation and Embedding Pipeline

## Detailed Steps

### 1. Text Extraction

- **Supported formats:**  
  - PDF (scanned or native)  
  - Images (jpeg, png, etc.)  
  - Word documents (.docx)

- **Methods used:**  
  - Native PDFs: direct text extraction (if possible)  
  - Scanned PDFs & images: convert to images + OCR using `pytesseract`  
  - Word documents: reading via the `python-docx` library

### 2. Chunking (segmenting)

- Limit the text size to match embedding and LLM model capacities.  
- Typical method: chunk by max number of tokens (~500 tokens per chunk).

### 3. Embedding Generation

- **Model used:** `sentence-transformers/all-MiniLM-L6-v2`

- **Installation:**
```bash
pip install sentence-transformers
````
- **Example of generation:**
```bash
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
```

### 4. Storage in PostgreSQL with pgvector
- **PostgreSQL + pgvector extension installation:**
````bash
#Dans psql
CREATE EXTENSION IF NOT EXISTS vector;

````
- **SQL table:**
````bash
CREATE TABLE document_chunks (
    id SERIAL PRIMARY KEY,
    file_name VARCHAR,
    chunk_index INTEGER,
    text_chunk TEXT,
    embedding VECTOR(384),
    metadata JSONB
);
`````
- **SQLAlchemy model:**
    - SQLAlchemy is an ORM (**Object Relational Mapper**) in Python that allows you to manipulate a relational database using Python classes.
A **SQLAlchemy** model corresponds to a Python class linked to a SQL table.
     
## Useful Commands
- **Install dependencies:**
  
  ````bash
  pip install -r requirements.txt`
  ````
- **Create pgvector extension in PostgreSQL (psql):**
   ````bash
   CREATE EXTENSION IF NOT EXISTS vector;
   ````
- **Run Flask microservice:**
   ````
    python app.py
   ````
- **Run the test script:**
  ```` 
  python test_post_upload.py
  ````



  

  


