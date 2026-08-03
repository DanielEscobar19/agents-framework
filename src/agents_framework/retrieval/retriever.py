from qdrant_client.models import Filter

from agents_framework.embeddings.ollama_embedder import OllamaEmbedder
from agents_framework.retrieval.metadata_factory import MetadataFactory
from agents_framework.models.search_result import SearchResult
from agents_framework.storage.qdrant_service import QdrantService


class Retriever:

    def __init__(self, config):

        self.embedder = OllamaEmbedder(config)
        self.qdrant = QdrantService(config)
        self.score_threshold = config.score_threshold

    def search(
        self,
        query: str,
        limit: int = 10,
        query_filter: Filter | None = None,
        min_score: float | None = None,
    ) -> list[SearchResult]:

        threshold = min_score if min_score is not None else self.score_threshold

        vector = self.embedder.embed(query)

        response = self.qdrant.client.query_points(
            collection_name=self.qdrant.collection_name,
            query=vector,
            query_filter=query_filter,
            limit=limit,
        )

        results = []

        for point in response.points:

            if point.score < threshold:
                continue

            payload = point.payload

            metadata = MetadataFactory.build(payload["metadata"])

            results.append(
                SearchResult(
                    score=point.score,
                    text=payload["text"],
                    file=payload["file"],
                    start_line=payload["start_line"],
                    end_line=payload["end_line"],
                    element_type=payload["element_type"],
                    metadata=metadata,
                )
            )

        return results
