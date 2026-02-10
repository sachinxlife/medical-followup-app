from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.followups import router as followups_router
from app.api.patients import router as patients_router
from app.api.visits import router as visits_router
from app.auth.router import router as auth_router
from app.core.config import settings
from app.database.session import init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(patients_router, prefix=settings.API_V1_STR)
app.include_router(visits_router, prefix=settings.API_V1_STR)
app.include_router(followups_router, prefix=settings.API_V1_STR)
