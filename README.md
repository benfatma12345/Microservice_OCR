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
- **Create the table:**
  ````bash 
   CREATE TABLE document_chunks (
     id SERIAL PRIMARY KEY,
     file_name VARCHAR,
     chunk_index INTEGER,
     text_chunk TEXT,
     embedding VECTOR(384),
    doc_metadata JSONB  
    );
    ````
- **Environment Configuration**:
  
  Create a **.env** file:
  ````bash
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=postgres
   DB_USER=postgres
   DB_PASSWORD=root
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
         "text_chunk":"LEAVE POLICY\nTEMPLATE FOR\nHR\nPROFESSIONALS\nn= 7\nBy\nHRGURUJI\nwww....taking of such leave.\nPolicy provisions apply to all employees, that is, permanent employees, temporary employees and\ncasual employees.",
        "doc_metadata":null,
        "similarity_score":1.5923
      }
    ]
    ````

 # Step 4: Prompting + Answer Generation with Together.ai

- Sign up at https://together.ai
- Go to your account settings

- Get your API Key (free tier gives you limited usage).

- Install HTTP client library if needed
````bash 
pip install requests
````
- **Run FastAPI for querying:**
````bash
  uvicorn main:app --reload
````
- **Sample Query via cURL**
````bash 
     POST http://localhost:8000/semantic-search \
     "Content-Type: application/json" \
     '{"question": "What is the policy for paid leave?",
  "top_k": 2}'
````
-   **Response:**
   ````bash 
