import argparse

from agents_framework.indexing.indexer import Indexer
from agents_framework.embeddings.ollama_embedder import OllamaEmbedder
from agents_framework.storage.qdrant_service import QdrantService
from config.config import load_config
from app import App


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root_path", help="Repository to index")

    args = parser.parse_args()

    config = load_config()

    app = App(args.root_path, config)
    app.run()

    # print("Indexing real repository...")

    # indexer = Indexer(
    #     root_path="C:/Users/danescob3/Desktop/BrandCheck/agents-framework"
    # )

    # indexer.index()

    # print("\nDone indexing ✔")


if __name__ == "__main__":
    main()
