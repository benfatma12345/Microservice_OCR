#import requests
import together
import os
import re
#OGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY") 
together.api_key = "8a554229205fea94afbaf2c300743e05b1fba2338d0c769b6dbefb0945fb0be2"
"""
def classify_text_with_llm(text):
    endpoint = "https://api.together.xyz/inference"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "Bearer 8a554229205fea94afbaf2c300743e05b1fba2338d0c769b6dbefb0945fb0be2"
    }

    prompt = f
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

""" body = {
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
        """
def count_tokens(text: str) -> int:
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except ImportError:
        return len(text) // 4

def classify_text_with_llm(text: str, model: str) -> str:
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

    try:
        response = together.Complete.create(
            model=model,
            prompt=prompt,
            max_tokens=10,
            temperature=0.3,
            top_p=0.9
        )
        if 'output' in response:
            raw_output = response['output']['choices'][0]['text'].strip().lower()
        elif 'choices' in response:
            raw_output = response['choices'][0]['text'].strip().lower()
        else:
            print("Réponse API Together inattendue :", response)
            return "unknown"

        categories = {"resume", "contract", "invoice", "academic paper", "letter", "policy", "report"}
        for category in categories:
            if re.search(rf"\b{re.escape(category)}\b", raw_output):
                return category
        return "unknown"
    except Exception as e:
        print(f"Erreur API Together: {e}")
        return "unknown"