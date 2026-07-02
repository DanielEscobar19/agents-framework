from ollama import Client

from config.config import config


class OllamaEmbedder:

    def __init__(self):
        self.client = Client()

    def embed(self, text: str):

        response = self.client.embeddings(model=config.embedding_model, prompt=text)

        return response["embedding"]
