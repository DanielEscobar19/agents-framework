from dataclasses import dataclass

from agents_framework.models.search_result import SearchResult


@dataclass(slots=True)
class RetrievalContext:
    query: str

    results: list[SearchResult]
