from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

# Shared properties
class DoctorBase(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    registration_number: str = Field(min_length=3, max_length=64)

# Properties to receive via API on creation
class DoctorCreate(DoctorBase):
    password: str = Field(min_length=8, max_length=128)

# Properties to return via API
class Doctor(DoctorBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Properties stored in DB
class DoctorInDB(Doctor):
    hashed_password: str
