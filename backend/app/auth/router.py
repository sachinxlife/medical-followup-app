from fastapi import APIRouter, HTTPException, status, Depends
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.deps import get_db
from app.models.doctor import Doctor
from app.schemas.doctor import DoctorCreate
from .schemas import DoctorLogin, Token
from .security import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=Token)
async def signup(doctor: DoctorCreate, db: AsyncSession = Depends(get_db)):
    # Check if email already registered
    result = await db.execute(select(Doctor).where(Doctor.email == doctor.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if registration number already registered
    result = await db.execute(select(Doctor).where(Doctor.registration_number == doctor.registration_number))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration number already registered"
        )
    
    hashed_password = get_password_hash(doctor.password)
    db_doctor = Doctor(
        name=doctor.name,
        email=doctor.email,
        registration_number=doctor.registration_number,
        hashed_password=hashed_password
    )
    
    db.add(db_doctor)
    await db.commit()
    await db.refresh(db_doctor)
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_doctor.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(doctor: DoctorLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Doctor).where(Doctor.email == doctor.email))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not verify_password(doctor.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
