from agents_framework.models.chunk import Chunk
from agents_framework.models.chunk_metadata import ChunkMetadata
from .base import IChunker


class MarkdownChunker(IChunker):

    def chunk(self, text: str, file_path: str) -> list[Chunk]:

        chunks = []
        lines = text.splitlines()

        current_chunk = []
        start_line = 1

        for i, line in enumerate(lines, start=1):

            # New section starts
            if line.startswith("#"):

                # flush previous chunk
                if current_chunk:
                    chunks.append(
                        Chunk(
                            text="\n".join(current_chunk),
                            start_line=start_line,
                            end_line=i - 1,
                            element_type="section",
                            metadata=ChunkMetadata(
                                file_path=file_path,
                                file_extension=".md",
                                relative_path=file_path,
                                language="markdown",
                                symbol_type="section",
                                symbol_name=None,
                                chunk_hash=None,
                            ),
                        )
                    )

                current_chunk = [line]
                start_line = i

            else:
                current_chunk.append(line)

        # flush last chunk
        if current_chunk:
            chunks.append(
                Chunk(
                    text="\n".join(current_chunk),
                    start_line=start_line,
                    end_line=len(lines),
                    element_type="section",
                    metadata=ChunkMetadata(
                        file_path=file_path,
                        file_extension=".md",
                        relative_path=file_path,
                        language="markdown",
                        symbol_type="section",
                        symbol_name=None,
                        chunk_hash=None,
                    ),
                )
            )

        return chunks
