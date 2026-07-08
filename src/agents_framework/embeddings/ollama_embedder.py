from ollama import Client
from typing import Any


class OllamaEmbedder:

    def __init__(self, config: Any):
        self.client = Client()
        self.config = config

    def embed(self, text: str):

        response = self.client.embeddings(
            model=self.config.embedding_model, prompt=text
        )

        return response["embedding"]
