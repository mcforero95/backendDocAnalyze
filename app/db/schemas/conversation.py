from datetime import datetime
from pydantic import BaseModel
from typing import List

class MessageSchema(BaseModel):
    id: int
    question: str
    answer: str
    created_at: datetime

    class Config:
        from_attributes = True

class ConversationSchema(BaseModel):
    id: int
    document_id: int
    created_at: datetime
    messages: List[MessageSchema]

    class Config:
        from_attributes = True

class ConversationListSchema(BaseModel):
    id: int
    document_id: int
    created_at: datetime

    class Config:
        from_attributes = True
