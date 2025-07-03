import requests
import os

TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY") 
def classify_text_with_llm(text):
    endpoint = "https://api.together.xyz/inference"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "Bearer 8a554229205fea94afbaf2c300743e05b1fba2338d0c769b6dbefb0945fb0be2"
    }

    prompt = f"""
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
\"\"\"{text[:3000]}\"\"\"
"""

    body = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "prompt": prompt,
        "max_tokens": 10,
        "temperature": 0.3,
        "top_p": 0.9,
    }

    response = requests.post(endpoint, headers=headers, json=body)

    if response.status_code == 200:
        try:
            data = response.json()
            raw_output = data.get("choices", [{}])[0].get("text", "").strip().lower()
            print("LLM output brut:", repr(raw_output))

            # Extraction robuste avec regex
            import re
            categories = {"resume", "contract", "invoice", "academic paper", "letter", "policy", "report"}

            for category in categories:
                if re.search(rf"\b{re.escape(category)}\b", raw_output):
                    return category

            return "unknown"
        except Exception as e:
            print("Erreur parsing LLM:", e)
            return "unknown"
    else:
        print("Erreur LLM:", response.status_code, response.text)
        return "unknown"