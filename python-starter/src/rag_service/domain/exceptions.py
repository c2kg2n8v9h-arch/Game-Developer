class RagError(Exception):
    """Base expected RAG error."""


class EmptyDocumentError(RagError):
    pass


class EmptyQueryError(RagError):
    pass
