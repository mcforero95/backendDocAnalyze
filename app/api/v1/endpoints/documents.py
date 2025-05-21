from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.crud import document as crud_document, user as crud_user
from app.db.schemas.document import DocumentOut
from app.core.security import decode_access_token
from fastapi.security import OAuth2PasswordBearer
from typing import List
from app.db.schemas.document_chunk import DocumentChunkOut
from app.db.crud.document_chunk import get_chunks_by_document
from app.services.document_processor import extract_text, process_and_store_chunks_sqlalchemy
from app.services.pubsub_service import publish_to_pubsub         # (Nuevo servicio)
from app.core.config import settings
import base64

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
router = APIRouter()

@router.post("/upload", response_model=DocumentOut)
def upload_document(
    file: UploadFile = File(...),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decode_access_token(token)
    user_email = payload.get("sub")
    user = crud_user.get_user_by_email(db, user_email)
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no autenticado")

    # 1. Crear registro del documento
    document = crud_document.create_document_metadata(db, file, user.id)

    # 2. Leer contenido para Pub/Sub
    file_content = file.file.read()
    file.file.seek(0)

    # 3. Procesar y almacenar chunks inmediatamente
    text = extract_text(file)
    process_and_store_chunks_sqlalchemy(db, document.id, text)

    # 4. Publicar mensaje a Pub/Sub para que el Worker suba a GCS
    destination_blob_name = f"{user.id}/{document.id}/{file.filename}"
    encoded_content = base64.b64encode(file_content).decode("utf-8")
    publish_to_pubsub(
        topic_name=settings.PUBSUB_TOPIC,
        data={
            "user_id": user.id,
            "document_id": document.id,
            "bucket_name": settings.CLOUD_STORAGE_BUCKET,
            "blob_name": destination_blob_name,
            "file_content": encoded_content
        }
    )

    return document

@router.get("/listDocuments", response_model=List[DocumentOut])
def list_documents_by_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decode_access_token(token)
    user_email = payload.get("sub")
    user = crud_user.get_user_by_email(db, user_email)
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no autenticado")

    documents = crud_document.get_documents_by_user(db, user.id)
    if not documents:
        raise HTTPException(status_code=404, detail="No se encontraron documentos para este usuario")

    return documents

@router.get("/document/{document_id}/chunks", response_model=List[DocumentChunkOut])
def get_document_chunks(
    document_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decode_access_token(token)
    user_email = payload.get("sub")
    user = crud_user.get_user_by_email(db, user_email)
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no autenticado")

    chunks = get_chunks_by_document(db, document_id)
    return chunks
