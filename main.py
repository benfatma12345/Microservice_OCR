from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Api.ollama_llm import ask_llm
from search.search_logic import search_similar_chunks  # ton module de recherche

app = FastAPI()

class QueryInput(BaseModel):
    question: str
    top_k: int = 5

@app.post("/ask")
def ask(query: QueryInput):
    try:
        # 1. Recherche de chunks similaires
        chunks = search_similar_chunks(query.question, query.top_k)

        # 2. Construction du contexte
        context = "\n---\n".join(chunk["text_chunk"] for chunk in chunks)

        # 3. Création du prompt
        prompt = f"""Context:
{context}

Question: {query.question}
Answer:"""

        # 4. Appel au LLM
        answer = ask_llm(prompt)

        # 5. Retour de la réponse
        return {
            "answer": answer,
            "context": chunks
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
