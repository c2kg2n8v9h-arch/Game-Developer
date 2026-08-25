from pathlib import Path

from rag_service.application.services.query import QueryService
from rag_service.application.services.world_generation import GenerateWorldCommand, WorldGenerationService
from rag_service.infrastructure.asset_stores.local import LocalWorldAssetStore
from rag_service.infrastructure.embeddings.hash_embedder import HashEmbedder
from rag_service.infrastructure.generators.context_generator import ContextGenerator
from rag_service.infrastructure.vector_stores.in_memory import InMemoryVectorStore
from rag_service.infrastructure.world_models.local import LocalWorldModel


def test_world_generation_uses_local_provider(tmp_path: Path) -> None:
    query = QueryService(HashEmbedder(), InMemoryVectorStore(), ContextGenerator())
    service = WorldGenerationService(LocalWorldModel(), query, LocalWorldAssetStore(tmp_path))
    job = service.create(GenerateWorldCommand("A moonlit castle"))
    world = service.get(job.id, persist_manifest=True)
    assert world.provider == "local"
    assert "A moonlit castle" in (world.caption or "")
    assert (tmp_path / job.id / "manifest.json").exists()
