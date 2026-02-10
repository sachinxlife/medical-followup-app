from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Medical Follow-up App"
    API_V1_STR: str = "/api/v1"
    
    # Check if DATABASE_URL is set, otherwise use a default
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/medicalapp"
    
    SECRET_KEY: str = "CHANGE_ME_IN_PRODUCTION"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
