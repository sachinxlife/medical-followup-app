from datetime import datetime
from pydantic import BaseModel, Field

class PatientBase(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    age: int = Field(ge=0, le=130)
    gender: str = Field(min_length=1, max_length=20)
    phone: str = Field(min_length=7, max_length=25)

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: int
    doctor_id: int
    created_at: datetime

    class Config:
        from_attributes = True
