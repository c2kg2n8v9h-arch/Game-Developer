from dataclasses import asdict
from fastapi import APIRouter, Depends, HTTPException
from rag_service.api.dependencies import get_world_generation_service
from rag_service.api.schemas import WorldCreateRequest, WorldJobResponse, WorldResponse
from rag_service.application.services.world_generation import GenerateWorldCommand, WorldGenerationService

router = APIRouter(prefix="/v1/worlds", tags=["worlds"])


@router.post("", response_model=WorldJobResponse, status_code=202)
def create_world(request: WorldCreateRequest, service: WorldGenerationService = Depends(get_world_generation_service)) -> WorldJobResponse:
    return WorldJobResponse(**asdict(service.create(GenerateWorldCommand(**request.model_dump()))))


@router.get("/{world_id}", response_model=WorldResponse)
def get_world(world_id: str, persist_manifest: bool = False, service: WorldGenerationService = Depends(get_world_generation_service)) -> WorldResponse:
    try:
        world = service.get(world_id, persist_manifest)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return WorldResponse(**asdict(world))
