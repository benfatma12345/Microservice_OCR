from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from typing import List

from db.db import init_db, SessionLocal
from models.db_models import ConversationMemory
from search.search_logic import search_similar_chunks
from Api.together_llm import ask_llm

import uvicorn

# Charger variables d’environnement
load_dotenv()

# Initialiser DB
init_db()

# Créer app FastAPI
app = FastAPI(
    title="Purpella RAG API",
    description="API de RAG avec mémoire multi-tours pour l’assistante RH Purpella.",
    version="1.0.0"
)

# Dépendance de session SQLAlchemy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------  MODELES Pydantic ----------
class QueryInput(BaseModel):
    session_id: str
    question: str
    top_k: int = 5

class AskResponse(BaseModel):
    answer: str
    context: List[dict]

class ResetResponse(BaseModel):
    message: str

# ----------  ENDPOINT /ask ----------
@app.post("/ask", response_model=AskResponse, tags=["Conversation"])
def ask_purpella(query: QueryInput, db: Session = Depends(get_db)):
    try:
        # 1. Récupérer les 3 derniers Q&A
        history = db.query(ConversationMemory)\
            .filter(ConversationMemory.session_id == query.session_id)\
            .order_by(ConversationMemory.turn_number.desc())\
            .limit(3)\
            .all()[::-1]

        history_text = ""
        for turn in history:
            history_text += f"User: {turn.question}\nPurpella: {turn.answer}\n\n"

        # 2. Récupérer chunks de documents
        chunks = search_similar_chunks(query.question, query.top_k)
        context_text = "\n- " + "\n- ".join(chunk["text_chunk"] for chunk in chunks)

        # 3. Créer prompt
        prompt = f"""You are Purpella, a helpful and professional HR assistant.

This is a conversation between an employee and Purpella. Use the previous turns to understand the context and answer naturally and clearly.

Conversation history:
{history_text}Relevant document context:{context_text}

Current question:
User: {query.question}

Purpella:"""

        # 4. Obtenir réponse LLM
        answer = ask_llm(prompt)

        # 5. Sauvegarder la réponse dans la mémoire
        max_turn = db.query(ConversationMemory.turn_number)\
            .filter(ConversationMemory.session_id == query.session_id)\
            .order_by(ConversationMemory.turn_number.desc())\
            .first()
        next_turn = (max_turn[0] + 1) if max_turn else 1

        memory = ConversationMemory(
            session_id=query.session_id,
            turn_number=next_turn,
            question=query.question,
            answer=answer
        )
        db.add(memory)
        db.commit()

        return {
            "answer": answer,
            "context": chunks
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----------  ENDPOINT /reset_session ----------
@app.delete("/reset_session/{session_id}", response_model=ResetResponse, tags=["Conversation"])
def reset_session(session_id: str, db: Session = Depends(get_db)):
    try:
        deleted = db.query(ConversationMemory).filter(ConversationMemory.session_id == session_id).delete()
        db.commit()
        return {"message": f"Session '{session_id}' reset successfully. ({deleted} turns deleted)"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----------  LANCEMENT ----------
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
