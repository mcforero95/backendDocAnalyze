from pydantic import BaseModel
from typing import Optional  # Importar Optional

class DocumentCreate(BaseModel):
    title: str
    content: str

class DocumentOut(BaseModel):
    id: int
    title: str
    content: Optional[str]
    owner_id: int

    class Config:
        orm_mode = True
