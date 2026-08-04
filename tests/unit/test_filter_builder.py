import pytest

from agents_framework.api.schemas import SearchFilter
from agents_framework.retrieval.filter_builder import build_filter
from qdrant_client.models import FieldCondition, Filter, MatchValue


def test_none_input_returns_none():
    assert build_filter(None) is None


def test_all_none_fields_returns_none():
    assert build_filter(SearchFilter()) is None


def test_language_filter():
    f = build_filter(SearchFilter(language="python"))
    assert isinstance(f, Filter)
    assert len(f.must) == 1
    cond = f.must[0]
    assert cond.key == "metadata.language"
    assert cond.match.value == "python"


def test_element_type_filter():
    f = build_filter(SearchFilter(element_type="method"))
    assert len(f.must) == 1
    assert f.must[0].key == "element_type"
    assert f.must[0].match.value == "method"


def test_file_path_filter():
    f = build_filter(SearchFilter(file_path="src/foo.py"))
    assert len(f.must) == 1
    assert f.must[0].key == "file"
    assert f.must[0].match.value == "src/foo.py"


def test_class_name_filter():
    f = build_filter(SearchFilter(class_name="MyService"))
    assert f.must[0].key == "metadata.class_name"
    assert f.must[0].match.value == "MyService"


def test_namespace_filter():
    f = build_filter(SearchFilter(namespace="BrandCheck.API"))
    assert f.must[0].key == "metadata.namespace"
    assert f.must[0].match.value == "BrandCheck.API"


def test_multiple_fields_creates_must_conditions():
    f = build_filter(SearchFilter(language="csharp", class_name="MyClass"))
    assert isinstance(f, Filter)
    assert len(f.must) == 2
    keys = {c.key for c in f.must}
    assert keys == {"metadata.language", "metadata.class_name"}


def test_partial_fields_skips_none():
    f = build_filter(SearchFilter(language="typescript", element_type=None))
    assert len(f.must) == 1
    assert f.must[0].key == "metadata.language"
