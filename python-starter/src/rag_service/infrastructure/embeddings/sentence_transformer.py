from collections.abc import Callable, Sequence
from threading import Lock
from typing import Any


class SentenceTransformerEmbedder:
    """Lazy semantic embedder so application startup never downloads a model."""

    def __init__(
        self,
        model_name: str,
        device: str | None = None,
        cache_folder: str | None = None,
        model_factory: Callable[..., Any] | None = None,
    ) -> None:
        self.model_name = model_name
        self._device = device
        self._cache_folder = cache_folder
        self._factory = model_factory
        self._model: Any | None = None
        self._lock = Lock()

    def _get_model(self) -> Any:
        if self._model is None:
            with self._lock:
                if self._model is None:
                    factory = self._factory
                    if factory is None:
                        from sentence_transformers import SentenceTransformer

                        factory = SentenceTransformer
                    kwargs = {}
                    if self._device:
                        kwargs["device"] = self._device
                    if self._cache_folder:
                        kwargs["cache_folder"] = self._cache_folder
                    self._model = factory(self.model_name, **kwargs)
        return self._model

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        if not texts:
            return []
        vectors = self._get_model().encode(list(texts), normalize_embeddings=True)
        return [[float(value) for value in vector] for vector in vectors]
