from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.crud.conversation import get_conversations_by_user, get_conversation
from app.db.crud import user as crud_user  
from app.db.schemas.conversation import ConversationSchema, ConversationListSchema
from app.core.security import decode_access_token
from fastapi.security import OAuth2PasswordBearer
from typing import List

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
router = APIRouter()

@router.get("/list", response_model=List[ConversationListSchema])
def list_conversations(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decode_access_token(token)
    user_email = payload.get("sub")
    user = crud_user.get_user_by_email(db, user_email)
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no autenticado")

    conversations = get_conversations_by_user(db, user.id)
    if not conversations:
        raise HTTPException(status_code=404, detail="No se encontraron conversaciones para este usuario")

    return conversations

@router.get("/byId/{conversation_id}", response_model=ConversationSchema)
def get_conversation_detail(conversation_id: int, db: Session = Depends(get_db)):
    conversation = get_conversation(db, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversación no encontrada")
    return conversation
