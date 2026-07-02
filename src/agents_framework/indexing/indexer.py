from agents_framework.indexing.scanner import FileScanner
from agents_framework.indexing.chunker import Chunker
from agents_framework.embeddings.ollama_embedder import OllamaEmbedder
from agents_framework.storage.qdrant_service import QdrantService
from agents_framework.storage.sqlite_state import SQLiteState
from qdrant_client.models import Filter, FieldCondition, MatchValue
import hashlib


class Indexer:

    def __init__(self, root_path: str):

        self.state = SQLiteState()

        self.scanner = FileScanner(root_path)
        self.chunker = Chunker()
        self.embedder = OllamaEmbedder()
        self.qdrant = QdrantService()

    # -----------------------------
    # Chunk ID
    # -----------------------------
    def make_chunk_id(self, file_path: str, chunk_index: int, chunk_text: str) -> str:
        raw = f"{file_path}:{chunk_index}:{chunk_text}"
        return hashlib.md5(raw.encode()).hexdigest()

    # -----------------------------
    # File hash
    # -----------------------------
    def hash_file(self, content: str) -> str:
        return hashlib.md5(content.encode()).hexdigest()

    # -----------------------------
    # Check if file exists in Qdrant
    # -----------------------------
    def qdrant_file_exists(self, file_path: str) -> bool:
        try:
            result = self.qdrant.client.scroll(
                collection_name=self.qdrant.collection_name,
                scroll_filter=Filter(
                    must=[FieldCondition(key="file", match=MatchValue(value=file_path))]
                ),
                limit=1,
            )[0]

            return len(result) > 0

        except Exception:
            return False

    # -----------------------------
    # Main indexing
    # -----------------------------
    def index(self):

        files = self.scanner.scan()

        print(f"\n📦 Found {len(files)} files\n")

        for file in files:

            try:
                print(f"\n📄 Processing file: {file}")

                content = file.read_text(encoding="utf-8", errors="ignore")
                file_hash = self.hash_file(content)

                # -----------------------------
                # Ensure collection exists FIRST
                # -----------------------------
                sample_vector = self.embedder.embed("init")
                self.qdrant.create_collection(len(sample_vector))

                # -----------------------------
                # Skip logic
                # -----------------------------
                file_changed = self.state.has_changed(str(file), file_hash)
                qdrant_exists = self.qdrant_file_exists(str(file))

                if not file_changed and qdrant_exists:
                    print(f"🟡 Skipping unchanged file: {file}")
                    continue

                # -----------------------------
                # Delete old data
                # -----------------------------
                print(f"🔴 Deleting old chunks for: {file}")

                try:
                    self.qdrant.client.delete(
                        collection_name=self.qdrant.collection_name,
                        points_selector=Filter(
                            must=[
                                FieldCondition(
                                    key="file", match=MatchValue(value=str(file))
                                )
                            ]
                        ),
                    )
                    print(f"🧹 Old chunks deleted for: {file}")

                except Exception as e:
                    print(f"⚠️ Delete warning: {e}")

                # -----------------------------
                # Chunking
                # -----------------------------
                chunks = self.chunker.chunk(content)

                if not chunks:
                    print(f"⚠️ No chunks for: {file}")
                    continue

                print(f"🧩 {file} → {len(chunks)} chunks")

                # -----------------------------
                # Embedding + storing
                # -----------------------------
                for chunk_index, chunk in enumerate(chunks):

                    vector = self.embedder.embed(chunk)

                    point_id = self.make_chunk_id(str(file), chunk_index, chunk)

                    print(f"🟢 Chunk {chunk_index} → {point_id}")

                    self.qdrant.upsert(
                        vector=vector,
                        payload={
                            "text": chunk,
                            "file": str(file),
                            "chunk_index": chunk_index,
                            "file_hash": file_hash,
                        },
                        point_id=point_id,
                    )

                    print(f"🔵 Stored chunk {chunk_index}")

                # -----------------------------
                # Save state
                # -----------------------------
                self.state.update_file(str(file), file_hash)

                print(f"✅ Finished file: {file}")

            except Exception as e:
                print(f"❌ Error processing {file}: {e}")
