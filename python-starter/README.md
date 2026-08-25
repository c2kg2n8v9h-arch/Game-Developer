# Enterprise RAG Service

Vendor-neutral Retrieval-Augmented Generation service using domain-driven, hexagonal boundaries.

```text
src/rag_service/
├── api/                 # HTTP routes, schemas, dependency wiring
├── application/         # Ingestion/query use cases and DTOs
├── domain/              # Entities, errors, provider interfaces
├── infrastructure/      # Embedding, vector store, and LLM adapters
├── config/              # Typed environment configuration
└── observability/       # Logging, metrics, tracing boundary
```

Dependencies point inward: `api/infrastructure -> application -> domain`. The domain knows no framework or AI vendor.

## Setup and run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m rag_service
```

Open `http://127.0.0.1:8000/docs`. Ingest with `POST /v1/documents`, then ask with `POST /v1/query`. Run tests with `pytest`.

## World models

`POST /v1/worlds` retrieves relevant indexed context and submits a grounded prompt to a world-model provider. `GET /v1/worlds/{id}` returns job state and generated asset references. The default `local` provider needs no credentials; configure `world_labs` or `nvidia_cosmos` through `.env` for production inference.

Generated manifests are written under `data/worlds/` only when `persist_manifest=true` is passed to the GET endpoint. Large generated assets belong in object storage, not Git.

Production providers implement the protocols in `domain/ports.py` and are selected in `api/dependencies.py`.
