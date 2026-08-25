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


class WorldCreateRequest(BaseModel):
    description: str = Field(min_length=1)
    display_name: str | None = None
    source_image_url: str | None = None
    metadata: dict[str, str] = Field(default_factory=dict)


class WorldJobResponse(BaseModel):
    id: str
    status: str
    provider: str
    error: str | None = None


class WorldAssetResponse(BaseModel):
    kind: str
    url: str


class WorldResponse(WorldJobResponse):
    caption: str | None = None
    assets: list[WorldAssetResponse]
