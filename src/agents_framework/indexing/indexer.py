from agents_framework.common.hash_utils import HashUtils
from agents_framework.enums.log_level import LogLevel
from agents_framework.indexing.chunkers.factory import ChunkerFactory
from agents_framework.indexing.normalizer.chunk_normalizer import ChunkNormalizer
from agents_framework.indexing.scanner import FileScanner
from agents_framework.embeddings.ollama_embedder import OllamaEmbedder
from agents_framework.storage.qdrant_service import QdrantService
from agents_framework.storage.sqlite_state import SQLiteState
from qdrant_client.models import Filter, FieldCondition, MatchValue, PointIdsList
from dataclasses import asdict
from agents_framework.util.logger import Logger
from typing import Any


class Indexer:

    def __init__(self, root_path: str, logger: Logger, config: Any):

        self.state = SQLiteState()

        self.scanner = FileScanner(root_path, config)
        self.chunker_factory = ChunkerFactory(config)
        self.normalizer = ChunkNormalizer()

        self.embedder = OllamaEmbedder(config)
        self.qdrant = QdrantService(config)
        self.logger = logger

    # -----------------------------
    # Sync deletions
    # -----------------------------
    def sync_deletions(self, current_files: set[str]):

        tracked_files = self.state.get_all_files()
        deleted_files = tracked_files - current_files

        for file in deleted_files:
            self.logger.log(f"🗑️ Deleting removed file: {file}")

            self.qdrant.client.delete(
                collection_name=self.qdrant.collection_name,
                points_selector=Filter(
                    must=[FieldCondition(key="file", match=MatchValue(value=file))]
                ),
            )

            self.state.delete_file(file)

    # -----------------------------
    # Hashing the file content to detect changes
    # -----------------------------
    def hash_file(self, content: str) -> str:
        return HashUtils.md5(content)

    # -----------------------------
    # Indexing
    # -----------------------------
    def index(self):

        files = self.scanner.scan()
        current_files = set(str(f) for f in files)

        self.sync_deletions(current_files)

        self.logger.log(f"\n📦 Found {len(files)} files\n")

        sample_vector = self.embedder.embed("init")
        self.qdrant.create_collection(len(sample_vector))

        for file in files:

            try:
                content = file.read_text(encoding="utf-8", errors="ignore")
                file_hash = self.hash_file(content)

                # skip unchanged
                if not self.state.has_changed(str(file), file_hash):
                    self.logger.log(f"🟡 Skipping unchanged: {file}", LogLevel.WARNING)

                    continue

                chunker = self.chunker_factory.get(file)
                raw_chunks = chunker.chunk(content, str(file))
                old_hashes = self.state.get_chunk_hashes(str(file))

                if not raw_chunks:
                    if old_hashes:
                        self.qdrant.client.delete(
                            collection_name=self.qdrant.collection_name,
                            points_selector=PointIdsList(points=list(old_hashes)),
                        )

                    self.state.upsert_chunks(str(file), set())
                    self.state.update_file(str(file), file_hash)

                    self.logger.log(
                        f"✅ {file} → +0 embedded, -{len(old_hashes)} deleted, 0 unchanged"
                    )
                    continue

                # Normalize all chunks first so hash-based diffing can run per chunk.
                chunks = [
                    self.normalizer.normalize(str(file), chunk) for chunk in raw_chunks
                ]

                new_hashes = {chunk.metadata.chunk_hash for chunk in chunks}

                to_add = new_hashes - old_hashes
                to_delete = old_hashes - new_hashes

                # log to check how many chunks were created
                self.logger.log(f"🧩 {file} → {len(chunks)} chunks")

                if to_delete:
                    self.qdrant.client.delete(
                        collection_name=self.qdrant.collection_name,
                        points_selector=PointIdsList(points=list(to_delete)),
                    )
                    self.logger.log(f"🗑️ Deleted {len(to_delete)} orphaned chunks")

                added = 0

                for chunk in chunks:

                    if chunk.metadata.chunk_hash not in to_add:
                        continue

                    vector = self.embedder.embed(chunk.text)

                    # SINGLE SOURCE OF TRUTH ID
                    point_id = chunk.metadata.chunk_hash

                    self.qdrant.upsert(
                        vector=vector,
                        point_id=point_id,
                        payload={
                            "chunk_hash": point_id,
                            "text": chunk.text,
                            "file": chunk.metadata.relative_path,
                            "element_type": chunk.element_type,
                            "start_line": chunk.start_line,
                            "end_line": chunk.end_line,
                            "metadata": {
                                "type": type(chunk.metadata).__name__,
                                **asdict(chunk.metadata),
                            },
                        },
                    )

                    added += 1

                self.state.upsert_chunks(str(file), new_hashes)

                self.state.update_file(str(file), file_hash)

                unchanged = len(new_hashes) - added

                self.logger.log(
                    f"✅ {file} → +{added} embedded, -{len(to_delete)} deleted, {unchanged} unchanged"
                )

            except Exception as e:
                self.logger.log(f"❌ Error: {file} → {e}", LogLevel.ERROR)
