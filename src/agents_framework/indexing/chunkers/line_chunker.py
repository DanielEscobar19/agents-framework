from agents_framework.models.chunk import Chunk
from agents_framework.models.chunk_metadata import ChunkMetadata
from .base import IChunker


class LineChunker(IChunker):

    def __init__(self, chunk_size: int = 40, overlap: int = 10):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str, file_path: str) -> list[Chunk]:

        lines = text.splitlines()
        chunks = []

        step = self.chunk_size - self.overlap

        for start in range(0, len(lines), step):

            end = min(start + self.chunk_size, len(lines))
            chunk_lines = lines[start:end]

            chunk_text = "\n".join(chunk_lines)

            if not chunk_text.strip():
                continue

            chunks.append(
                Chunk(
                    text=chunk_text,
                    start_line=start + 1,
                    end_line=end,
                    element_type="lines",
                    metadata=ChunkMetadata(
                        file_path=file_path,
                        file_extension=(
                            file_path.split(".")[-1] if "." in file_path else ""
                        ),
                        relative_path=file_path,
                        language="unknown",
                        symbol_name=None,
                        symbol_type="lines",
                        chunk_hash=None,
                    ),
                )
            )

        return chunks
