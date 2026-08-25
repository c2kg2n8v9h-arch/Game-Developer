from pydantic import BaseModel, Field


class DocumentRequest(BaseModel):
    document_id: str = Field(min_length=1)
    content: str = Field(min_length=1)
    metadata: dict[str, str] = Field(default_factory=dict)


class IngestResponse(BaseModel):
    document_id: str
    chunks_indexed: int


class QueryRequest(BaseModel):
    question: str = Field(min_length=1)
    top_k: int = Field(default=4, ge=1, le=20)


class CitationResponse(BaseModel):
    chunk_id: str
    document_id: str
    score: float


class AnswerResponse(BaseModel):
    answer: str
    citations: list[CitationResponse]
