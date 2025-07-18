import together
import os
from dotenv import load_dotenv

load_dotenv()

# Configure API key (pas besoin de requests)
together.api_key = os.getenv("TOGETHER_API_KEY")

TOGETHER_MODEL = "mistralai/Mistral-7B-Instruct-v0.1"

def ask_llm(prompt: str) -> str:
    response = together.chat.completions.create(
        model=TOGETHER_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful HR assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=512,
        temperature=0.7
    )

    return response.choices[0].message.content
