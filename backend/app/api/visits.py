from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.deps import get_db
from app.auth.deps import get_current_doctor
from app.models.visit import Visit
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.schemas.visit import Visit as VisitSchema, VisitCreate

router = APIRouter(prefix="/patients", tags=["visits"])

async def get_patient_for_doctor(patient_id: int, doctor: Doctor, db: AsyncSession) -> Patient:
    result = await db.execute(select(Patient).where(Patient.id == patient_id))
    patient = result.scalar_one_or_none()
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
        
    if patient.doctor_id != doctor.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this patient"
        )
    return patient

@router.post("/{patient_id}/visits", response_model=VisitSchema, status_code=status.HTTP_201_CREATED)
async def create_visit(
    patient_id: int,
    visit_data: VisitCreate,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: AsyncSession = Depends(get_db)
):
    # Verify patient ownership
    await get_patient_for_doctor(patient_id, current_doctor, db)
    
    db_visit = Visit(
        **visit_data.model_dump(),
        patient_id=patient_id
    )
    db.add(db_visit)
    await db.commit()
    await db.refresh(db_visit)
    return db_visit

@router.get("/{patient_id}/visits", response_model=List[VisitSchema])
async def get_patient_visits(
    patient_id: int,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    # Verify patient ownership
    await get_patient_for_doctor(patient_id, current_doctor, db)
    
    # Get visits
    query = select(Visit).where(Visit.patient_id == patient_id).offset(skip).limit(limit)
    result = await db.execute(query)
    visits = result.scalars().all()
    return visits
