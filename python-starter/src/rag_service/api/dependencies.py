from functools import lru_cache
from rag_service.application.services.npc_dialogue import NpcDialogueService
from rag_service.application.services.ingestion import IngestionService
from rag_service.application.services.huggingface_import import HuggingFaceDatasetImporter
from rag_service.application.services.query import QueryService
from rag_service.application.services.world_generation import WorldGenerationService
from rag_service.config.settings import get_settings
from rag_service.infrastructure.embeddings.hash_embedder import HashEmbedder
from rag_service.infrastructure.embeddings.sentence_transformer import SentenceTransformerEmbedder
from rag_service.infrastructure.generators.context_generator import ContextGenerator
from rag_service.infrastructure.vector_stores.in_memory import InMemoryVectorStore
from rag_service.infrastructure.vector_stores.sqlite import SQLiteVectorStore
from rag_service.infrastructure.asset_stores.local import LocalWorldAssetStore
from rag_service.infrastructure.world_models.local import LocalWorldModel
from rag_service.infrastructure.world_models.nvidia_cosmos import NvidiaCosmosWorldModel
from rag_service.infrastructure.world_models.world_labs import WorldLabsWorldModel
from rag_service.infrastructure.generators.huggingface_npc import HuggingFaceNpcGenerator
from rag_service.infrastructure.generators.local_npc import LocalNpcGenerator

_local_world_model = LocalWorldModel()


@lru_cache
def get_embedder():
    config = get_settings()
    provider = config.embedding_provider.lower()
    if provider == "hash":
        return HashEmbedder()
    if provider == "sentence_transformers":
        return SentenceTransformerEmbedder(
            config.embedding_model,
            config.embedding_device,
            str(config.huggingface_cache_path),
        )
    raise RuntimeError(f"unsupported embedding provider: {provider}")


@lru_cache
def get_vector_store():
    config = get_settings()
    provider = config.vector_store_provider.lower()
    if provider == "memory":
        return InMemoryVectorStore()
    if provider == "sqlite":
        return SQLiteVectorStore(config.vector_store_path)
    raise RuntimeError(f"unsupported vector store provider: {provider}")


@lru_cache
def get_ingestion_service() -> IngestionService:
    config = get_settings()
    return IngestionService(get_embedder(), get_vector_store(), config.chunk_size, config.chunk_overlap)


@lru_cache
def get_huggingface_importer() -> HuggingFaceDatasetImporter:
    config = get_settings()
    token = config.huggingface_token.get_secret_value() if config.huggingface_token else None
    return HuggingFaceDatasetImporter(get_ingestion_service(), token)


@lru_cache
def get_query_service() -> QueryService:
    return QueryService(get_embedder(), get_vector_store(), ContextGenerator())


@lru_cache
def get_npc_dialogue_service() -> NpcDialogueService:
    config = get_settings()
    provider = config.npc_provider.lower()
    if provider == "local":
        generator = LocalNpcGenerator()
    elif provider == "huggingface":
        if config.huggingface_token is None:
            raise RuntimeError("RAG_HUGGINGFACE_TOKEN is required for the Hugging Face NPC provider")
        generator = HuggingFaceNpcGenerator(
            config.huggingface_chat_model,
            config.huggingface_token.get_secret_value(),
            config.huggingface_inference_provider,
            config.huggingface_max_tokens,
        )
    else:
        raise RuntimeError(f"unsupported NPC provider: {provider}")
    return NpcDialogueService(get_embedder(), get_vector_store(), generator)


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
