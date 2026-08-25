from functools import lru_cache
from rag_service.application.services.ingestion import IngestionService
from rag_service.application.services.query import QueryService
from rag_service.application.services.world_generation import WorldGenerationService
from rag_service.config.settings import get_settings
from rag_service.infrastructure.embeddings.hash_embedder import HashEmbedder
from rag_service.infrastructure.generators.context_generator import ContextGenerator
from rag_service.infrastructure.vector_stores.in_memory import InMemoryVectorStore
from rag_service.infrastructure.asset_stores.local import LocalWorldAssetStore
from rag_service.infrastructure.world_models.local import LocalWorldModel
from rag_service.infrastructure.world_models.nvidia_cosmos import NvidiaCosmosWorldModel
from rag_service.infrastructure.world_models.world_labs import WorldLabsWorldModel

_embedder, _store, _generator = HashEmbedder(), InMemoryVectorStore(), ContextGenerator()
_local_world_model = LocalWorldModel()


@lru_cache
def get_ingestion_service() -> IngestionService:
    config = get_settings()
    return IngestionService(_embedder, _store, config.chunk_size, config.chunk_overlap)


@lru_cache
def get_query_service() -> QueryService:
    return QueryService(_embedder, _store, _generator)


@lru_cache
def get_world_generation_service() -> WorldGenerationService:
    config = get_settings()
    provider = config.world_model_provider.lower()
    if provider == "world_labs":
        if config.world_labs_api_key is None:
            raise RuntimeError("RAG_WORLD_LABS_API_KEY is required")
        model = WorldLabsWorldModel(config.world_labs_api_key.get_secret_value(), config.world_labs_model, config.world_labs_base_url)
    elif provider == "nvidia_cosmos":
        key = config.cosmos_api_key.get_secret_value() if config.cosmos_api_key else None
        model = NvidiaCosmosWorldModel(config.cosmos_base_url, key)
    elif provider == "local":
        model = _local_world_model
    else:
        raise RuntimeError(f"unsupported world model provider: {provider}")
    return WorldGenerationService(model, get_query_service(), LocalWorldAssetStore(config.world_asset_path))
