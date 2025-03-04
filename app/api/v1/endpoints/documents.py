from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.crud import document as crud_document, user as crud_user
from app.db.schemas.document import DocumentOut, DocumentCreate
from app.core.security import decode_access_token
from app.services.document_processor import extract_text
from fastapi.security import OAuth2PasswordBearer
from typing import List
from app.db.schemas.document import DocumentOut

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

    text = extract_text(file)
    if not text:
        raise HTTPException(status_code=400, detail="No se pudo extraer texto del archivo.")

    document = crud_document.create_document(
        db, DocumentCreate(title=file.filename, content=text), user.id
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
