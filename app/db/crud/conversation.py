from sqlalchemy.orm import Session
from app.db.models.conversation import Conversation, Message

def create_conversation(db: Session, user_id: int, document_id: int):
    conversation = Conversation(user_id=user_id, document_id=document_id)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation

def add_message(db: Session, conversation_id: int, question: str, answer: str):
    message = Message(conversation_id=conversation_id, question=question, answer=answer)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

def get_conversations_by_user(db: Session, user_id: int):
    return db.query(Conversation).filter(Conversation.user_id == user_id).all()

def get_conversation(db: Session, conversation_id: int):
    return db.query(Conversation).filter(Conversation.id == conversation_id).first()
