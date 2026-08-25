from fastapi import FastAPI
from rag_service.api.routes.health import router as health_router
from rag_service.api.routes.rag import router as rag_router
from rag_service.api.routes.worlds import router as worlds_router
from rag_service.config.settings import get_settings
from rag_service.observability.logging import configure_logging


def create_app() -> FastAPI:
    config = get_settings()
    configure_logging(config.log_level)
    app = FastAPI(title=config.app_name, version="0.1.0")
    app.include_router(health_router)
    app.include_router(rag_router)
    app.include_router(worlds_router)
    return app


app = create_app()
