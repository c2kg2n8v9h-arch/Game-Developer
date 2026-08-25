"""Vendor-neutral contracts for world models and generated-asset storage."""

from typing import Protocol

from .world_entities import GeneratedWorld, WorldJob, WorldRequest


class WorldModel(Protocol):
    def create_world(self, request: WorldRequest) -> WorldJob: ...
    def get_world(self, world_id: str) -> GeneratedWorld: ...


class WorldAssetStore(Protocol):
    def save_manifest(self, world: GeneratedWorld) -> str: ...
