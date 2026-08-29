import os

# Tests use deterministic, in-memory providers even when a developer .env enables
# semantic embeddings and durable runtime storage.
os.environ["RAG_EMBEDDING_PROVIDER"] = "hash"
os.environ["RAG_VECTOR_STORE_PROVIDER"] = "memory"
os.environ["RAG_NPC_PROVIDER"] = "local"
