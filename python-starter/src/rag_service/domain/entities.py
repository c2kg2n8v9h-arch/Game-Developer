from dataclasses import dataclass, field


@dataclass(frozen=True)
class Chunk:
    id: str
    document_id: str
    content: str
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class SearchResult:
    chunk: Chunk
    score: float
