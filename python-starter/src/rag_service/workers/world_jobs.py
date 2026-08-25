from rag_service.application.services.world_generation import WorldGenerationService
from rag_service.domain.world_entities import GeneratedWorld


def poll_and_persist_world(service: WorldGenerationService, world_id: str) -> GeneratedWorld:
    return service.get(world_id, persist_manifest=True)
