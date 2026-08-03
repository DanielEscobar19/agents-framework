from dataclasses import dataclass
import json
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    qdrant_url: str
    collection_name: str
    embedding_model: str

    allowed_extensions: list[str]
    ignored_directories: list[str]

    chunk_size: int
    chunk_overlap: int
    logging_level: str

    top_k: int
    score_threshold: float
    max_context_tokens: int


def load_config() -> Config:
    config_file = Path(__file__).with_name("appsettings.json")

    with config_file.open(encoding="utf-8") as f:
        app = json.load(f)

    return Config(
        qdrant_url=os.getenv("QDRANT_URL", "http://localhost:6333"),
        collection_name=os.getenv("COLLECTION_NAME", "codebase"),
        embedding_model=os.getenv("EMBEDDING_MODEL", "nomic-embed-text"),
        allowed_extensions=app["scanner"]["allowed_extensions"],
        ignored_directories=app["scanner"]["ignored_directories"],
        chunk_size=app["chunking"]["chunk_size"],
        chunk_overlap=app["chunking"]["chunk_overlap"],
        logging_level=app.get("logging", {}).get("level", "INFO"),
        top_k=app["retrieval"]["top_k"],
        score_threshold=app["retrieval"]["score_threshold"],
        max_context_tokens=app["mcp"]["max_context_tokens"],
    )


config = load_config()
