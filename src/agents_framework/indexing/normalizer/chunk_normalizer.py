from dataclasses import asdict
from agents_framework.common.hash_utils import HashUtils
from agents_framework.models.chunk import Chunk


class ChunkNormalizer:

    def normalize(self, file_path: str, chunk: Chunk) -> Chunk:

        # semantic stable hash (NO index dependency)
        raw = (
            f"{file_path}:"
            f"{chunk.start_line}:{chunk.end_line}:"
            f"{chunk.element_type}:"
            f"{chunk.text}"
        )

        chunk.metadata.chunk_hash = HashUtils.md5(raw)
        chunk.metadata.file_path = file_path

        return chunk
