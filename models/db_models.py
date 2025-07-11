from sqlalchemy import Column, Integer, String, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from pgvector.sqlalchemy import Vector

Base = declarative_base()

class DocumentChunk(Base):
    __tablename__ = 'document_chunks'

    id = Column(Integer, primary_key=True)
    file_name = Column(String)
    chunk_index = Column(Integer)
    text_chunk = Column(Text)
    embedding = Column(Vector(384))
    doc_metadata = Column(JSON)
