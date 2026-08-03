from fastapi import APIRouter, Request

from agents_framework.api.schemas import (
    RetrieveRequest,
    RetrieveResponse,
    SearchResultResponse,
    ContextRequest,
    ContextResponse,
)

router = APIRouter(prefix="/retrieval", tags=["retrieval"])


@router.post("/retrieve", response_model=RetrieveResponse)
async def retrieve(body: RetrieveRequest, request: Request):
    service = request.app.state.retrieval_service
    ctx = service.retrieve(body.query, limit=body.top_k)
    return RetrieveResponse(
        query=ctx.query,
        results=[
            SearchResultResponse(
                score=r.score,
                file=r.file,
                start_line=r.start_line,
                end_line=r.end_line,
                element_type=r.element_type,
                text=r.text,
            )
            for r in ctx.results
        ],
    )


@router.post("/context", response_model=ContextResponse)
async def context(body: ContextRequest, request: Request):
    service = request.app.state.retrieval_service
    return ContextResponse(
        query=body.query,
        context=service.build_context(body.query),
    )
