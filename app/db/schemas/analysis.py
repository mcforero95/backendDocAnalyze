from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AnalysisBase(BaseModel):
    document_id: int
    summary: Optional[str] = None
    insights: Optional[str] = None

class AnalysisCreate(AnalysisBase):
    pass

class AnalysisUpdate(AnalysisBase):
    pass

class AnalysisInDBBase(AnalysisBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2 reemplazo de orm_mode

class Analysis(AnalysisInDBBase):
    pass
