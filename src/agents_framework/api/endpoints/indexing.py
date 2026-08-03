from fastapi import APIRouter, Request

from agents_framework.api.schemas import IndexRequest, IndexResponse
from app import App

router = APIRouter(prefix="/indexing", tags=["indexing"])


@router.post("/index", response_model=IndexResponse)
async def index(body: IndexRequest, request: Request):
    config = request.app.state.config
    app = App(body.root_path, config)
    app.run()
    return IndexResponse(status="ok")
