# File: Api/together_llm.py

import requests
import os
from dotenv import load_dotenv
load_dotenv()

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")  
TOGETHER_MODEL = "mistralai/Mistral-7B-Instruct-v0.1"

def ask_llm(prompt: str) -> str:
    url = "https://api.together.xyz/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": TOGETHER_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful HR assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 512,
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"Together API error: {response.text}")

    return response.json()["choices"][0]["message"]["content"]
