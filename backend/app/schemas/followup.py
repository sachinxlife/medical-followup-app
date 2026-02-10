from datetime import datetime
from typing import List
from pydantic import BaseModel
from app.schemas.visit import Visit as VisitSchema

class FollowUp(VisitSchema):
    patient_name: str
    patient_id: int

class FollowUpsResponse(BaseModel):
    upcoming: List[FollowUp]
    missed: List[FollowUp]
