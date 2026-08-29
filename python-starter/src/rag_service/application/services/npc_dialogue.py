from rag_service.domain.entities import NpcReply
from rag_service.domain.ports import Embedder, NpcGenerator, VectorStore


class NpcDialogueService:
    def __init__(self, embedder: Embedder, store: VectorStore, generator: NpcGenerator) -> None:
        self._embedder = embedder
        self._store = store
        self._generator = generator

    def reply(
        self,
        character: str,
        player_message: str,
        state: dict[str, str],
        top_k: int,
    ) -> NpcReply:
        message = player_message.strip()
        if not message:
            raise ValueError("player message must not be empty")
        results = self._store.search(self._embedder.embed([message])[0], max(1, top_k))
        return self._generator.reply(character.strip() or "Wanderer", message, state, [item.chunk for item in results])
