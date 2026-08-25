from rag_service.application.dto import IngestCommand
from rag_service.application.services.ingestion import IngestionService
from rag_service.infrastructure.embeddings.hash_embedder import HashEmbedder
from rag_service.infrastructure.vector_stores.in_memory import InMemoryVectorStore


def test_ingestion_chunks_and_indexes_document() -> None:
    service = IngestionService(HashEmbedder(), InMemoryVectorStore(), 10, 2)
    assert service.ingest(IngestCommand("doc-1", "A document longer than one chunk.")) > 1
