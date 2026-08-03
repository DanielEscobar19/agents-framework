import pytest

from agents_framework.retrieval.context_builder import ContextBuilder
from tests.conftest import make_result


def test_empty_results_returns_empty_string():
    cb = ContextBuilder(max_tokens=1000)
    assert cb.build([]) == ""


def test_single_result_contains_header_and_text():
    cb = ContextBuilder(max_tokens=1000)
    r = make_result(
        file="src/foo.py",
        start_line=1,
        end_line=5,
        element_type="function",
        text="def foo(): pass",
    )
    output = cb.build([r])
    assert "# src/foo.py:1-5 [function]" in output
    assert "def foo(): pass" in output


def test_deduplication_by_chunk_hash():
    cb = ContextBuilder(max_tokens=1000)
    r1 = make_result(chunk_hash="same")
    r2 = make_result(chunk_hash="same", text="duplicate")
    output = cb.build([r1, r2])
    assert output.count("same") <= 1


def test_unique_hashes_both_included():
    cb = ContextBuilder(max_tokens=1000)
    r1 = make_result(chunk_hash="aaa", text="first chunk")
    r2 = make_result(chunk_hash="bbb", text="second chunk")
    output = cb.build([r1, r2])
    assert "first chunk" in output
    assert "second chunk" in output


def test_token_budget_truncates_at_boundary():
    # each block is roughly header + text; set budget just big enough for one block
    cb = ContextBuilder(max_tokens=10)  # 40 chars
    r1 = make_result(chunk_hash="aaa", text="short")
    r2 = make_result(chunk_hash="bbb", text="x" * 200)
    output = cb.build([r1, r2])
    assert "short" in output
    assert "x" * 200 not in output


def test_none_chunk_hash_not_deduplicated():
    cb = ContextBuilder(max_tokens=1000)
    r1 = make_result(chunk_hash=None, text="block one")
    r2 = make_result(chunk_hash=None, text="block two")
    output = cb.build([r1, r2])
    # None hashes should not cause the second result to be dropped
    assert "block one" in output
    assert "block two" in output
