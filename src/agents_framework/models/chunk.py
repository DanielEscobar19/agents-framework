from dataclasses import dataclass
from agents_framework.models.chunk_metadata import ChunkMetadata


@dataclass
class Chunk:
    text: str
    start_line: int
    end_line: int
    element_type: str
    metadata: ChunkMetadata
