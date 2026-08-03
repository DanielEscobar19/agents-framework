from dataclasses import dataclass
from agents_framework.models.chunk_metadata import ChunkMetadata


@dataclass
class MarkdownChunkMetadata(ChunkMetadata):
    heading: str | None = None
    heading_level: int | None = None
    section_path: str | None = None  # breadcrumb e.g. "Architecture > Components"
