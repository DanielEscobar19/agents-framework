from agents_framework.models.chunk import Chunk
from agents_framework.models.markdown_chunk_metadata import MarkdownChunkMetadata
from .base import IChunker


class MarkdownChunker(IChunker):

    def chunk(self, text: str, file_path: str) -> list[Chunk]:

        chunks = []
        lines = text.splitlines()

        current_chunk: list[str] = []
        start_line = 1
        heading_stack: list[tuple[int, str]] = []
        current_heading: str | None = None
        current_heading_level: int | None = None
        current_section_path: str | None = None

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
                            metadata=MarkdownChunkMetadata(
                                file_path=file_path,
                                file_extension=".md",
                                relative_path=file_path,
                                language="markdown",
                                symbol_type="section",
                                symbol_name=current_heading,
                                chunk_hash=None,
                                heading=current_heading,
                                heading_level=current_heading_level,
                                section_path=current_section_path,
                            ),
                        )
                    )

                level = len(line) - len(line.lstrip("#"))
                heading_text = line.lstrip("#").strip()

                while heading_stack and heading_stack[-1][0] >= level:
                    heading_stack.pop()
                heading_stack.append((level, heading_text))

                current_heading = heading_text
                current_heading_level = level
                current_section_path = " > ".join(h for _, h in heading_stack)

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
                    metadata=MarkdownChunkMetadata(
                        file_path=file_path,
                        file_extension=".md",
                        relative_path=file_path,
                        language="markdown",
                        symbol_type="section",
                        symbol_name=current_heading,
                        chunk_hash=None,
                        heading=current_heading,
                        heading_level=current_heading_level,
                        section_path=current_section_path,
                    ),
                )
            )

        return chunks
