from sqlalchemy.orm import Session
from app.db.models.document import Document
from app.db.schemas.document import DocumentCreate


def create_document(db: Session, document: DocumentCreate, user_id: int):
    db_document = Document(
        title=document.title,
        content=document.content,
        owner_id=user_id
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


def get_documents_by_user(db: Session, user_id: int):
    return db.query(Document).filter(Document.owner_id == user_id).all()
