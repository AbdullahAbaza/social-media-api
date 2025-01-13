import secrets
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Use top level .env file (one level above ./app/)
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore"
    )

    SECRET_KEY: str = secrets.token_urlsafe(32)
    
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    
    DATABASE_HOSTNAME: str
    DATABASE_PORT: int = 5432
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str = ""
    DATABASE_NAME: str = ""
    

settings = Settings()