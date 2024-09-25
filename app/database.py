from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Column, Integer, String, DateTime


engine = create_engine(
    "postgresql+psycopg2://root:password@localhost/loop",
    pool_size=20,
    max_overflow=0
)

session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = scoped_session(session_factory)

Base = declarative_base()

def get_db():
    return Session()

class Store(Base):
    __tablename__ = "stores"

    id = Column(String, primary_key=True, index=True)
    timezone_str = Column(String, default="America/Chicago")

class BusinessHours(Base):
    __tablename__ = "business_hours"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    store_id = Column(String)
    day_of_week = Column(Integer)
    start_time_local = Column(String)
    end_time_local = Column(String)

class StoreStatus(Base):
    __tablename__ = "store_status"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    store_id = Column(String)
    timestamp_utc = Column(DateTime, index=True)
    status = Column(String)

class Report(Base):
    __tablename__ = "reports"

    id = Column(String, primary_key=True)
    status = Column(String)
    created_at = Column(DateTime)
    completed_at = Column(DateTime, nullable=True)