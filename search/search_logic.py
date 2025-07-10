from sqlalchemy import text
from db import engine 
from utils.embedding_utils import model as embedding_model
from sentence_transformers import SentenceTransformer





def search_similar_chunks(question: str, top_k: int = 5):
    question_embedding = embedding_model.encode(question).tolist()
    question_embedding_str = f"[{', '.join(map(str, question_embedding))}]"

    # on injecte embedding directement dans la requête
    sql = f"""
        SELECT 
            file_name,
            chunk_index,
            text_chunk,
            doc_metadata,
            1 - (embedding <#> '{question_embedding_str}'::vector) AS similarity
        FROM document_chunks
        ORDER BY embedding <#> '{question_embedding_str}'::vector
        LIMIT {top_k}
    """

    with engine.connect() as conn:
        result = conn.execute(text(sql))
        rows = result.fetchall()

    return [
        {
            "file_name": row.file_name,
            "chunk_index": row.chunk_index,
            "text_chunk": row.text_chunk,
            "doc_metadata": row.doc_metadata,
            "similarity_score": round(row.similarity, 4)
        }
        for row in rows
    ]
