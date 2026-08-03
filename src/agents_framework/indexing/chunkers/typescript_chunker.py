import re
from pathlib import Path

from agents_framework.models.chunk import Chunk
from agents_framework.models.chunk_metadata import ChunkMetadata
from agents_framework.models.typescript_chunk_metadata import TypeScriptChunkMetadata
from .base import IChunker


class TypeScriptChunker(IChunker):

    # function foo( or async function foo(
    FUNC_RE = re.compile(r"^(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*[(<]")
    # const foo = ( or const foo = async (
    ARROW_RE = re.compile(
        r"^(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\("
    )
    # class Foo or export class Foo or abstract class Foo
    CLASS_RE = re.compile(r"^(?:export\s+)?(?:abstract\s+)?class\s+(\w+)")
    # indented method: methodName( — not a keyword, not const/let/var/function
    METHOD_RE = re.compile(
        r"^(\s+)(?!(?:if|else|for|while|switch|return|const|let|var|function|//|/\*)\b)(\w+)\s*\("
    )

    def _scan_brace_body(self, lines: list[str], start: int) -> int:
        """Return the line index (0-based) where the braced body ends."""
        depth = 0
        for j in range(start, len(lines)):
            depth += lines[j].count("{") - lines[j].count("}")
            if depth <= 0 and j >= start:
                return j
        return len(lines) - 1

    def _find_open_brace(
        self, lines: list[str], from_line: int, lookahead: int = 6
    ) -> int | None:
        """Return the first line index containing '{' within lookahead lines."""
        for j in range(from_line, min(from_line + lookahead, len(lines))):
            if "{" in lines[j]:
                return j
        return None

    def chunk(self, text: str, file_path: str) -> list[Chunk]:
        ext = Path(file_path).suffix.lower()
        language = "typescript" if ext == ".ts" else "javascript"

        lines = text.splitlines()
        chunks: list[Chunk] = []
        current_class: str | None = None
        # track class body end to reset current_class
        class_end: int = -1

        for i, line in enumerate(lines):
            stripped = line.strip()

            # reset class context once we've passed its body
            if current_class is not None and i > class_end:
                current_class = None

            # --- class declaration ---
            class_match = self.CLASS_RE.match(stripped)
            if class_match:
                class_name = class_match.group(1)
                body_start = self._find_open_brace(lines, i)
                if body_start is not None:
                    body_end = self._scan_brace_body(lines, body_start)
                    chunk_text = "\n".join(lines[i : body_end + 1])
                    chunks.append(
                        Chunk(
                            text=chunk_text,
                            start_line=i + 1,
                            end_line=body_end + 1,
                            element_type="class",
                            metadata=TypeScriptChunkMetadata(
                                file_path=file_path,
                                file_extension=ext,
                                relative_path=file_path,
                                language=language,
                                class_name=class_name,
                                symbol_name=class_name,
                                symbol_type="class",
                            ),
                        )
                    )
                    current_class = class_name
                    class_end = body_end
                continue

            # --- named function ---
            func_match = self.FUNC_RE.match(stripped)
            if func_match:
                func_name = func_match.group(1)
                body_start = self._find_open_brace(lines, i)
                if body_start is not None:
                    body_end = self._scan_brace_body(lines, body_start)
                    chunk_text = "\n".join(lines[i : body_end + 1])
                    chunks.append(
                        Chunk(
                            text=chunk_text,
                            start_line=i + 1,
                            end_line=body_end + 1,
                            element_type="function",
                            metadata=TypeScriptChunkMetadata(
                                file_path=file_path,
                                file_extension=ext,
                                relative_path=file_path,
                                language=language,
                                function_name=func_name,
                                symbol_name=func_name,
                                symbol_type="function",
                            ),
                        )
                    )
                continue

            # --- arrow function assignment ---
            arrow_match = self.ARROW_RE.match(stripped)
            if arrow_match:
                func_name = arrow_match.group(1)
                # find '=>' to determine body style
                arrow_pos = None
                for j in range(i, min(i + 8, len(lines))):
                    if "=>" in lines[j]:
                        arrow_pos = j
                        break
                if arrow_pos is not None:
                    # check if block body or expression body
                    after_arrow = lines[arrow_pos].split("=>", 1)[1].strip()
                    if after_arrow.startswith("{") or "{" in after_arrow:
                        body_start = self._find_open_brace(lines, arrow_pos)
                        if body_start is not None:
                            body_end = self._scan_brace_body(lines, body_start)
                        else:
                            body_end = arrow_pos
                    else:
                        # expression body: find end of statement (semicolon or end of arrow line)
                        body_end = arrow_pos
                        for j in range(arrow_pos, min(arrow_pos + 4, len(lines))):
                            if ";" in lines[j] or lines[j].strip() == "":
                                body_end = j
                                break
                    chunk_text = "\n".join(lines[i : body_end + 1])
                    chunks.append(
                        Chunk(
                            text=chunk_text,
                            start_line=i + 1,
                            end_line=body_end + 1,
                            element_type="arrow_function",
                            metadata=TypeScriptChunkMetadata(
                                file_path=file_path,
                                file_extension=ext,
                                relative_path=file_path,
                                language=language,
                                function_name=func_name,
                                is_arrow_function=True,
                                symbol_name=func_name,
                                symbol_type="arrow_function",
                            ),
                        )
                    )
                continue

            # --- method inside class ---
            if current_class is not None:
                method_match = self.METHOD_RE.match(line)
                if method_match:
                    method_name = method_match.group(2)
                    # skip constructor keyword handled elsewhere; skip common noise
                    if method_name in (
                        "if",
                        "else",
                        "for",
                        "while",
                        "switch",
                        "return",
                    ):
                        continue
                    body_start = self._find_open_brace(lines, i)
                    if body_start is not None:
                        body_end = self._scan_brace_body(lines, body_start)
                        chunk_text = "\n".join(lines[i : body_end + 1])
                        chunks.append(
                            Chunk(
                                text=chunk_text,
                                start_line=i + 1,
                                end_line=body_end + 1,
                                element_type="method",
                                metadata=TypeScriptChunkMetadata(
                                    file_path=file_path,
                                    file_extension=ext,
                                    relative_path=file_path,
                                    language=language,
                                    class_name=current_class,
                                    function_name=method_name,
                                    symbol_name=method_name,
                                    symbol_type="method",
                                ),
                            )
                        )

        # fallback: if nothing extracted, return the whole file as one chunk
        if not chunks:
            chunks.append(
                Chunk(
                    text=text,
                    start_line=1,
                    end_line=len(lines),
                    element_type="file",
                    metadata=ChunkMetadata(
                        file_path=file_path,
                        file_extension=ext,
                        relative_path=file_path,
                        language=language,
                    ),
                )
            )

        return chunks
