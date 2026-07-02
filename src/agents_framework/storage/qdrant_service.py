from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from config.config import config


class QdrantService:

    def __init__(self):
        self.client = QdrantClient(url=config.qdrant_url)
        self.collection_name = config.collection_name

    def create_collection(self, vector_size: int):

        collections = self.client.get_collections().collections
        exists = any(c.name == self.collection_name for c in collections)

        if not exists:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )

    def upsert(self, vector, payload: dict, point_id: int):

        self.client.upsert(
            collection_name=self.collection_name,
            points=[PointStruct(id=point_id, vector=vector, payload=payload)],
        )

    def search(self, vector, limit: int = 5):

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=vector,
            limit=limit,
            with_payload=True,
            with_vectors=False,
        )

        return results.points
