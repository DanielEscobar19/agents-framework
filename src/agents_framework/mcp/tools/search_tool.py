from agents_framework.retrieval.retrieval_service import RetrievalService
from config.config import Config


def make_search_tools(service: RetrievalService):

    def search_code(query: str, top_k: int | None = None) -> list[dict]:
        """Search the indexed codebase for chunks semantically matching the query."""
        ctx = service.retrieve(query, limit=top_k)
        return [
            {
                "score": round(r.score, 4),
                "file": r.file,
                "start_line": r.start_line,
                "end_line": r.end_line,
                "element_type": r.element_type,
                "text": r.text,
            }
            for r in ctx.results
        ]

    def get_context(query: str) -> str:
        """Return a token-bounded context string assembled from the top matching chunks."""
        return service.build_context(query)

    return search_code, get_context
