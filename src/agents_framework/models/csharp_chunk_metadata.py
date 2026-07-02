from dataclasses import dataclass
from agents_framework.models.chunk_metadata import ChunkMetadata


@dataclass
class CSharpChunkMetadata(ChunkMetadata):
    namespace: str | None = None
    class_name: str | None = None
    method_name: str | None = None
