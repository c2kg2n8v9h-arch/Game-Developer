"""Orchestrates RAG-grounded world generation."""

from dataclasses import dataclass, field

from rag_service.application.dto import QueryCommand
from rag_service.application.services.query import QueryService
from rag_service.domain.exceptions import RagError
from rag_service.domain.world_entities import GeneratedWorld, WorldJob, WorldRequest
from rag_service.domain.world_ports import WorldAssetStore, WorldModel


@dataclass(frozen=True)
class GenerateWorldCommand:
    description: str
    display_name: str | None = None
    source_image_url: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)


class WorldGenerationService:
    def __init__(
        self,
        model: WorldModel,
        query_service: QueryService,
        asset_store: WorldAssetStore,
    ) -> None:
        self._model = model
        self._query_service = query_service
        self._asset_store = asset_store

    def create(self, command: GenerateWorldCommand) -> WorldJob:
        description = command.description.strip()
        if not description:
            raise RagError("world description must not be empty")
        grounding = self._query_service.query(QueryCommand(description)).answer
        prompt = f"Requested world:\n{description}\n\nRetrieved project context:\n{grounding}"
        return self._model.create_world(
            WorldRequest(prompt, command.display_name, command.source_image_url, command.metadata)
        )

    def get(self, world_id: str, persist_manifest: bool = False) -> GeneratedWorld:
        world = self._model.get_world(world_id)
        if persist_manifest:
            self._asset_store.save_manifest(world)
        return world
