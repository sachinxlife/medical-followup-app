from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class VisitBase(BaseModel):
    visit_date: datetime
    notes: Optional[str] = None
    follow_up_date: Optional[datetime] = None

class VisitCreate(VisitBase):
    pass

class Visit(VisitBase):
    id: int
    patient_id: int
    created_at: datetime

    class Config:
        from_attributes = True
