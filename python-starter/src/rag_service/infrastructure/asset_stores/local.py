import json
from dataclasses import asdict
from pathlib import Path
from rag_service.domain.world_entities import GeneratedWorld


class LocalWorldAssetStore:
    def __init__(self, root: Path) -> None:
        self._root = root

    def save_manifest(self, world: GeneratedWorld) -> str:
        directory = self._root / world.id
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / "manifest.json"
        path.write_text(json.dumps(asdict(world), indent=2), encoding="utf-8")
        return str(path)
