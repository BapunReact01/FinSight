from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database - PostgreSQL (password URL-encoded)
    DATABASE_URL: str = "postgresql://postgres:Bapun%400108@localhost:5432/finsight_db"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Azure Storage
    AZURE_STORAGE_CONNECTION_STRING: Optional[str] = None
    AZURE_CONTAINER_NAME: str = "finsight-uploads"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    class Config:
        env_file = ".env"

settings = Settings()