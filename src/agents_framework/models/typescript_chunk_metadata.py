from dataclasses import dataclass

from agents_framework.models.chunk_metadata import ChunkMetadata


@dataclass
class TypeScriptChunkMetadata(ChunkMetadata):
    class_name: str | None = None
    function_name: str | None = None
    is_arrow_function: bool = False
