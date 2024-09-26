from sqlalchemy.orm import Session
from app.database import Store, StoreStatus
from datetime import datetime

def get_store_timezone(session:Session, store_id:str):
    return session.query(Store).filter(Store.id == store_id).all()

def get_store(db: Session, store_id: str):
    return db.query(Store).filter(Store.id == store_id).first()

def get_stores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Store).offset(skip).limit(limit).all()

def get_store_status(db: Session, store_id: str, start_time: datetime, end_time: datetime):
    data = db.query(StoreStatus).filter(
        StoreStatus.store_id == store_id,
        StoreStatus.timestamp_utc >= start_time,
        StoreStatus.timestamp_utc <= end_time
    ).order_by(StoreStatus.timestamp_utc).all()
    return data