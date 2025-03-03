from sqlalchemy.orm import Session
from app.db.models.analysis import Analysis
from app.db.schemas.analysis import AnalysisCreate

def create_analysis(db: Session, analysis: AnalysisCreate):
    db_analysis = Analysis(**analysis.dict())
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    return db_analysis

def get_analysis(db: Session, analysis_id: int):
    return db.query(Analysis).filter(Analysis.id == analysis_id).first()
