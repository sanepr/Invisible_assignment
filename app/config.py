"""Application configuration module."""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)
    
    # Database
    DATABASE_URL: str = "sqlite:///./expense_settlement.db"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Application
    APP_NAME: str = "Expense Settlement API"
    DEBUG: bool = True


settings = Settings()
