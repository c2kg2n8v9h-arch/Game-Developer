"""Deterministic provider for local development and automated tests."""

from uuid import uuid4

from rag_service.domain.world_entities import GeneratedWorld, WorldAsset, WorldJob, WorldJobStatus, WorldRequest


class LocalWorldModel:
    provider = "local"

    def __init__(self) -> None:
        self._worlds: dict[str, GeneratedWorld] = {}

    def create_world(self, request: WorldRequest) -> WorldJob:
        world_id = str(uuid4())
        self._worlds[world_id] = GeneratedWorld(
            id=world_id,
            status=WorldJobStatus.SUCCEEDED,
            provider=self.provider,
            assets=[WorldAsset("manifest", f"local://worlds/{world_id}/manifest.json")],
            caption=request.prompt,
        )
        return WorldJob(world_id, WorldJobStatus.SUCCEEDED, self.provider)

    def get_world(self, world_id: str) -> GeneratedWorld:
        try:
            return self._worlds[world_id]
        except KeyError as exc:
            raise LookupError(f"world not found: {world_id}") from exc
