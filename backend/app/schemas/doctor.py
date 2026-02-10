from datetime import datetime
from pydantic import BaseModel, EmailStr

# Shared properties
class DoctorBase(BaseModel):
    name: str
    email: EmailStr
    registration_number: str

# Properties to receive via API on creation
class DoctorCreate(DoctorBase):
    password: str

# Properties to return via API
class Doctor(DoctorBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Properties stored in DB
class DoctorInDB(Doctor):
    hashed_password: str
