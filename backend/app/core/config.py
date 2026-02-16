"""Application configuration"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    """Application Settings"""
    
    # App
    app_name: str = "AlgoTrade Lab"
    debug: bool = False
    environment: str = "development"
    log_level: str = "INFO"
    
    # Database
    database_url: str = Field(default="postgresql://user:password@localhost:5432/algotrade_db")
    
    # JWT/Security
    secret_key: str = Field(default="your-secret-key-change-in-production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # WebSocket
    ws_host: str = "localhost"
    ws_port: int = 8001
    
    # Redis
    redis_url: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
