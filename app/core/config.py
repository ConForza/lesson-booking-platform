from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Lesson Reminder API"
    api_v1_prefix: str = "/api/v1"
    environment: str = "local"
    version: str = "0.1.0"

    jwt_secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=".env"
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()