from agents_framework.models.chunk_metadata import ChunkMetadata
from agents_framework.models.search_result import SearchResult


def make_result(
    score: float = 0.8,
    file: str = "src/foo.py",
    text: str = "def foo(): pass",
    chunk_hash: str = "abc123",
    start_line: int = 1,
    end_line: int = 5,
    element_type: str = "function",
) -> SearchResult:
    return SearchResult(
        score=score,
        file=file,
        text=text,
        start_line=start_line,
        end_line=end_line,
        element_type=element_type,
        metadata=ChunkMetadata(
            file_path=file,
            file_extension=".py",
            relative_path=file,
            chunk_hash=chunk_hash,
        ),
    )
