from datetime import datetime
from pydantic import BaseModel

class PatientBase(BaseModel):
    name: str
    age: int
    gender: str
    phone: str

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: int
    doctor_id: int
    created_at: datetime

    class Config:
        from_attributes = True
