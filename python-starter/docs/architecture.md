# Architecture decisions

- **Domain** owns entities and provider contracts and has no framework dependencies.
- **Application** coordinates ingestion and query use cases.
- **Infrastructure** implements provider contracts for local or hosted systems.
- **API** validates HTTP data and maps it to application DTOs.
- **Composition root** is the only place selecting concrete providers.

## Production checklist

- Durable vector database, embedding provider, LLM, object storage, and queues
- Identity, tenant authorization, rate limiting, and audit logging
- Malware scanning, PII controls, encryption, and retention policies
- Hybrid retrieval, reranking, prompt versioning, and RAG evaluations
- Structured logs, metrics, traces, SLOs, alerting, and managed secrets
