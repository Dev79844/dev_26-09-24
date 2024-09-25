from pydantic import BaseModel
from datetime import datetime

class StoreBase(BaseModel):
    timezone_str: str = "America/Chicago"

class StoreCreate(StoreBase):
    pass

class Store(StoreBase):
    id: str

    class Config:
        orm_mode = True

class ReportBase(BaseModel):
    status: str

class ReportCreate(ReportBase):
    id: str

class Report(ReportBase):
    id: str
    created_at: datetime
    completed_at: datetime = None

    class Config:
        orm_mode = True


