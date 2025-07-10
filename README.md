# Steps 2 : Document Preparation and Embedding Pipeline

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
# Steps 3: Query Processing and Semantic Search
## FastAPI-based Semantic Search API
- 1. Accepts user question (natural language)
- 2. Embeds it with the same transformer model
- 3. Performs vector similarity search using pgvector

- 4. Returns top-k (default: 5) matching chunks for LLM prompt building

### Commands
- **Run FastAPI for querying:**
````bash
  uvicorn main:app --reload
````
- **Sample Query via cURL**
  ````bash 
    curl -X POST http://localhost:8000/semantic-search \
     -H "Content-Type: application/json" \
     -d '{"question": "What is the policy for paid leave?",
  "top_k": 3}'
  ````
  - **Response:**
   ````bash 
    [
      {
        "file_name":"Leave-Policy-Template-for-Human-Resources.pdf",
         "chunk_index":0,
         "text_chunk":"LEAVE POLICY\nTEMPLATE FOR\nHR\nPROFESSIONALS\nn= 7\nBy\nHRGURUJI\nwww.hrguruji.com\nLEAVE POLICY\nOBJECTIVE\nThe objective of this policy is to regulate all forms of leave that are accrued and due to employees\nas a benefit, and to outline procedures to be followed for the granting and taking of such leave.\nPolicy provisions apply to all employees, that is, permanent employees, temporary employees and\ncasual employees.\nPOLICY\nThe following leave policy procedures will apply:",
        "doc_metadata":null,
        "similarity_score":1.5923
      
     
      }
    ]


  

  


