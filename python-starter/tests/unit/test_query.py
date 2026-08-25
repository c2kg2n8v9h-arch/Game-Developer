from rag_service.application.dto import IngestCommand, QueryCommand
from rag_service.application.services.ingestion import IngestionService
from rag_service.application.services.query import QueryService
from rag_service.infrastructure.embeddings.hash_embedder import HashEmbedder
from rag_service.infrastructure.generators.context_generator import ContextGenerator
from rag_service.infrastructure.vector_stores.in_memory import InMemoryVectorStore


def test_query_returns_grounded_citation() -> None:
    embedder, store = HashEmbedder(), InMemoryVectorStore()
    IngestionService(embedder, store, 100, 10).ingest(IngestCommand("handbook", "Employees receive twenty vacation days."))
    result = QueryService(embedder, store, ContextGenerator()).query(QueryCommand("How many vacation days?"))
    assert result.citations[0].document_id == "handbook"
    assert "twenty vacation days" in result.answer
