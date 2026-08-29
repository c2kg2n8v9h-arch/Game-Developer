from functools import lru_cache
from pathlib import Path

from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="RAG_", env_file=".env", extra="ignore")
    app_name: str = "Enterprise RAG Service"
    environment: str = "local"
    log_level: str = "INFO"
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k: int = 4
    embedding_provider: str = "hash"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_device: str | None = None
    huggingface_cache_path: Path = Path("data/hf-cache/hub")
    vector_store_provider: str = "memory"
    vector_store_path: Path = Path("data/rag.sqlite3")
    npc_provider: str = "local"
    huggingface_chat_model: str = "Qwen/Qwen3-8B"
    huggingface_inference_provider: str = "auto"
    huggingface_max_tokens: int = 300
    world_model_provider: str = "local"
    world_labs_api_key: SecretStr | None = None
    world_labs_model: str = "marble-1.1"
    world_labs_base_url: str = "https://api.worldlabs.ai"
    cosmos_base_url: str = "http://127.0.0.1:8080"
    cosmos_api_key: SecretStr | None = None
    huggingface_token: SecretStr | None = None
    world_asset_path: Path = Path("data/worlds")

    @field_validator("huggingface_token", "world_labs_api_key", "cosmos_api_key", mode="before")
    @classmethod
    def blank_secrets_are_unset(cls, value: object) -> object:
        if value is None or (isinstance(value, str) and not value.strip()):
            return None
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
