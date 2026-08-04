from pydantic import BaseModel, Field


class SearchFilter(BaseModel):
    language: str | None = None
    element_type: str | None = None
    file_path: str | None = None
    class_name: str | None = None
    namespace: str | None = None


class IndexRequest(BaseModel):
    root_path: str = Field(..., description="Absolute path to the repository to index")


class IndexResponse(BaseModel):
    status: str


class RetrieveRequest(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int | None = Field(None, gt=0, description="Override configured top_k")
    filter: SearchFilter | None = None


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
    filter: SearchFilter | None = None


class ContextResponse(BaseModel):
    query: str
    context: str
