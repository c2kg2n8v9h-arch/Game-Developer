import json
import math
import sqlite3
from collections.abc import Sequence
from pathlib import Path
from threading import RLock

from rag_service.domain.entities import Chunk, SearchResult


class SQLiteVectorStore:
    """Small durable vector store for local game development and prototypes."""

    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(path, check_same_thread=False)
        self._lock = RLock()
        with self._connection:
            self._connection.execute(
                """CREATE TABLE IF NOT EXISTS chunks (
                    id TEXT PRIMARY KEY,
                    document_id TEXT NOT NULL,
                    content TEXT NOT NULL,
                    metadata TEXT NOT NULL,
                    vector TEXT NOT NULL
                )"""
            )

    def upsert(self, chunks: Sequence[Chunk], vectors: Sequence[list[float]]) -> None:
        if len(chunks) != len(vectors):
            raise ValueError("each chunk must have one vector")
        rows = [
            (chunk.id, chunk.document_id, chunk.content, json.dumps(chunk.metadata), json.dumps(vector))
            for chunk, vector in zip(chunks, vectors, strict=True)
        ]
        with self._lock, self._connection:
            self._connection.executemany(
                """INSERT INTO chunks (id, document_id, content, metadata, vector)
                   VALUES (?, ?, ?, ?, ?)
                   ON CONFLICT(id) DO UPDATE SET
                     document_id=excluded.document_id,
                     content=excluded.content,
                     metadata=excluded.metadata,
                     vector=excluded.vector""",
                rows,
            )

    def search(self, vector: list[float], limit: int) -> list[SearchResult]:
        with self._lock:
            rows = self._connection.execute(
                "SELECT id, document_id, content, metadata, vector FROM chunks"
            ).fetchall()
        query_norm = math.sqrt(sum(value * value for value in vector)) or 1.0
        results = []
        for chunk_id, document_id, content, metadata, stored_vector in rows:
            candidate = json.loads(stored_vector)
            candidate_norm = math.sqrt(sum(value * value for value in candidate)) or 1.0
            score = sum(a * b for a, b in zip(vector, candidate)) / (query_norm * candidate_norm)
            chunk = Chunk(chunk_id, document_id, content, json.loads(metadata))
            results.append(SearchResult(chunk, score))
        return sorted(results, key=lambda result: result.score, reverse=True)[:limit]
