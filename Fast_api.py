from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from search.search_logic import search_similar_chunks

app = FastAPI()

class QueryInput(BaseModel):
    question: str
    top_k: int = 5

@app.post("/semantic-search")
def semantic_search(query: QueryInput):
    try:
        results = search_similar_chunks(query.question, query.top_k)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
