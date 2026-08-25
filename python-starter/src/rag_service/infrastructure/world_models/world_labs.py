"""World Labs Marble API adapter."""

from typing import Any

import httpx

from rag_service.domain.world_entities import GeneratedWorld, WorldAsset, WorldJob, WorldJobStatus, WorldRequest


class WorldLabsWorldModel:
    provider = "world_labs"

    def __init__(self, api_key: str, model: str, base_url: str, timeout: float = 120.0) -> None:
        self._model = model
        self._client = httpx.Client(
            base_url=base_url.rstrip("/"),
            headers={"WLT-Api-Key": api_key},
            timeout=timeout,
        )

    def create_world(self, request: WorldRequest) -> WorldJob:
        world_prompt: dict[str, Any] = {"type": "text", "text_prompt": request.prompt}
        if request.source_image_url:
            world_prompt = {"type": "image", "image_url": request.source_image_url, "text_prompt": request.prompt}
        response = self._client.post(
            "/marble/v1/worlds:generate",
            json={"world_prompt": world_prompt, "model": self._model, "display_name": request.display_name},
        )
        response.raise_for_status()
        data = response.json()
        operation = data.get("operation", data)
        world = data.get("world") or operation.get("response", {}).get("world") or {}
        world_id = world.get("id") or operation.get("world_id") or operation.get("name", "").rsplit("/", 1)[-1]
        if not world_id:
            raise ValueError("World Labs response did not contain a world identifier")
        status = WorldJobStatus.SUCCEEDED if world else WorldJobStatus.QUEUED
        return WorldJob(world_id, status, self.provider)

    def get_world(self, world_id: str) -> GeneratedWorld:
        response = self._client.get(f"/marble/v1/worlds/{world_id}")
        response.raise_for_status()
        world = response.json().get("world", response.json())
        assets = world.get("assets") or {}
        collected: list[WorldAsset] = []
        for kind, url in (assets.get("splats", {}).get("spz_urls") or {}).items():
            collected.append(WorldAsset(f"splat_{kind}", url))
        mesh_url = (assets.get("mesh") or {}).get("collider_mesh_url")
        pano_url = (assets.get("imagery") or {}).get("pano_url")
        for kind, url in (("collider_mesh", mesh_url), ("panorama", pano_url), ("thumbnail", assets.get("thumbnail_url"))):
            if url:
                collected.append(WorldAsset(kind, url))
        return GeneratedWorld(world_id, WorldJobStatus.SUCCEEDED, self.provider, collected, assets.get("caption"))
