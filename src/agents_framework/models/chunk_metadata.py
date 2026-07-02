from dataclasses import dataclass


@dataclass
class ChunkMetadata:
    file_path: str
    file_extension: str
    relative_path: str
    symbol_name: str | None = None
    symbol_type: str | None = None
    chunk_hash: str | None = None
    language: str = ""
