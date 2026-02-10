import sys
import os

# Add the project root directory to the Python path to allow running as script
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, APIRouter
from app.auth.router import router as auth_router
from app.api.patients import router as patients_router
from app.api.visits import router as visits_router
from app.api.followups import router as followups_router

app = FastAPI(title="Medical App")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# API Router setup
app.include_router(auth_router)
app.include_router(patients_router)
app.include_router(visits_router)
app.include_router(followups_router)
