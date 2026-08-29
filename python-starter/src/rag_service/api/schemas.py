from pydantic import BaseModel, Field


class DocumentRequest(BaseModel):
    document_id: str = Field(min_length=1)
    content: str = Field(min_length=1)
    metadata: dict[str, str] = Field(default_factory=dict)


class IngestResponse(BaseModel):
    document_id: str
    chunks_indexed: int


class HuggingFaceDatasetRequest(BaseModel):
    dataset_id: str = Field(min_length=1, examples=["roneneldan/TinyStories"])
    split: str = Field(default="train", min_length=1)
    config_name: str | None = None
    revision: str | None = None
    text_columns: list[str] = Field(default_factory=list)
    max_rows: int = Field(default=100, ge=1, le=10_000)


class HuggingFaceDatasetResponse(BaseModel):
    dataset_id: str
    split: str
    rows_indexed: int
    chunks_indexed: int


class NpcTurnRequest(BaseModel):
    character: str = Field(default="The Cartographer", min_length=1)
    player_message: str = Field(min_length=1)
    state: dict[str, str] = Field(default_factory=dict)
    top_k: int = Field(default=3, ge=1, le=10)


class NpcActionResponse(BaseModel):
    kind: str
    target: str | None = None
    value: str | None = None


class NpcTurnResponse(BaseModel):
    speech: str
    emotion: str
    intent: str
    actions: list[NpcActionResponse]


class AiCapabilitiesResponse(BaseModel):
    embedding_provider: str
    embedding_model: str
    vector_store_provider: str
    npc_provider: str
    npc_model: str
    huggingface_token_configured: bool


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
