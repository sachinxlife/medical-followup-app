from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Medical Follow-up App"
    API_V1_STR: str = "/api/v1"

    # Prefer environment-provided DATABASE_URL in production
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/medicalapp"

    SECRET_KEY: str = "CHANGE_ME_IN_PRODUCTION"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
