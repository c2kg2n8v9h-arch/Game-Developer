$ErrorActionPreference = "Stop"
python -m pytest --cov=rag_service --cov-report=term-missing
