from unittest.mock import patch

from config.config import load_config


def test_load_config_field_types():
    config = load_config()
    assert isinstance(config.qdrant_url, str)
    assert isinstance(config.collection_name, str)
    assert isinstance(config.embedding_model, str)
    assert isinstance(config.allowed_extensions, list)
    assert isinstance(config.ignored_directories, list)
    assert isinstance(config.chunk_size, int)
    assert isinstance(config.chunk_overlap, int)
    assert isinstance(config.logging_level, str)
    assert isinstance(config.top_k, int)
    assert isinstance(config.score_threshold, float)
    assert isinstance(config.max_context_tokens, int)


def test_load_config_appsettings_values():
    config = load_config()
    assert config.top_k == 8
    assert config.score_threshold == 0.5
    assert config.max_context_tokens == 12000
    assert ".py" in config.allowed_extensions
    assert ".git" in config.ignored_directories


def test_load_config_env_overrides(monkeypatch):
    monkeypatch.setenv("QDRANT_URL", "http://custom:9999")
    monkeypatch.setenv("COLLECTION_NAME", "my-collection")
    monkeypatch.setenv("EMBEDDING_MODEL", "custom-model")
    config = load_config()
    assert config.qdrant_url == "http://custom:9999"
    assert config.collection_name == "my-collection"
    assert config.embedding_model == "custom-model"


def test_load_config_env_defaults(monkeypatch):
    monkeypatch.delenv("QDRANT_URL", raising=False)
    monkeypatch.delenv("COLLECTION_NAME", raising=False)
    monkeypatch.delenv("EMBEDDING_MODEL", raising=False)
    config = load_config()
    assert config.qdrant_url == "http://localhost:6333"
    assert config.collection_name == "codebase"
    assert config.embedding_model == "nomic-embed-text"
