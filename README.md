# OCR Microservice with Flask – Summary of Functionality

## How to run the microservice

### 1. Install system dependencies

- [✅ Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [✅ Poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases)

**Make sure that**:  
- `tesseract.exe` and `pdftoppm.exe` are in your system `PATH`.  
- Quick test:
  ```bash
  tesseract --version
  pdftoppm -v

### 2.  Install Python dependencies
```bash
pip install flask pytesseract pdf2image pillow
pip install -r requirements.txt
```
### 3.Set Together.ai API key
```bash
set TOGETHER_API_KEY=your_api
````
### 4.Start the service
```bash
python app.py
```
By default, the service runs at:
```bash
http://localhost:5000/upload-form
```

## A working Flask microservice with

###  Objective  
Create a web microservice capable of:

- receiving files (images or PDFs),

- extracting text via OCR (Tesseract),

- returning the extracted text along with metadata in a JSON response.

###  Contexte  
This microservice will serve as a core component in a **RAG (Retrieval Augmented Generation)** system to automatically extract the textual content from documents.

### Technologies used
- Python 3.x  
- Flask *(framework web)*  
- `pytesseract` *(Python wrapper for Tesseract OCR)*  
- `pdf2image` *(PDF to images conversion)*  
- `Pillow` *(image processing)*  
- **Tesseract OCR** *(open-source OCR engine)*  
- **Poppler** *(system tool for PDF manipulation)*
  

###  Upload and save

- Retrieve files via `request.files` (key `files`).  
- Temporarily save locally  (e.g : `/tmp`).  

###  File type and metadata

- Detect MIME type (`image/png`, `application/pdf`) using `mimetypes`.  
- Extract file size using `os.stat`.  
- Use temporary file path for processing..  

###  OCR extraction

- If image → apply Tesseract directly.
- If PDF → convert pages to images via `pdf2image.convert_from_path`.  
- Apply Tesseract OCR on each image.

- Concatenate extracted text.

- Automatically determine number of pages.

---


###  Example JSON response
```json
[
  {
    "extracted_text": "Nom : Wafa Ben Fatma\nProjet : Microservice OCR\nDate : @2 Juillet 2025\n\nCe fichier contient un exemple de texte clair\npour tester 1\u2019extraction OCR avec Tesseract.\n",
    "file_name": "Test.png",
    "file_path": "C:\\Users\\wsi\\AppData\\Local\\Temp\\tmpvf0_wieu.png",
    "file_size": 5927,
    "file_type": "image/png",
    "number_of_pages": 1
  }
]
````
# Logic to classify documents using Together.ai’s LLM

## Overview

After extracting text from the uploaded document via OCR or PDF processing, the service sends the extracted text to Together.ai’s large language model (LLM) for automatic document classification.

## How it works

### Prepare the prompt

The extracted text is inserted into a prompt asking the model to classify it into exactly one of the predefined categories:

```text
You are a professional document classifier.

Classify the following text into exactly one of the following categories:
- resume
- contract
- invoice
- academic paper
- letter
- policy
- report

Respond ONLY with the category name (e.g. "contract").

Text:
"""
[extracted text here]
"""
````
### Send API request
Créer un microservice web capable de :
- **URL**: https://api.together.xyz/inference ,
- **Method**: POST,
- **Headers**:
   - Authorization: Bearer <TOGETHER_API_KEY>
   - Content-Type: application/json
- **Body parameters:**
   - model: "mistralai/Mixtral-8x7B-Instruct-v0.1"
   - prompt: the prompt above with inserted text
   - max_tokens: 10
   - top_p: 0.9
   - temperature: 0.3
### Process response
The LLM responds with text containing the predicted category. The service extracts the category by:

- Parsing the JSON response.

- Extracting the generated text.

- Matching it against the known categories (resume, contract, invoice, academic paper, letter, policy, report).

- Returning the matched category or "unknown" if no match found.


  
  



## OCR & LLM Classification Architecture
```mermaid
flowchart TD
    Client["Client\n(Uploads files via POST /upload)"]
    Flask["Flask Microservice"]
    Save["Temporary local save"]
    CheckType["Detect file type"]
    ImageProcess["Tesseract OCR\n(on image)"]
    PDFConvert["PDF → Images conversion\n(pdf2image)"]
    PDFOCR["Tesseract OCR\n(on each image)"]
    ConcatText["Concatenate OCR text"]
    Classify["Classification via\nTogether.ai LLM API"]
    JSONResp["JSON response\n(list of objects)"]

    Client -->|POST /upload| Flask
    Flask --> Save
    Save --> CheckType
    CheckType -->|Image| ImageProcess
    CheckType -->|PDF| PDFConvert
    PDFConvert --> PDFOCR
    ImageProcess --> ConcatText
    PDFOCR --> ConcatText
    ConcatText --> Classify
    Classify --> JSONResp

````
**Brief explanation:**
- After extracting OCR text (ConcatText), the text is sent to the Classify component that calls the Together.ai API to classify the document.
- The classification result is then included in the final JSON response.










