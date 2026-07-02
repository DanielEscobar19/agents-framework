from dataclasses import dataclass

from agents_framework.models.chunk_metadata import ChunkMetadata


@dataclass
class PythonChunkMetadata(ChunkMetadata):
    class_name: str | None = None
    function_name: str | None = None

    decorators: list[str] | None = None
    imports: list[str] | None = None
