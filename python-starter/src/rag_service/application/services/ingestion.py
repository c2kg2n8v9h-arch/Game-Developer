from rag_service.application.dto import IngestCommand
from rag_service.domain.entities import Chunk
from rag_service.domain.exceptions import EmptyDocumentError
from rag_service.domain.ports import Embedder, VectorStore


class IngestionService:
    def __init__(self, embedder: Embedder, store: VectorStore, chunk_size: int, overlap: int) -> None:
        if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
            raise ValueError("invalid chunk configuration")
        self._embedder, self._store = embedder, store
        self._size, self._overlap = chunk_size, overlap

    def ingest(self, command: IngestCommand) -> int:
        text = command.content.strip()
        if not text:
            raise EmptyDocumentError("document content must not be empty")
        step = self._size - self._overlap
        chunks = [Chunk(f"{command.document_id}:{i}", command.document_id, text[start:start + self._size], command.metadata) for i, start in enumerate(range(0, len(text), step))]
        self._store.upsert(chunks, self._embedder.embed([item.content for item in chunks]))
        return len(chunks)
