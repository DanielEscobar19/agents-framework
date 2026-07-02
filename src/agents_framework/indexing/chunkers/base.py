from abc import ABC, abstractmethod
from agents_framework.models.chunk import Chunk


class IChunker(ABC):

    @abstractmethod
    def chunk(self, text: str, file_path: str) -> list[Chunk]:
        pass
