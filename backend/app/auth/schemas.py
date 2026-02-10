from pydantic import BaseModel, EmailStr


class DoctorLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
