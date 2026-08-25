from rag_service.application.dto import Citation, QueryCommand, QueryResponse
from rag_service.domain.exceptions import EmptyQueryError
from rag_service.domain.ports import Embedder, Generator, VectorStore


class QueryService:
    def __init__(self, embedder: Embedder, store: VectorStore, generator: Generator) -> None:
        self._embedder, self._store, self._generator = embedder, store, generator

    def query(self, command: QueryCommand) -> QueryResponse:
        question = command.question.strip()
        if not question:
            raise EmptyQueryError("question must not be empty")
        results = self._store.search(self._embedder.embed([question])[0], max(1, command.top_k))
        return QueryResponse(self._generator.generate(question, [x.chunk for x in results]), [Citation(x.chunk.id, x.chunk.document_id, x.score) for x in results])
