from pathlib import Path
from types import SimpleNamespace

from rag_service.domain.entities import Chunk
from rag_service.infrastructure.embeddings.sentence_transformer import SentenceTransformerEmbedder
from rag_service.infrastructure.generators.huggingface_npc import HuggingFaceNpcGenerator
from rag_service.infrastructure.vector_stores.sqlite import SQLiteVectorStore


class FakeEmbeddingModel:
    def encode(self, texts, normalize_embeddings):
        assert normalize_embeddings is True
        return [[float(len(text)), 1.0] for text in texts]


def test_sentence_transformer_adapter_is_lazy_and_normalizes() -> None:
    calls = []

    def factory(name, **kwargs):
        calls.append((name, kwargs))
        return FakeEmbeddingModel()

    embedder = SentenceTransformerEmbedder("test/model", "cpu", model_factory=factory)
    assert calls == []
    assert embedder.embed(["lore"]) == [[4.0, 1.0]]
    assert calls == [("test/model", {"device": "cpu"})]


def test_sqlite_vector_store_persists_chunks(tmp_path: Path) -> None:
    path = tmp_path / "rag.sqlite3"
    store = SQLiteVectorStore(path)
    store.upsert([Chunk("1", "doc", "Moon gate")], [[1.0, 0.0]])

    reopened = SQLiteVectorStore(path)
    results = reopened.search([1.0, 0.0], 1)

    assert results[0].chunk.content == "Moon gate"
    assert results[0].score == 1.0


def test_huggingface_npc_adapter_parses_structured_reply() -> None:
    content = '{"speech":"The gate opens.","emotion":"hopeful","intent":"offer_quest","actions":[{"kind":"offer_quest","target":"moon_gate","value":"open"}]}'
    response = SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=content))])
    client = SimpleNamespace(chat_completion=lambda **kwargs: response)
    generator = HuggingFaceNpcGenerator("test/model", "token", client=client)

    reply = generator.reply("Guide", "Help me", {}, [Chunk("1", "doc", "The moon gate is sealed.")])

    assert reply.speech == "The gate opens."
    assert reply.actions[0].kind == "offer_quest"
