from unittest.mock import MagicMock, patch

import pytest

from agents_framework.models.retrieval_context import RetrievalContext
from tests.conftest import make_result


def make_config(
    top_k: int = 5, score_threshold: float = 0.5, max_context_tokens: int = 4000
):
    cfg = MagicMock()
    cfg.top_k = top_k
    cfg.score_threshold = score_threshold
    cfg.max_context_tokens = max_context_tokens
    return cfg


def make_service(config=None, retriever_results=None):
    """Build a RetrievalService with Retriever and Embedder mocked out."""
    from agents_framework.retrieval.retrieval_service import RetrievalService

    cfg = config or make_config()
    svc = RetrievalService.__new__(RetrievalService)
    svc.config = cfg

    from agents_framework.retrieval.context_builder import ContextBuilder

    svc.context_builder = ContextBuilder(cfg.max_context_tokens)

    mock_retriever = MagicMock()
    mock_retriever.search.return_value = (
        retriever_results if retriever_results is not None else []
    )
    svc.retriever = mock_retriever

    return svc, mock_retriever


def test_retrieve_uses_config_top_k_when_no_limit_given():
    cfg = make_config(top_k=7)
    svc, mock_retriever = make_service(config=cfg, retriever_results=[make_result()])
    svc.retrieve("query")
    mock_retriever.search.assert_called_once()
    _, kwargs = mock_retriever.search.call_args
    assert kwargs["limit"] == 7


def test_retrieve_respects_explicit_limit():
    svc, mock_retriever = make_service(retriever_results=[make_result()])
    svc.retrieve("query", limit=3)
    _, kwargs = mock_retriever.search.call_args
    assert kwargs["limit"] == 3


def test_retrieve_passes_min_score_override():
    svc, mock_retriever = make_service(retriever_results=[make_result()])
    svc.retrieve("query", min_score=0.3)
    _, kwargs = mock_retriever.search.call_args
    assert kwargs["min_score"] == 0.3


def test_remove_empty_filters_blank_text():
    blank = make_result(text="   ")
    populated = make_result(text="some code", chunk_hash="xyz")
    svc, _ = make_service(retriever_results=[blank, populated])
    ctx = svc.retrieve("query")
    assert all(r.text.strip() for r in ctx.results)


def test_soft_fallback_fires_when_threshold_drops_all_results(capsys):
    cfg = make_config(score_threshold=0.9)
    svc, mock_retriever = make_service(config=cfg)

    fallback_result = make_result(score=0.4)
    # first call (with threshold) returns empty; second call (min_score=0.0) returns a result
    mock_retriever.search.side_effect = [[], [fallback_result]]

    ctx = svc.retrieve("query")

    assert len(ctx.results) == 1
    assert mock_retriever.search.call_count == 2
    captured = capsys.readouterr()
    assert "warning" in captured.err.lower()


def test_soft_fallback_does_not_fire_when_min_score_explicitly_set():
    svc, mock_retriever = make_service(retriever_results=[])
    svc.retrieve("query", min_score=0.1)
    # when min_score is explicit, no retry should happen
    assert mock_retriever.search.call_count == 1


def test_build_context_returns_string():
    svc, _ = make_service(retriever_results=[make_result(text="def bar(): pass")])
    result = svc.build_context("query")
    assert isinstance(result, str)
    assert "def bar(): pass" in result
