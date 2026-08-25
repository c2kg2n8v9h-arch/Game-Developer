from dataclasses import asdict
from fastapi import APIRouter, Depends
from rag_service.api.dependencies import get_ingestion_service, get_query_service
from rag_service.api.schemas import AnswerResponse, CitationResponse, DocumentRequest, IngestResponse, QueryRequest
from rag_service.application.dto import IngestCommand, QueryCommand
from rag_service.application.services.ingestion import IngestionService
from rag_service.application.services.query import QueryService

router = APIRouter(prefix="/v1", tags=["rag"])


@router.post("/documents", response_model=IngestResponse, status_code=201)
def ingest_document(request: DocumentRequest, service: IngestionService = Depends(get_ingestion_service)) -> IngestResponse:
    count = service.ingest(IngestCommand(request.document_id, request.content, request.metadata))
    return IngestResponse(document_id=request.document_id, chunks_indexed=count)


@router.post("/query", response_model=AnswerResponse)
def query(request: QueryRequest, service: QueryService = Depends(get_query_service)) -> AnswerResponse:
    result = service.query(QueryCommand(request.question, request.top_k))
    return AnswerResponse(answer=result.answer, citations=[CitationResponse(**asdict(x)) for x in result.citations])
