from pydantic import BaseModel, EmailStr

class DoctorCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class DoctorLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
