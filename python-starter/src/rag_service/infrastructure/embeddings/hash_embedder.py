import hashlib
from collections.abc import Sequence


class HashEmbedder:
    """Deterministic local embedder; replace in production."""

    def __init__(self, dimensions: int = 64) -> None:
        self._dimensions = dimensions

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        output = []
        for text in texts:
            vector = [0.0] * self._dimensions
            for token in text.lower().split():
                index = int.from_bytes(hashlib.sha256(token.encode()).digest()[:4]) % self._dimensions
                vector[index] += 1.0
            magnitude = sum(x * x for x in vector) ** 0.5 or 1.0
            output.append([x / magnitude for x in vector])
        return output
