from collections.abc import Sequence
from typing import Protocol
from .entities import Chunk, NpcReply, SearchResult


class Embedder(Protocol):
    def embed(self, texts: Sequence[str]) -> list[list[float]]: ...


class VectorStore(Protocol):
    def upsert(self, chunks: Sequence[Chunk], vectors: Sequence[list[float]]) -> None: ...
    def search(self, vector: list[float], limit: int) -> list[SearchResult]: ...


class Generator(Protocol):
    def generate(self, question: str, context: Sequence[Chunk]) -> str: ...


class NpcGenerator(Protocol):
    def reply(
        self,
        character: str,
        player_message: str,
        state: dict[str, str],
        context: Sequence[Chunk],
    ) -> NpcReply: ...
