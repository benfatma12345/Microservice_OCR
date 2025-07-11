from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Api.together_llm import ask_llm   # ← Use Together API
from search.search_logic import search_similar_chunks

app = FastAPI()

class QueryInput(BaseModel):
    question: str
    top_k: int = 5

@app.post("/ask")
def ask(query: QueryInput):
    try:
        chunks = search_similar_chunks(query.question, query.top_k)
        context = "\n---\n".join(chunk["text_chunk"] for chunk in chunks)

        prompt = f"""Context:
{context}

Question: {query.question}
Answer:"""

        answer = ask_llm(prompt)
        return {"answer": answer, "context": chunks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
