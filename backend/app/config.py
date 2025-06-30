from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    database_url: str = "postgresql://rpassistant:rpassistant@localhost:5432/rpassistant"
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    google_client_id: Optional[str] = None
    google_client_secret: Optional[str] = None
    discord_client_id: Optional[str] = None
    discord_client_secret: Optional[str] = None
    discord_redirect_uri: str = "http://localhost:8000/auth/discord/callback"
    
    openai_api_key: Optional[str] = None
    
    max_file_size: int = 50000000
    upload_folder: str = "uploads"
    
    redis_url: str = "redis://localhost:6379"
    
    class Config:
        env_file = ".env"

settings = Settings()