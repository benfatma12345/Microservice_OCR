from sqlalchemy import text
from db.init_db import engine
from utils.embedding_utils import model

def search_similar_chunks(question: str, top_k: int = 5):
    question_embedding = embedding_model.encode(question).tolist()

    sql = text("""
        SELECT 
            file_name,
            chunk_index,
            text_chunk,
            doc_metadata,
            1 - (embedding <#> :embedding) AS similarity
        FROM document_chunks
        ORDER BY embedding <#> :embedding
        LIMIT :top_k
    """)

    with engine.connect() as conn:
        result = conn.execute(sql, {
            "embedding": question_embedding,
            "top_k": top_k
        })

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
