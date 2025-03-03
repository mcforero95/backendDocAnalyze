from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.crud.document import get_documents_by_user
from app.db.crud.user import get_user_by_email
from app.core.security import decode_access_token
from app.services.summarizer import summarize_text
from app.services.question_answering import answer_question
from fastapi.security import OAuth2PasswordBearer
from app.db.crud.conversation import create_conversation, add_message
from app.db.models.conversation import Conversation  # Asegúrate de importar Conversation
import logging

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
router = APIRouter()

@router.get("/summarize/{document_id}")
def summarize(document_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    user_email = payload.get("sub")
    user = get_user_by_email(db, user_email)
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no autenticado")
    
    documents = get_documents_by_user(db, user.id)
    document = next((doc for doc in documents if doc.id == document_id), None)
    if not document:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    
    summary = summarize_text(document.content)
    return {"summary": summary}

@router.post("/ask/{document_id}")
def ask(document_id: int, question: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    user_email = payload.get("sub")
    user = get_user_by_email(db, user_email)
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no autenticado")
    
    documents = get_documents_by_user(db, user.id)
    document = next((doc for doc in documents if doc.id == document_id), None)
    if not document:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    
    conversation = db.query(Conversation).filter_by(user_id=user.id, document_id=document_id).first()
    if not conversation:
        conversation = create_conversation(db, user.id, document_id)
        logger.info(f"Conversación creada con ID: {conversation.id}")
    
    answer = answer_question(document.content, question)
    add_message(db, conversation.id, question, answer)
    return {"answer": answer}