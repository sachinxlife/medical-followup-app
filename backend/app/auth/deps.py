from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import ALGORITHM, SECRET_KEY
from app.core.config import settings
from app.database.deps import get_db
from app.models.doctor import Doctor

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


async def get_current_doctor(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> Doctor:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        doctor_id: Optional[str] = payload.get("sub")
        if doctor_id is None:
            raise credentials_exception
        doctor_id_int = int(doctor_id)
    except JWTError:
        raise credentials_exception
    except ValueError:
        raise credentials_exception

    result = await db.execute(select(Doctor).where(Doctor.id == doctor_id_int))
    doctor = result.scalar_one_or_none()

    if doctor is None:
        raise credentials_exception
    return doctor
