from dataclasses import asdict
from fastapi import APIRouter, Depends
from rag_service.api.dependencies import get_huggingface_importer, get_ingestion_service, get_query_service
from rag_service.api.schemas import AnswerResponse, CitationResponse, DocumentRequest, HuggingFaceDatasetRequest, HuggingFaceDatasetResponse, IngestResponse, QueryRequest
from rag_service.application.services.huggingface_import import HuggingFaceDatasetImporter
from rag_service.application.dto import IngestCommand, QueryCommand
from rag_service.application.services.ingestion import IngestionService
from rag_service.application.services.query import QueryService

router = APIRouter(prefix="/v1", tags=["rag"])


@router.post("/documents", response_model=IngestResponse, status_code=201)
def ingest_document(request: DocumentRequest, service: IngestionService = Depends(get_ingestion_service)) -> IngestResponse:
    count = service.ingest(IngestCommand(request.document_id, request.content, request.metadata))
    return IngestResponse(document_id=request.document_id, chunks_indexed=count)


@router.post("/datasets/hugging-face", response_model=HuggingFaceDatasetResponse, status_code=201)
def ingest_huggingface_dataset(
    request: HuggingFaceDatasetRequest,
    importer: HuggingFaceDatasetImporter = Depends(get_huggingface_importer),
) -> HuggingFaceDatasetResponse:
    rows, chunks = importer.import_rows(
        request.dataset_id,
        request.split,
        request.config_name,
        request.revision,
        request.text_columns,
        request.max_rows,
    )
    return HuggingFaceDatasetResponse(
        dataset_id=request.dataset_id,
        split=request.split,
        rows_indexed=rows,
        chunks_indexed=chunks,
    )


@router.post("/query", response_model=AnswerResponse)
def query(request: QueryRequest, service: QueryService = Depends(get_query_service)) -> AnswerResponse:
    result = service.query(QueryCommand(request.question, request.top_k))
    return AnswerResponse(answer=result.answer, citations=[CitationResponse(**asdict(x)) for x in result.citations])
