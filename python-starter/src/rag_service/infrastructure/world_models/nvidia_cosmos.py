"""NVIDIA Cosmos NIM adapter using its inference endpoint."""

import httpx

from rag_service.domain.world_entities import GeneratedWorld, WorldAsset, WorldJob, WorldJobStatus, WorldRequest


class NvidiaCosmosWorldModel:
    provider = "nvidia_cosmos"

    def __init__(self, base_url: str, api_key: str | None = None, timeout: float = 300.0) -> None:
        headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
        self._client = httpx.Client(base_url=base_url.rstrip("/"), headers=headers, timeout=timeout)
        self._results: dict[str, GeneratedWorld] = {}

    def create_world(self, request: WorldRequest) -> WorldJob:
        response = self._client.post("/v1/infer", json={"prompt": request.prompt})
        response.raise_for_status()
        data = response.json()
        world_id = str(data.get("id") or data.get("request_id") or data.get("job_id"))
        if world_id == "None":
            raise ValueError("Cosmos response did not contain a job identifier")
        urls = data.get("output_urls") or ([data["output_url"]] if data.get("output_url") else [])
        status = WorldJobStatus.SUCCEEDED if urls else WorldJobStatus.RUNNING
        self._results[world_id] = GeneratedWorld(world_id, status, self.provider, [WorldAsset("video", url) for url in urls])
        return WorldJob(world_id, status, self.provider)

    def get_world(self, world_id: str) -> GeneratedWorld:
        if world_id not in self._results:
            raise LookupError("Cosmos NIM result is not available in this process")
        return self._results[world_id]
