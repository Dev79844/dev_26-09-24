from sqlalchemy.orm import Session
from app.database import Store

def get_store_timezone(session:Session, store_id:str):
    return session.query(Store).filter(Store.id == store_id).all()
