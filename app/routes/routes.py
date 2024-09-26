from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas
from app.controllers import report
from app.utils.report_utils import generate_report
from uuid import uuid4

router = APIRouter()

@router.post("/trigger_report", response_model=schemas.Report)
async def trigger_report(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    report_id = str(uuid4())
    report_data = report.create_report(db, schemas.ReportCreate(id=report_id, status="Running"))
    background_tasks.add_task(generate_report, report_id, db)
    return report_data

@router.get("/get_report/{report_id}", response_model=schemas.Report)
async def get_report(report_id: str, db: Session = Depends(get_db)):
    db_report = report.get_report(db, report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return db_report