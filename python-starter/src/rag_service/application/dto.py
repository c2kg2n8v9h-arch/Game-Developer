from dataclasses import dataclass, field


@dataclass(frozen=True)
class IngestCommand:
    document_id: str
    content: str
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class QueryCommand:
    question: str
    top_k: int = 4


@dataclass(frozen=True)
class Citation:
    chunk_id: str
    document_id: str
    score: float


@dataclass(frozen=True)
class QueryResponse:
    answer: str
    citations: list[Citation]
