$ErrorActionPreference = "Stop"
python -m uvicorn rag_service.api.app:app --reload
