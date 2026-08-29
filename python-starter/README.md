# Lorebound Game AI Stack

Hugging Face-ready game AI service with dataset streaming, semantic memory, durable local storage, structured NPC dialogue, and Unreal/browser connectors.

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

## Isolated setup and run

```powershell
.\scripts\setup_ai.ps1 -Profile runtime
Copy-Item .env.example .env
.\.venv\Scripts\python.exe -m rag_service
```

Use `-Profile full` to additionally install Diffusers, PEFT, TRL, and Evaluate for media generation and fine-tuning. The project-local `.venv` prevents Hugging Face dependencies from conflicting with PlatformIO or global Python tools.

Open `http://127.0.0.1:8000/docs`. Ingest with `POST /v1/documents`, then ask with `POST /v1/query`. Run tests with `pytest`.

Open `http://127.0.0.1:8000/game` to play **Lorebound**, a small browser adventure that streams story rows from Hugging Face and uses them as its world memory.

## AI runtime profiles

The checked-in defaults need no credentials and keep tests fast. `.env.example` enables semantic embeddings and durable SQLite memory:

```dotenv
RAG_EMBEDDING_PROVIDER=sentence_transformers
RAG_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
RAG_VECTOR_STORE_PROVIDER=sqlite
RAG_NPC_PROVIDER=local
```

For hosted NPC dialogue, create a scoped Hugging Face token and change only local `.env`:

```dotenv
RAG_HUGGINGFACE_TOKEN=hf_your_token
RAG_NPC_PROVIDER=huggingface
RAG_HUGGINGFACE_CHAT_MODEL=Qwen/Qwen3-8B
RAG_HUGGINGFACE_INFERENCE_PROVIDER=auto
```

`GET /v1/ai/capabilities` reports the active provider configuration without exposing the token. `POST /v1/ai/npc/turn` returns validated `speech`, `emotion`, `intent`, and proposed `actions`; the game engine remains authoritative for applying actions.

Example NPC turn:

```powershell
Invoke-RestMethod -Method Post http://127.0.0.1:8000/v1/ai/npc/turn `
  -ContentType "application/json" `
  -Body '{"character":"The Cartographer","player_message":"Where does the silver path lead?","state":{"location":"Map End"}}'
```

## Hugging Face datasets

Stream game lore, dialogue, quests, or other text rows from a public Hub dataset into the RAG index:

```powershell
Invoke-RestMethod -Method Post http://127.0.0.1:8000/v1/datasets/hugging-face `
  -ContentType "application/json" `
  -Body '{"dataset_id":"roneneldan/TinyStories","split":"train","text_columns":["text"],"max_rows":100}'
```

The importer streams rows and stops at `max_rows`, so it does not download the entire dataset. For a private or gated dataset, set `RAG_HUGGINGFACE_TOKEN` in `.env`. Dataset terms and licenses still apply to generated game content.

## World models

`POST /v1/worlds` retrieves relevant indexed context and submits a grounded prompt to a world-model provider. `GET /v1/worlds/{id}` returns job state and generated asset references. The default `local` provider needs no credentials; configure `world_labs` or `nvidia_cosmos` through `.env` for production inference.

Generated manifests are written under `data/worlds/` only when `persist_manifest=true` is passed to the GET endpoint. Large generated assets belong in object storage, not Git.

Production providers implement the protocols in `domain/ports.py` and are selected in `api/dependencies.py`.

## Package profiles

| Profile | Components | Purpose |
|---|---|---|
| Base | FastAPI, Datasets, Hub client | API and Hub dataset streaming |
| `ai` | Sentence Transformers, Transformers, Accelerate, Safetensors | Semantic retrieval and model inference |
| `optimization` | ONNX Runtime | Hardware-optimized local inference target |
| `training` | PEFT, TRL, Evaluate | LoRA fine-tuning and automated evaluation |
| `media` | Diffusers, SoundFile | Offline image, texture, audio, and asset workflows |
