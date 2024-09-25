from sqlalchemy.orm import Session
from app.database import Report
from app.schemas import ReportCreate
from datetime import datetime

def create_report(session:Session, report:ReportCreate):
    db_report = Report(**report.model_dump(), created_at=datetime.utcnow())
    session.add(db_report)
    session.commit()
    session.refresh(db_report)
    return db_report

def update_report(session:Session, report_id:str, status:str):
    report = session.query(Report).filter(Report.id == report_id).first()
    if report:
        report.status = status
        if status == "complete":
            report.completed_at = datetime.utcnow()
        session.commit()
        session.refresh(report)
    return report