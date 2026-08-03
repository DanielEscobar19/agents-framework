from dataclasses import dataclass

from agents_framework.models.chunk_metadata import ChunkMetadata


@dataclass(slots=True)
class SearchResult:
    score: float
    file: str
    text: str
    start_line: int
    end_line: int
    element_type: str
    metadata: ChunkMetadata
    expanded_text: str | None = None
    expanded_start_line: int | None = None
    expanded_end_line: int | None = None
