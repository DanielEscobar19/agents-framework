from typing import Type

from agents_framework.models.chunk_metadata import ChunkMetadata
from agents_framework.models.markdown_chunk_metadata import MarkdownChunkMetadata
from agents_framework.models.python_chunk_metadata import PythonChunkMetadata
from agents_framework.models.csharp_chunk_metadata import CSharpChunkMetadata
from agents_framework.models.typescript_chunk_metadata import TypeScriptChunkMetadata


class MetadataFactory:

    _registry: dict[str, Type[ChunkMetadata]] = {
        "ChunkMetadata": ChunkMetadata,
        "MarkdownChunkMetadata": MarkdownChunkMetadata,
        "PythonChunkMetadata": PythonChunkMetadata,
        "CSharpChunkMetadata": CSharpChunkMetadata,
        "TypeScriptChunkMetadata": TypeScriptChunkMetadata,
    }

    @classmethod
    def build(cls, payload: dict) -> ChunkMetadata:

        payload = dict(payload)

        metadata_type = payload.pop("type")

        metadata_class = cls._registry.get(metadata_type)

        if metadata_class is None:
            raise ValueError(f"Unknown metadata type '{metadata_type}'")

        return metadata_class(**payload)
