import os
import tempfile
from typing import Union
from pydantic import BaseModel
from fastapi import UploadFile
from faster_whisper import WhisperModel
import requests
from dotenv import load_dotenv
import together
load_dotenv()

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
TOGETHER_MODEL = "mistralai/Mistral-7B-Instruct-v0.1"
#sorti
class MeetingSummary(BaseModel):
    general_topic_summary: str
    meeting_minutes: list[str]
    discussed_tasks: list[dict]
    postponed_points: list[str]

def transcribe_audio(file: UploadFile) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(file.file.read())
        tmp_path = tmp.name

    model = WhisperModel("base", compute_type="auto")
    segments, _ = model.transcribe(tmp_path)
    transcription = " ".join(segment.text for segment in segments)

    os.remove(tmp_path)
    return transcription

def summarize_meeting_text(text: str) -> dict:
    prompt = f"""
You are an AI assistant for HR. Summarize the following meeting transcript and return structured insights in JSON format with these keys:
- general_topic_summary (string)
- meeting_minutes (list of key discussion points)
- discussed_tasks (list of dicts with task and assigned_to)
- postponed_points (list of items deferred for future meetings)

Transcript:
{text}

Return only the JSON response.
    """

    response = together.Complete.create(
        prompt=prompt,
        model=TOGETHER_MODEL,
        max_tokens=800,
        temperature=0.3,
    )

    # 🔍 Affiche la réponse pour debug
    print("Together AI raw response:", response)

    try:
        import json
        # Essaye d'accéder à l'attribut texte généré
        content = response['choices'][0]['text']
        return json.loads(content)
    except (KeyError, json.JSONDecodeError) as e:
        raise Exception(f"Unexpected Together.ai response format: {e}")
