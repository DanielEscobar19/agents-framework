from agents_framework.api.schemas import SearchFilter
from agents_framework.retrieval.retrieval_service import RetrievalService
from config.config import Config


def make_search_tools(service: RetrievalService):

    def search_code(
        query: str,
        top_k: int | None = None,
        language: str | None = None,
        element_type: str | None = None,
        file_path: str | None = None,
        class_name: str | None = None,
    ) -> list[dict]:
        """Search the indexed codebase for chunks semantically matching the query."""
        sf = SearchFilter(
            language=language,
            element_type=element_type,
            file_path=file_path,
            class_name=class_name,
        )
        ctx = service.retrieve(query, limit=top_k, search_filter=sf)
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

    def get_context(
        query: str,
        language: str | None = None,
        file_path: str | None = None,
    ) -> str:
        """Return a token-bounded context string assembled from the top matching chunks."""
        sf = SearchFilter(language=language, file_path=file_path)
        return service.build_context(query, search_filter=sf)

    return search_code, get_context
