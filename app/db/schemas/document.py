from pydantic import BaseModel

class DocumentCreate(BaseModel):
    title: str
    content: str

class DocumentOut(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int

    class Config:
        orm_mode = True
