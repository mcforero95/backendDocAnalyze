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
from app.services.cloud_storage_service import upload_file_to_gcs  # (Nuevo servicio)
from app.services.pubsub_service import publish_to_pubsub         # (Nuevo servicio)
from app.core.config import settings

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

    # 1. Crear registro del documento en base de datos
    document = crud_document.create_document_metadata(db, file, user.id)

    # 2. Subir el archivo original a Cloud Storage
    destination_blob_name = f"{user.id}/{document.id}/{file.filename}"
    upload_file_to_gcs(
        bucket_name=settings.CLOUD_STORAGE_BUCKET,
        upload_file=file,
        destination_blob_name=destination_blob_name
    )

    # 3. Publicar mensaje en Pub/Sub para que el worker procese
    publish_to_pubsub(
        topic_name=settings.PUBSUB_TOPIC,
        data={
            "user_id": user.id,
            "document_id": document.id,
            "bucket_name": settings.CLOUD_STORAGE_BUCKET,
            "blob_name": destination_blob_name
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
