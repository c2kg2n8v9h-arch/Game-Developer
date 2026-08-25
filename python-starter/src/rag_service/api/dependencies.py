from functools import lru_cache
from rag_service.application.services.ingestion import IngestionService
from rag_service.application.services.query import QueryService
from rag_service.config.settings import get_settings
from rag_service.infrastructure.embeddings.hash_embedder import HashEmbedder
from rag_service.infrastructure.generators.context_generator import ContextGenerator
from rag_service.infrastructure.vector_stores.in_memory import InMemoryVectorStore

_embedder, _store, _generator = HashEmbedder(), InMemoryVectorStore(), ContextGenerator()


@lru_cache
def get_ingestion_service() -> IngestionService:
    config = get_settings()
    return IngestionService(_embedder, _store, config.chunk_size, config.chunk_overlap)


@lru_cache
def get_query_service() -> QueryService:
    return QueryService(_embedder, _store, _generator)
