import ast
from agents_framework.models.chunk import Chunk
from agents_framework.models.python_chunk_metadata import PythonChunkMetadata
from .base import IChunker


class PythonChunker(IChunker):

    def chunk(self, text: str, file_path: str) -> list[Chunk]:

        try:
            tree = ast.parse(text)
        except SyntaxError:
            return self._fallback(text, file_path)

        lines = text.splitlines()
        chunks = []

        for node in tree.body:

            # -------------------------
            # Top-level functions
            # -------------------------
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):

                chunk_text = self._get_source(lines, node)

                chunks.append(
                    Chunk(
                        text=chunk_text,
                        start_line=node.lineno,
                        end_line=getattr(node, "end_lineno", node.lineno),
                        element_type="function",
                        metadata=PythonChunkMetadata(
                            file_path=file_path,
                            file_extension=".py",
                            relative_path=file_path,
                            language="python",
                            function_name=node.name,
                            symbol_name=node.name,
                            symbol_type="function",
                        ),
                    )
                )

            # -------------------------
            # Classes + methods
            # -------------------------
            elif isinstance(node, ast.ClassDef):

                chunk_text = self._get_source(lines, node)

                chunks.append(
                    Chunk(
                        text=chunk_text,
                        start_line=node.lineno,
                        end_line=getattr(node, "end_lineno", node.lineno),
                        element_type="class",
                        metadata=PythonChunkMetadata(
                            file_path=file_path,
                            file_extension=".py",
                            relative_path=file_path,
                            language="python",
                            class_name=node.name,
                            symbol_name=node.name,
                            symbol_type="class",
                        ),
                    )
                )

                for method_node in node.body:
                    if isinstance(method_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        method_text = self._get_source(lines, method_node)
                        chunks.append(
                            Chunk(
                                text=method_text,
                                start_line=method_node.lineno,
                                end_line=getattr(
                                    method_node, "end_lineno", method_node.lineno
                                ),
                                element_type="function",
                                metadata=PythonChunkMetadata(
                                    file_path=file_path,
                                    file_extension=".py",
                                    relative_path=file_path,
                                    language="python",
                                    class_name=node.name,
                                    function_name=method_node.name,
                                    symbol_name=method_node.name,
                                    symbol_type="function",
                                ),
                            )
                        )

        return chunks

    def _get_source(self, lines, node):
        start = node.lineno - 1
        end = getattr(node, "end_lineno", node.lineno)
        return "\n".join(lines[start:end])

    def _fallback(self, text: str, file_path: str):

        return [
            Chunk(
                text=text,
                start_line=1,
                end_line=len(text.splitlines()),
                element_type="file",
                metadata=PythonChunkMetadata(
                    file_path=file_path,
                    file_extension=".py",
                    relative_path=file_path,
                    language="python",
                    symbol_type="file",
                ),
            )
        ]
