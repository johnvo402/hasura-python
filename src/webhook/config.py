import os
from typing import Optional
from pydantic_settings import BaseSettings

# Get the project root directory (2 levels up from this file)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

class Settings(BaseSettings):
    # Application settings
    LOG_LEVEL: str = "info"
    ENVIRONMENT: str = "dev"
    ROOT_DOMAIN: str = "localhost"
    DEV_MODE: bool = True
    
    # Hasura settings
    HASURA_BASE_URL: str = "http://localhost:8080"
    HASURA_ADMIN_SECRET: str = "hasura"
    
    # Postgres settings
    POSTGRES_SHM_SIZE: int = 220800000
    POSTGRES_HOST: str = "postgres"
    POSTGRES_USER: str = "postgres"
    POSTGRES_DB_NAME: str = "database"
    POSTGRES_PASSWORD: str = "postgrespassword"
    
    # JWT settings
    JWT_ISSUER: str = "https://nexlab.tech"
    JWT_CHECKSUM: bool = True
    JWT_SECRET_KEY: str = "your-256-bit-secret"
    JWT_AUDIENCE: str = "hasura"
    
    JWT_ACCESS_TOKEN_EXPIRE_HOURS: int = 1
    
    @property
    def DATABASE_URL(self) -> str:
        """Get database URL."""
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:5432/{self.POSTGRES_DB_NAME}"

    class Config:
        env_file = os.path.join(PROJECT_ROOT, ".env")
        case_sensitive = True

# Create global settings instance
settings = Settings()