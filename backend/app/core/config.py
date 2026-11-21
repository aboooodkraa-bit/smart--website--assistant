"""Application settings loaded from environment variables."""
from functools import lru_cache
from typing import Literal
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore")
    
    APP_NAME: str = "Smart Website Assistant"
    APP_ENV: Literal["development", "production", "test"] = "development"
    APP_DEBUG: bool = True
    APP_BASE_URL: str = "http://127.0.0.1:8000"
    SECRET_KEY: str = Field(..., min_length=32)
    ADMIN_INITIAL_EMAIL: str = "admin@example.com"
    ADMIN_INITIAL_PASSWORD: str = Field(..., min_length=8)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/app.db"
    ALLOWED_ORIGINS: str = "http://127.0.0.1:5500,http://localhost:5500"
    AI_PROVIDER: Literal["mock", "openai"] = "mock"
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    AI_MAX_TOKENS: int = 600
    AI_TIMEOUT_SECONDS: int = 20
    RATE_LIMIT_CHAT_PER_MINUTE: int = 20
    RATE_LIMIT_CONTACT_PER_HOUR: int = 5
    CONVERSATION_RETENTION_DAYS: int = 30

    @field_validator("SECRET_KEY")
    @classmethod
    def _secret_must_not_be_placeholder(cls, v: str) -> str:
        if "REPLACE_ME" in v or v.strip() == "":
            raise ValueError("SECRET_KEY is missing or uses the placeholder.")
        return v

    @property
    def allowed_origins_list(self) -> list[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",") if o.strip()]

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
