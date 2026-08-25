from functools import lru_cache
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="RAG_", env_file=".env", extra="ignore")
    app_name: str = "Enterprise RAG Service"
    environment: str = "local"
    log_level: str = "INFO"
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k: int = 4
    world_model_provider: str = "local"
    world_labs_api_key: SecretStr | None = None
    world_labs_model: str = "marble-1.1"
    world_labs_base_url: str = "https://api.worldlabs.ai"
    cosmos_base_url: str = "http://127.0.0.1:8080"
    cosmos_api_key: SecretStr | None = None
    world_asset_path: Path = Path("data/worlds")


@lru_cache
def get_settings() -> Settings:
    return Settings()
