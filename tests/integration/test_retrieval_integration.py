import pytest

# Representative (query, expected_file_substring) pairs for smoke-testing retrieval quality.
QUERY_EXPECTATIONS = [
    ("what does the indexer do?", "indexer"),
    ("chunking strategy", "chunker"),
    ("incremental indexing", "ARCHITECTURE"),
    ("how are embeddings generated", "ollama"),
]


@pytest.mark.integration
@pytest.mark.parametrize("query,expected_file", QUERY_EXPECTATIONS)
def test_query_returns_relevant_result(query, expected_file):
    from agents_framework.retrieval.retrieval_service import RetrievalService
    from config.config import load_config

    config = load_config()
    service = RetrievalService(config)
    ctx = service.retrieve(query)

    assert ctx.results, f"No results for query: '{query}'"
    files = [r.file.lower() for r in ctx.results]
    assert any(expected_file.lower() in f for f in files), (
        f"Expected a result from a file containing '{expected_file}' for query '{query}'. "
        f"Got: {files}"
    )


@pytest.mark.integration
def test_context_is_non_empty_and_within_token_budget():
    from agents_framework.retrieval.retrieval_service import RetrievalService
    from agents_framework.retrieval.context_builder import ContextBuilder
    from config.config import load_config

    config = load_config()
    service = RetrievalService(config)
    context = service.build_context("incremental indexing")

    assert context.strip()
    # verify character budget is respected
    max_chars = config.max_context_tokens * ContextBuilder._CHARS_PER_TOKEN
    assert len(context) <= max_chars