step 4
{"answer":"Employees who are away from the office and who are being treated in an institution for the rehabilitation of alcoholism, or drug addiction may be granted sick leave for the period that they are away, provided that a sufficient number of days sick leave are available to the employee.","context":                                      [
  [
    {"file_name":"Leave-Policy-Template-for-Human-Resources.pdf", 
    "chunk_index":23,
    "text_chunk":"(6) Should an employee become ill whilst on annual leave, such portion of their vacation leave\nmay, ....",
    "doc_metadata":null,"similarity_score":1.696},
    
   {"file_name":"Leave-Policy-Template-for-Human-Resources.pdf","chunk_index":23,
   "text_chunk":"(6) Should an employee become ill whilst on annual leave, such portion of their vacation leave\nmay, subject to the submissio ...leave are available to the","doc_metadata":{"file_type":"application/pdf","file_size":374786},"similarity_score":1.696}
   ]
  } 
````

# Step 5: Unified FastAPI Endpoint /ask
- Full Endpoint Code :
````bash 
  @app.post("/ask")
def ask(query: QueryInput):
    chunks = search_similar_chunks(query.question, query.top_k)
    context = "\n---\n".join(chunk["text_chunk"] for chunk in chunks)
    prompt = f"Context:\n{context}\n\nQuestion: {query.question}\nAnswer:"
    answer = ask_llm(prompt)
    return {"answer": answer, "context": chunks}
````
- ### Test Scripts Summary

| Script             | Purpose                                      |
|--------------------|----------------------------------------------|
| `test_post_upload.py` | Upload documents, extract text, embed content, and insert into PostgreSQL |
| `main.py` (FastAPI)   | Answer user questions via the `/ask` route (RAG pipeline entry point) |
| `together_llm.py`       | Handles API call to Together.ai for open-source LLM (e.g., Mistral) |
| `search_logic.py`     | Performs semantic similarity search in PostgreSQL using `pgvector` |

##  Run Order — How to Test the Full RAG System

Follow these steps to test the system end-to-end:

---

###  1. Start PostgreSQL and Enable `pgvector`

Ensure your PostgreSQL server is running and the `pgvector` extension is enabled:

```sql
-- Inside psql
CREATE EXTENSION IF NOT EXISTS vector;
````
### 2. Launch the Flask Document Ingestion Microservice

Run your Flask service to enable document upload and processing:

```bash
python app_flask.py
````
This will start the document ingestion microservice, which:

- Accepts file uploads (PDF, DOCX, images)

- Extracts text (with OCR if needed)

- Splits into chunks

- Embeds text with MiniLM

- Stores in PostgreSQL with pgvector
### 3. Run the Test Uploader
This script sends multiple HR documents to the ingestion endpoint for processing:

````bash
python test_post_upload.py
````
It performs:

- Upload of .docx, .pdf, and .png files from a folder like hr_documents/

- Text extraction + embedding

- Insertion into document_chunks table in PostgreSQL
### 4. Launch FastAPI for Querying

Start your FastAPI server to handle semantic search and question-answering:

```bash
uvicorn main:app --reload
````
This will launch the API server at:
````bash
http://127.0.0.1:8000
````
Once started, the /ask endpoint will be available for queries.
### 5. Ask Questions via Postman 

- **Sample Query via cURL**
````bash 
     POST http://localhost:8000/ask
     "Content-Type: application/json" \
     {"question": "What is the maternity   leave policy?",
      "top_k": 5
}

````
-   **Response:**
````bash
 {
    "answer": "The maternity leave policy is as follows:\nAn employee who gives birth shall be entitled to maternity leave of twelve (12) weeks\ncommencing from the date of confinement. The employee may take additional leave, in\naccordance with the terms of this agreement.",
    "context": [
        {
            "file_name": "hr_policy.pdf",
            "chunk_index": 13,
            "text_chunk": "confinements or adoptions. This leave provision shall also applyto an employee whose\nchild still-born.\nOnce an employee has given birth, she can return and commence duties if a doctor certifies\nthat she is fit to commence normal duties after a period of six (6) weeks after birth;\nSecurity of employment is protected during the period of maternity leave;\nMaternity leave must in all cases be uninterrupted and continuous with theconfinement. It",
            "doc_metadata": null,
            "similarity_score": 1.6837
        },
        {
            "file_name": "Leave-Policy-Template-for-Human-Resources.pdf",
            "chunk_index": 13,
            "text_chunk": "confinements or adoptions. This leave provision shall also applyto an employee whose\nchild still-born.\nOnce an employee has given birth, she can return and commence duties if a doctor certifies\nthat she is fit to commence normal duties after a period of six (6) weeks after birth;\nSecurity of employment is protected during the period of maternity leave;\nMaternity leave must in all cases be uninterrupted and continuous with theconfinement. It",
            "doc_metadata": null,
            "similarity_score": 1.6837
        },
        {
            "file_name": "Leave-Policy-Template-for-Human-Resources.pdf",
            "chunk_index": 13,
            "text_chunk": "confinements or adoptions. This leave provision shall also applyto an employee whose\nchild still-born.\nOnce an employee has given birth, she can return and commence duties if a doctor certifies\nthat she is fit to commence normal duties after a period of six (6) weeks after birth;\nSecurity of employment is protected during the period of maternity leave;\nMaternity leave must in all cases be uninterrupted and continuous with theconfinement. It",
            "doc_metadata": {
                "file_type": "application/pdf",
                "file_size": 374786
            },
            "similarity_score": 1.6837
        },
        {
            "file_name": "Leave-Policy-Template-for-Human-Resources.pdf",
            "chunk_index": 13,
            "text_chunk": "confinements or adoptions. This leave provision shall also applyto an employee whose\nchild still-born.\nOnce an employee has given birth, she can return and commence duties if a doctor certifies\nthat she is fit to commence normal duties after a period of six (6) weeks after birth;\nSecurity of employment is protected during the period of maternity leave;\nMaternity leave must in all cases be uninterrupted and continuous with theconfinement. It",
            "doc_metadata": {
                "file_type": "application/pdf",
                "file_size": 374786
            },
            "similarity_score": 1.6837
        },
        {
            "file_name": "hr_policy.pdf",
            "chunk_index": 15,
            "text_chunk": "immediately prior to any of the said incidents, should not be taken into account for\npurposes of the restriction above;\nDuring the period of maternity leave normal annual leave benefits do not accrue;\nMaternity leave should be applied for at least four (4) weeks in advance to allow adequate\nplanning for the employee’s absence;\nBefore leaving to go on maternity leave the employees shall enter into an agreement with\nXYZ, stating that the individual will return to work after their confinement.",
            "doc_metadata": null,
            "similarity_score": 1.6674
        }
    ]
}
```` 
## Step 6: Implementation of Multi-turn Dialogue Memory in the RAG System

### 1. Objective
Allow Purpella to handle follow-up questions by keeping track of the last 3 Q&A turns **per user session**. This makes conversations more natural and context-aware.


### 2. Database Schema for Memory
```sql
CREATE TABLE conversation_memory (
    id SERIAL PRIMARY KEY,
    session_id TEXT NOT NULL,
    turn_number INTEGER NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT NOW()
);
````
### 3. FastAPI Endpoint Update /ask
- Accept session_id in request.

- Fetch last 3 Q&A pairs from conversation_memory by session_id.

- Format them into the "Conversation history" section.

- Generate prompt and call LLM.

- Save current turn into conversation_memory.
### 4. Ask Questions via Postman 

   - POST /ask
  
````bash 
     POST http://localhost:8000/ask
     "Content-Type: application/json" \
     {
       "session_id": "abc123",
        "question": "What is the annual   leave policy?",
       "top_k": 3
}


````
   - **Response:**
````bash
{
    {"answer":" Our Foundation offers comprehensive vacation time policies for both part-time and full-time employees, as well as other forms of leave as needed. Part-time employees are entitled to one day per month in lieu of vacation pay and a minimum of two weeks of vacation time. Full-time employees are entitled to a minimum of four weeks of paid vacation time per year, as well as other forms of leave such as sick leave, personal leave, parental leave, and compassionate care leave. Our annual leave policy is designed to ensure that employees have access to the time and resources they need to maintain their health, well-being, and job performance. If you have any questions or concerns about your vacation time entitlements or our leave policy, please don't hesitate to contact me for further information.","context":[{"file_name":"Valve_NewEmployeeHandbook.pdf","chunk_index":108,"text_chunk":"Doesn’t Work?\nSometimes, the philosophy and methods outlined in this\nbook don’t match perfectly with how things are going day\nto day. But we’re confident that even when problems persist\nfor a while, Valve roots them out.\nAs you see it, are there areas of the company in which\nthe ideals in this book are realized more fully than others?\nWhat should we do about that? Are those differences a\ngood thing? What would you change? This handbook\ndescribes the goals we believe in. If you find yourself in","doc_metadata":{"file_type":"application/pdf","file_size":26380552},"similarity_score":1.2708}],"prompt":"You are Purpella, a helpful and professional HR assistant.\n\nThis is a conversation between an employee and Purpella. Use the previous turns to understand the context and answer naturally and clearly.\n\nConversation history:\nUser: What about part-time employees?\nPurpella:  As a part-time employee, you are entitled to one day per month in lieu of 4% vacation pay. The day is equivalent to the normal number of hours regularly worked by you. Additionally, you are required to take a minimum of two weeks of vacation time, either paid or unpaid. Is there anything else you would like to know about vacation time for part-time employees?\n\nUser:  Does that include public holidays?\nPurpella:  Yes, our Foundation observes the following paid holidays, as per our policy and procedure statement:\n\n* New Year's Day\n* Good Friday\n* Easter Monday\n* Victoria Day\n* Canada Day\n* Civic Holiday\n* Labour Day\n* Thanksgiving Day\n* Christmas Day\n* Boxing Day\n\nIf you are a part-time employee not scheduled to work on a public holiday, you will not receive holiday pay in accordance with the Employment Standards Act.\n\nPlease let me know if you have any other questions or concerns about vacation time for part-time employees.\n\nUser: What is the annual leave policy for full-time employees?\nPurpella:  Our Foundation offers a comprehensive leave policy for full-time employees, which is designed to provide employees with adequate time off to rest, recharge, and balance their work and personal lives.\n\nUnder our annual leave policy, full-time employees are entitled to a minimum of 4 weeks of paid vacation time per year, in addition to any other forms of leave that may be available to them. This time can be taken in one continuous block, or it can be broken up into shorter intervals throughout the year.\n\nIn addition to vacation time, full-time employees may be eligible for other forms of leave, such as sick leave, personal leave, parental leave, and compassionate care leave, depending on their individual circumstances and needs.\n\nTo use vacation time, full-time employees must provide at least 2 weeks' notice to their supervisor, and may be required to complete any outstanding work or cover their absence during their time off.\n\nEmployees who wish to take time off for non-vacation purposes, such as personal or family matters, may be eligible for personal leave under our leave policy. To request personal leave, employees must provide at least 2 weeks' notice to their supervisor and provide supporting documentation.\n\nOverall, our annual leave policy is designed to ensure that full-time employees have access to the time and resources they need to maintain their health, well-being, and job performance. If you have any questions or concerns about your annual leave entitlements or our leave policy, please do not hesitate to contact me for further information.\n\nRelevant document context:\n- Doesn’t Work?\nSometimes, the philosophy and methods outlined in this\nbook don’t match perfectly with how things are going day\nto day. But we’re confident that even when problems persist\nfor a while, Valve roots them out.\nAs you see it, are there areas of the company in which\nthe ideals in this book are realized more fully than others?\nWhat should we do about that? Are those differences a\ngood thing? What would you change? This handbook\ndescribes the goals we believe in. If you find yourself in\n\nCurrent question:\nUser: Can you summarize it all in one paragraph?\n\nPurpella:"}
}
```` 
   - **DELETE /reset_session/{session_id}**
````bash 
     DELETE http://localhost:8000/reset_session/abc123
    

````
-   **Response:**
````bash
 {
    "message": "Session 'abc123' reset successfully. (1 turns deleted)"
}
````
### 5. Ask Questions via Swagger UI

Disponible automatiquement à :
**http://localhost:8000/docs**

