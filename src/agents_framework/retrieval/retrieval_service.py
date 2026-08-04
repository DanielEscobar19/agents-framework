import sys

from agents_framework.models.retrieval_context import RetrievalContext
from agents_framework.retrieval.context_builder import ContextBuilder
from agents_framework.retrieval.filter_builder import build_filter
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
        min_score: float | None = None,
        search_filter=None,
    ) -> RetrievalContext:

        effective_limit = limit or self.config.top_k
        qdrant_filter = build_filter(search_filter)

        results = self.retriever.search(
            query=query,
            limit=effective_limit,
            min_score=min_score,
            query_filter=qdrant_filter,
        )

        results = self._remove_empty(results)

        # soft fallback: retry without threshold so the caller always gets candidates
        if not results and min_score is None:
            print(
                f"[warning] No results above score_threshold={self.config.score_threshold} "
                f"for query '{query}'. Returning best available results.",
                file=sys.stderr,
            )
            results = self.retriever.search(
                query=query,
                limit=effective_limit,
                min_score=0.0,
                query_filter=qdrant_filter,
            )
            results = self._remove_empty(results)

        return RetrievalContext(
            query=query,
            results=results,
        )

    def build_context(self, query: str, search_filter=None) -> str:
        context = self.retrieve(query, search_filter=search_filter)
        return self.context_builder.build(context.results)

    def _remove_empty(self, results):

        return [r for r in results if r.text.strip()]
