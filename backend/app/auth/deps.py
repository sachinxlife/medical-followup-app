from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import ALGORITHM, SECRET_KEY
from app.database.deps import get_db
from app.models.doctor import Doctor

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


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
        email: Optional[str] = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await db.execute(select(Doctor).where(Doctor.email == email))
    doctor = result.scalar_one_or_none()

    if doctor is None:
        raise credentials_exception
    return doctor
