#  Microservice OCR avec Flask – Résumé de fonctionnement

## Comment exécuter le microservice

### 1. Installer les dépendances système

- [✅ Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [✅ Poppler pour Windows](https://github.com/oschwartz10612/poppler-windows/releases)

 **Assurez-vous que** :
- `tesseract.exe` et `pdftoppm.exe` sont dans votre `PATH` système.
- Test rapide :
  ```bash
  tesseract --version
  pdftoppm -v
  ```
### 2. Installer les dépendances Python
```bash
pip install flask pytesseract pdf2image pillow
```
### 3. Lancer le service
```bash
python app.py
```
Par défaut, le service s’exécute sur :
```bash
http://localhost:5000/upload-form
```

## Microservice OCR avec Flask – Phase 1

###  Objectif  
Créer un microservice web capable de :
- recevoir des fichiers (images ou PDF),
- extraire le texte via OCR (Tesseract),
- retourner ce texte accompagné de métadonnées dans une réponse JSON.

###  Contexte  
Ce microservice servira de **composant de base** dans un système **RAG** (Retrieval Augmented Generation), pour **extraire automatiquement le contenu textuel** des documents.

### Technologies utilisées
- Python 3.x  
- Flask *(framework web)*  
- `pytesseract` *(wrapper Python de Tesseract OCR)*  
- `pdf2image` *(conversion PDF → images)*  
- `Pillow` *(traitement d’images)*  
- **Tesseract OCR** *(moteur OCR open source)*  
- **Poppler** *(outil système pour manipuler les PDF)*
  
### Architectur
```mermaid
flowchart TD
    Client["Client\n(Envoi fichiers POST /upload)"]
    Flask["Flask Microservice"]
    Save["Sauvegarde temporaire locale"]
    CheckType["Détection type fichier"]
    ImageProcess["OCR Tesseract\n(sur image)"]
    PDFConvert["Conversion PDF → Images\n(pdf2image)"]
    PDFOCR["OCR Tesseract\n(sur chaque image)"]
    ConcatText["Concaténation texte OCR"]
    JSONResp["Réponse JSON\n(liste d’objets)"]

    Client -->|POST /upload| Flask
    Flask --> Save
    Save --> CheckType
    CheckType -->|Image| ImageProcess
    CheckType -->|PDF| PDFConvert
    PDFConvert --> PDFOCR
    ImageProcess --> ConcatText
    PDFOCR --> ConcatText
    ConcatText --> JSONResp
````

###  Upload et sauvegarde

- Récupération des fichiers via `request.files` (clé `files`).  
- Sauvegarde temporaire locale (ex : `/tmp`).  

###  Type et métadonnées

- Détection du type MIME (`image/png`, `application/pdf`) avec `mimetypes`.  
- Taille extraite via `os.stat`.  
- Chemin temporaire utilisé pour le traitement.  

###  Extraction OCR

- Si image → Tesseract appliqué directement.  
- Si PDF → conversion des pages en images via `pdf2image.convert_from_path`.  
- Tesseract appliqué à chaque image.  
- Texte concaténé.  
- Nombre de pages déterminé automatiquement.

---


###  Exemple de réponse JSON
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





