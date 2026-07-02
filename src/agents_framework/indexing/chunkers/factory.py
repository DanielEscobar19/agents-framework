from pathlib import Path

from .csharp_chunker import CSharpChunker
from .python_chunker import PythonChunker

from .line_chunker import LineChunker
from .markdown_chunker import MarkdownChunker


class ChunkerFactory:

    def __init__(self):
        self.line_chunker = LineChunker()
        self.markdown_chunker = MarkdownChunker()

    def get(self, file_path: str):

        ext = Path(file_path).suffix.lower()

        if ext == ".py":
            return PythonChunker()

        if ext == ".cs":
            return CSharpChunker()

        if ext == ".md":
            return MarkdownChunker()

        return LineChunker()
