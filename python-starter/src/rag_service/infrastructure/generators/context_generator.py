from collections.abc import Sequence
from rag_service.domain.entities import Chunk


class ContextGenerator:
    """Local context echo; replace with a production LLM adapter."""

    def generate(self, question: str, context: Sequence[Chunk]) -> str:
        if not context:
            return "I do not have enough indexed context to answer that question."
        return f"Retrieved context for '{question}': {' '.join(x.content for x in context)}"
