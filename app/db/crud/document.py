from sqlalchemy.orm import Session
from app.db.models.document import Document
from app.db.schemas.document import DocumentCreate
from fastapi import UploadFile
from app.core.config import settings

def create_document_metadata(db: Session, file: UploadFile, user_id: int):
    """Crea solo el registro de metadatos en la base de datos, sin guardar archivo."""
    db_document = Document(
        title=file.filename,
        owner_id=user_id,
        content=None  # Dejamos el contenido vacío inicialmente
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def get_documents_by_user(db: Session, user_id: int):
    return db.query(Document).filter(Document.owner_id == user_id).all()
