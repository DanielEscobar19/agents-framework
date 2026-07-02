from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    qdrant_url: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    collection_name: str = os.getenv("COLLECTION_NAME", "codebase")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")


config = Config()
