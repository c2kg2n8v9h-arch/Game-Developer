from collections.abc import Sequence

from rag_service.domain.entities import Chunk, NpcReply


class LocalNpcGenerator:
    def reply(
        self,
        character: str,
        player_message: str,
        state: dict[str, str],
        context: Sequence[Chunk],
    ) -> NpcReply:
        del state
        lore = context[0].content if context else "The road ahead is hidden by mist."
        return NpcReply(
            speech=f"{character} considers '{player_message}'. {lore}",
            emotion="curious",
            intent="reveal_lore" if context else "conversation",
        )
