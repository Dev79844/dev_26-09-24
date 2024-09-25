from sqlalchemy.orm import Session
from app.database import BusinessHours


def get_business_hours(session:Session, store_id:str):
    return session.query(BusinessHours).filter(BusinessHours.store_id == store_id).all()