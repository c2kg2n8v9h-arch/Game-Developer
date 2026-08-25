"""Entities describing world-generation requests, jobs, and assets."""

from dataclasses import dataclass, field
from enum import StrEnum


class WorldJobStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


@dataclass(frozen=True)
class WorldRequest:
    prompt: str
    display_name: str | None = None
    source_image_url: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class WorldAsset:
    kind: str
    url: str


@dataclass(frozen=True)
class WorldJob:
    id: str
    status: WorldJobStatus
    provider: str
    error: str | None = None


@dataclass(frozen=True)
class GeneratedWorld:
    id: str
    status: WorldJobStatus
    provider: str
    assets: list[WorldAsset] = field(default_factory=list)
    caption: str | None = None
    error: str | None = None
