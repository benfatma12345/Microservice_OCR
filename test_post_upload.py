import requests
import os

# Endpoint de ton microservice Flask
url = "http://127.0.0.1:5000/process-documents"

# Liste de fichiers de test (assure-toi qu'ils existent dans le dossier "hr_documents")
test_files = [
    "hr_documents/hr_policy.docx",
    "hr_documents/Contrat_service.docx",
    "hr_documents/Leave-Policy-Template-for-Human-Resources.pdf",
    "hr_documents/HR-Guide_-Policy-and-Procedure-Template.pdf",
    "hr_documents/Paid-Maternity-Leave-Policy-Template-v3.pdf",
   "hr_documents/parental-leave-toolkit.pdf",

    "hr_documents/Sample-Human Resources Memo.pdf",
    "hr_documents/Valve_NewEmployeeHandbook.pdf",
    
]

headers = {"Accept": "application/json"}

for file_path in test_files:
    if not os.path.exists(file_path):
        print(f"[] Fichier non trouvé : {file_path}")
        continue

    print(f"\n Envoi de : {file_path}")

    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f)}
        try:
            response = requests.post(url, files=files, headers=headers)
            print(f"Status: {response.status_code}")
            print("Réponse JSON:", response.json())
        except Exception as e:
            print(f"Erreur d'envoi : {e}")
