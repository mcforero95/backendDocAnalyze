from pydantic import BaseModel
from typing import List

class DocumentChunkOut(BaseModel):
    chunk_index: int
    chunk_text: str
    embedding: List[float]

    class Config:
        orm_mode = True
