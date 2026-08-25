from collections.abc import Sequence
from threading import RLock
from rag_service.domain.entities import Chunk, SearchResult


class InMemoryVectorStore:
    """Thread-safe local store; replace with a durable vector DB."""

    def __init__(self) -> None:
        self._items: dict[str, tuple[Chunk, list[float]]] = {}
        self._lock = RLock()

    def upsert(self, chunks: Sequence[Chunk], vectors: Sequence[list[float]]) -> None:
        if len(chunks) != len(vectors):
            raise ValueError("each chunk must have one vector")
        with self._lock:
            for chunk, vector in zip(chunks, vectors, strict=True):
                self._items[chunk.id] = (chunk, vector)

    def search(self, vector: list[float], limit: int) -> list[SearchResult]:
        with self._lock:
            results = [SearchResult(chunk, sum(a * b for a, b in zip(vector, candidate))) for chunk, candidate in self._items.values()]
        return sorted(results, key=lambda x: x.score, reverse=True)[:limit]
