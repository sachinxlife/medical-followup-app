from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.deps import get_db
from app.auth.deps import get_current_doctor
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.schemas.patient import Patient as PatientSchema, PatientCreate

router = APIRouter(prefix="/patients", tags=["patients"])

@router.post("/", response_model=PatientSchema, status_code=status.HTTP_201_CREATED)
async def create_patient(
    patient: PatientCreate,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: AsyncSession = Depends(get_db)
):
    db_patient = Patient(
        **patient.model_dump(),
        doctor_id=current_doctor.id
    )
    db.add(db_patient)
    await db.commit()
    await db.refresh(db_patient)
    return db_patient

@router.get("/", response_model=List[PatientSchema])
async def get_patients(
    current_doctor: Doctor = Depends(get_current_doctor),
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    # Only return patients belonging to the current doctor
    query = select(Patient).where(Patient.doctor_id == current_doctor.id).offset(skip).limit(limit)
    result = await db.execute(query)
    patients = result.scalars().all()
    return patients
