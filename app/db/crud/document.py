from sqlalchemy.orm import Session
from app.db.models.document import Document
from app.db.schemas.document import DocumentCreate
import os
from uuid import uuid4
from fastapi import UploadFile
from app.core.config import settings


def create_document(db: Session, file: UploadFile, user_id: int):
    # Extraer texto
    from app.services.document_processor import extract_text
    text = extract_text(file)
    if not text:
        raise ValueError("No se pudo extraer texto del archivo")

    # Guardar archivo en NFS
    ext = file.filename.split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    file_path = os.path.join(settings.SHARED_FILES_PATH, filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # Crear registro en base de datos
    db_document = Document(
        title=file.filename,
        content=text,
        owner_id=user_id
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document, text


def get_documents_by_user(db: Session, user_id: int):
    return db.query(Document).filter(Document.owner_id == user_id).all()
