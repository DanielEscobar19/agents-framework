from agents_framework.indexing.indexer import Indexer
from agents_framework.embeddings.ollama_embedder import OllamaEmbedder
from agents_framework.storage.qdrant_service import QdrantService


def main():

    print("Indexing real repository...")

    indexer = Indexer(
        root_path="C:/Users/danescob3/Desktop/BrandCheck/agents-framework"
    )

    indexer.index()

    print("\nDone indexing ✔")


if __name__ == "__main__":
    main()
