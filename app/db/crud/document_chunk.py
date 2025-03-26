from sqlalchemy.orm import Session
from app.db.models.document_chunk import DocumentChunk

def create_document_chunk(
    db: Session,
    document_id: int,
    chunk_text: str,
    embedding: list[float],
    chunk_index: int
):
    db_chunk = DocumentChunk(
        document_id=document_id,
        chunk_text=chunk_text,
        embedding=embedding,
        chunk_index=chunk_index
    )
    db.add(db_chunk)
    return db_chunk

def get_chunks_by_document(db: Session, document_id: int):
    return db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).order_by(DocumentChunk.chunk_index).all()
