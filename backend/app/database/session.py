from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def init_db() -> None:
    from app.database.base import Base
    from app.models import doctor, patient, visit  # noqa: F401  # register metadata

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
