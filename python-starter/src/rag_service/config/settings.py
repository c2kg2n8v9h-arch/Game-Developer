from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="RAG_", env_file=".env", extra="ignore")
    app_name: str = "Enterprise RAG Service"
    environment: str = "local"
    log_level: str = "INFO"
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k: int = 4


@lru_cache
def get_settings() -> Settings:
    return Settings()
