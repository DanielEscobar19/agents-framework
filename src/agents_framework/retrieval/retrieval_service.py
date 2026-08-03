from agents_framework.models.retrieval_context import RetrievalContext
from agents_framework.retrieval.context_builder import ContextBuilder
from agents_framework.retrieval.retriever import Retriever


class RetrievalService:

    def __init__(self, config):

        self.config = config
        self.retriever = Retriever(config)
        self.context_builder = ContextBuilder(config.max_context_tokens)

    def retrieve(
        self,
        query: str,
        limit: int | None = None,
    ) -> RetrievalContext:

        results = self.retriever.search(
            query=query,
            limit=limit or self.config.top_k,
        )

        results = self._remove_empty(results)

        return RetrievalContext(
            query=query,
            results=results,
        )

    def build_context(self, query: str) -> str:
        context = self.retrieve(query)
        return self.context_builder.build(context.results)

    def _remove_empty(self, results):

        return [r for r in results if r.text.strip()]
