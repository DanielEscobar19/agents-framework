from pydantic import BaseModel, Field


class IndexRequest(BaseModel):
    root_path: str = Field(..., description="Absolute path to the repository to index")


class IndexResponse(BaseModel):
    status: str


class RetrieveRequest(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int | None = Field(None, gt=0, description="Override configured top_k")


class SearchResultResponse(BaseModel):
    score: float
    file: str
    start_line: int
    end_line: int
    element_type: str
    text: str


class RetrieveResponse(BaseModel):
    query: str
    results: list[SearchResultResponse]


class ContextRequest(BaseModel):
    query: str = Field(..., min_length=1)


class ContextResponse(BaseModel):
    query: str
    context: str
