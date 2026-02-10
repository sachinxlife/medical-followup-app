from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class VisitBase(BaseModel):
    visit_date: datetime = Field(default_factory=datetime.utcnow)
    notes: Optional[str] = Field(default=None, max_length=5000)
    follow_up_date: Optional[datetime] = None

class VisitCreate(VisitBase):
    pass

class Visit(VisitBase):
    id: int
    patient_id: int
    created_at: datetime

    class Config:
        from_attributes = True
