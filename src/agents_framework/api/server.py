from contextlib import asynccontextmanager

from fastapi import FastAPI

from agents_framework.api.endpoints.indexing import router as indexing_router
from agents_framework.api.endpoints.retrieval import router as retrieval_router
from agents_framework.retrieval.retrieval_service import RetrievalService
from config.config import load_config


@asynccontextmanager
async def lifespan(app: FastAPI):
    config = load_config()
    app.state.config = config
    app.state.retrieval_service = RetrievalService(config)
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="agents-framework", lifespan=lifespan)
    app.include_router(retrieval_router)
    app.include_router(indexing_router)
    return app


app = create_app()
