from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from app.database.deps import get_db
from app.auth.deps import get_current_doctor
from app.models.visit import Visit
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.schemas.followup import FollowUpsResponse, FollowUp

router = APIRouter(prefix="/followups", tags=["follow-ups"])

@router.get("/", response_model=FollowUpsResponse)
async def get_followups(
    current_doctor: Doctor = Depends(get_current_doctor),
    db: AsyncSession = Depends(get_db)
):
    # Use datetime for comparison with DateTime column
    now = datetime.utcnow()
    today_start = datetime(now.year, now.month, now.day)
    seven_days_later = today_start + timedelta(days=7)
    
    # Base query: Visits for patients belonging to current doctor that have a follow_up_date
    stmt = (
        select(Visit)
        .join(Visit.patient)
        .where(
            and_(
                Patient.doctor_id == current_doctor.id,
                Visit.follow_up_date.is_not(None)
            )
        )
        .options(selectinload(Visit.patient))
    )

    # 1. Upcoming follow-ups: follow_up_date is today or in future (up to 7 days)
    # maximizing coverage: include appointments from start of today until end of 7th day
    upcoming_stmt = stmt.where(
        and_(
            Visit.follow_up_date >= today_start,
            Visit.follow_up_date <= seven_days_later + timedelta(days=1) # inclusive of the 7th day
        )
    ).order_by(Visit.follow_up_date.asc())
    
    upcoming_result = await db.execute(upcoming_stmt)
    upcoming_visits = upcoming_result.scalars().all()

    # 2. Missed follow-ups: follow_up_date is in the past (before today_start)
    missed_stmt = stmt.where(
        Visit.follow_up_date < today_start
    ).order_by(Visit.follow_up_date.desc())
    
    missed_result = await db.execute(missed_stmt)
    missed_visits = missed_result.scalars().all()

    def map_visits(visits):
        return [
            FollowUp(
                id=v.id,
                patient_id=v.patient_id,
                created_at=v.created_at,
                visit_date=v.visit_date,
                notes=v.notes,
                follow_up_date=v.follow_up_date,
                patient_name=v.patient.name
            )
            for v in visits
        ]

    return FollowUpsResponse(
        upcoming=map_visits(upcoming_visits),
        missed=map_visits(missed_visits)
    )
