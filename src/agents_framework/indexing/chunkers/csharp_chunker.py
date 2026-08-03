import re
from agents_framework.models.chunk import Chunk
from agents_framework.models.csharp_chunk_metadata import CSharpChunkMetadata
from .base import IChunker


class CSharpChunker(IChunker):

    CLASS_RE = re.compile(r"\bclass\s+(\w+)")
    METHOD_RE = re.compile(
        r"\b(public|private|protected|internal)\s+[\w<>\[\]]+\s+(\w+)\s*\("
    )

    def chunk(self, text: str, file_path: str) -> list[Chunk]:

        lines = text.splitlines()
        chunks = []

        current_class = None

        for i, line in enumerate(lines):

            # detect class context
            class_match = self.CLASS_RE.search(line)
            if class_match:
                current_class = class_match.group(1)

            # detect method
            method_match = self.METHOD_RE.search(line)
            if method_match:

                method_name = method_match.group(2)

                # scan forward to find the opening brace (within 5 lines)
                body_start = None
                for j in range(i, min(i + 6, len(lines))):
                    if "{" in lines[j]:
                        body_start = j
                        break

                if body_start is not None:
                    depth = 0
                    body_end = body_start
                    for j in range(body_start, len(lines)):
                        depth += lines[j].count("{") - lines[j].count("}")
                        if depth <= 0:
                            body_end = j
                            break
                    chunk_text = "\n".join(lines[i : body_end + 1])
                    end_line = body_end + 1
                else:
                    chunk_text = line
                    end_line = i + 1

                chunks.append(
                    Chunk(
                        text=chunk_text,
                        start_line=i + 1,
                        end_line=end_line,
                        element_type="method",
                        metadata=CSharpChunkMetadata(
                            file_path=file_path,
                            file_extension=".cs",
                            relative_path=file_path,
                            language="csharp",
                            class_name=current_class,
                            method_name=method_name,
                            symbol_name=method_name,
                            symbol_type="method",
                            chunk_hash=None,
                        ),
                    )
                )

        return chunks
