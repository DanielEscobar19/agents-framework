from agents_framework.common.hash_utils import HashUtils
from agents_framework.indexing.chunkers.factory import ChunkerFactory
from agents_framework.indexing.normalizer.chunk_normalizer import ChunkNormalizer
from agents_framework.indexing.scanner import FileScanner
from agents_framework.embeddings.ollama_embedder import OllamaEmbedder
from agents_framework.storage.qdrant_service import QdrantService
from agents_framework.storage.sqlite_state import SQLiteState
from qdrant_client.models import Filter, FieldCondition, MatchValue
from dataclasses import asdict


class Indexer:

    def __init__(self, root_path: str):

        self.state = SQLiteState()

        self.scanner = FileScanner(root_path)
        self.chunker_factory = ChunkerFactory()
        self.normalizer = ChunkNormalizer()

        self.embedder = OllamaEmbedder()
        self.qdrant = QdrantService()

    # -----------------------------
    # Sync deletions
    # -----------------------------
    def sync_deletions(self, current_files: set[str]):

        tracked_files = self.state.get_all_files()
        deleted_files = tracked_files - current_files

        for file in deleted_files:

            print(f"🗑️ Deleting removed file: {file}")

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

        print(f"\n📦 Found {len(files)} files\n")

        sample_vector = self.embedder.embed("init")
        self.qdrant.create_collection(len(sample_vector))

        for file in files:

            try:
                content = file.read_text(encoding="utf-8", errors="ignore")
                file_hash = self.hash_file(content)

                # skip unchanged
                if not self.state.has_changed(str(file), file_hash):
                    print(f"🟡 Skipping unchanged: {file}")
                    continue

                chunker = self.chunker_factory.get(file)
                chunks = chunker.chunk(content, str(file))

                if not chunks:
                    continue

                print(f"🧩 {file} → {len(chunks)} chunks")

                for chunk in chunks:

                    # LAYER 2: normalize
                    chunk = self.normalizer.normalize(str(file), chunk)

                    vector = self.embedder.embed(chunk.text)

                    # SINGLE SOURCE OF TRUTH ID
                    point_id = chunk.metadata.chunk_hash

                    self.qdrant.upsert(
                        vector=vector,
                        point_id=point_id,
                        payload={
                            "text": chunk.text,
                            "file": str(file),
                            "element_type": chunk.element_type,
                            "start_line": chunk.start_line,
                            "end_line": chunk.end_line,
                            "metadata": asdict(chunk.metadata),
                        },
                    )

                self.state.update_file(str(file), file_hash)

                print(f"✅ Finished: {file}")

            except Exception as e:
                print(f"❌ Error: {file} → {e}")
