from sqlalchemy import Column, Integer, ForeignKey, Text, JSON
from app.db.base import Base

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"))
    chunk_text = Column(Text, nullable=False)
    embedding = Column(JSON, nullable=False)
    chunk_index = Column(Integer, nullable=False)
