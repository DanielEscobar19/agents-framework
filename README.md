# Agents Framework

A local AI-powered code intelligence framework that indexes repositories, generates embeddings using Ollama, stores semantic vectors in Qdrant, and serves as the foundation for an MCP-compatible retrieval system.

---

# Prerequisites

Before running the project, install:

- Python 3.12+
- Docker Desktop
- Ollama

Verify the installations:

```bash
python --version
docker --version
ollama --version
```

---

# Initial Setup

## 1. Clone the repository

```bash
git clone <repository-url>
cd agents-framework
```

---

## 2. Create a virtual environment

This only needs to be done **once per clone**.

```bash
python -m venv .venv
```

---

## 3. Activate the virtual environment

### Windows (Command Prompt)

```cmd
.venv\Scripts\activate
```

### Windows (PowerShell)

```powershell
.\.venv\Scripts\Activate.ps1
```

You should see:

```text
(.venv)
```

at the beginning of your terminal prompt.

---

## 4. Install the project

Install all dependencies:

```bash
pip install -r requirements.txt
```

Then install the project in **editable mode**:

```bash
pip install -e .
```

This registers the `agents_framework` package with Python so imports like:

```python
from agents_framework.indexing.indexer import Indexer
```

work automatically without needing to configure `PYTHONPATH`.

> **Note:** This requires the `pyproject.toml` file included in the repository.

---

## 5. Configure environment variables

Create a `.env` file in the project root.

Example:

```text
QDRANT_URL=http://localhost:6333

COLLECTION_NAME=codebase

EMBEDDING_MODEL=nomic-embed-text
```

---

## 6. Start Ollama

Ensure Ollama is installed.

Download the embedding model:

```bash
ollama pull nomic-embed-text
```

Verify:

```bash
ollama list
```

---

## 7. Start Qdrant

Start the existing container:

```bash
docker start qdrant
```

Verify:

```bash
docker ps
```

You should see a running container named `qdrant`.

---

# Running the Project

## Indexing

From the project root:

```bash
python main.py index <root_path>
```

Example:

```bash
python main.py index .
```

## Retrieval (CLI)

```bash
python main.py retrieve --query "what does the indexer do?"
```

With top-k override:

```bash
python main.py retrieve --query "chunking strategy" --top-k 5
```

Return assembled context string:

```bash
python main.py retrieve --query "chunking strategy" --context
```

## REST API

Start the FastAPI server:

```bash
python serve.py
```

Endpoints:

- `POST http://localhost:8000/retrieval/retrieve` — returns ranked results
- `POST http://localhost:8000/retrieval/context` — returns assembled context string
- `POST http://localhost:8000/indexing/index` — triggers incremental indexer

Example request body for `/retrieve`:

```json
{ "query": "how does incremental indexing work?", "top_k": 5 }
```

## MCP Server

Start the MCP server (stdio transport):

```bash
python mcp_server.py
```

To wire into VS Code Copilot, add to `.vscode/mcp.json`:

```json
{
  "servers": {
    "agents-framework": {
      "type": "stdio",
      "command": "python",
      "args": ["mcp_server.py"],
      "cwd": "<absolute-path-to-agents-framework>"
    }
  }
}
```

Available MCP tools:

- `search_code(query, top_k?)` — semantic chunk search
- `get_context(query)` — token-bounded context string
- `index_codebase(root_path)` — incremental indexer trigger

---

# Daily Workflow

Once the project has been set up, **do not recreate the virtual environment**.

Each day:

1. Open a terminal.
2. Navigate to the project.
3. Activate the virtual environment.
4. Ensure Qdrant is running.
5. Run the application.

```cmd
cd agents-framework

.venv\Scripts\activate

docker start qdrant

python main.py index .
```

---

# Recreating the Environment

You only need to recreate the virtual environment when:

- cloning the repository on a new machine
- deleting the `.venv` folder
- changing Python versions
- the virtual environment becomes corrupted

Recreate it with:

```bash
python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt

pip install -e .
```

---

# Project Structure

```text
agents-framework/
│
├── config/
│   ├── __init__.py
│   ├── config.py
│   └── appsettings.json
│
├── design/
│
├── src/
│   └── agents_framework/
│       ├── api/
│       │   ├── endpoints/
│       │   ├── schemas.py
│       │   └── server.py
│       ├── embeddings/
│       ├── indexing/
│       ├── mcp/
│       │   └── tools/
│       ├── models/
│       ├── retrieval/
│       │   ├── context_builder.py
│       │   ├── retrieval_service.py
│       │   └── retriever.py
│       ├── storage/
│       └── __init__.py
│
├── .env
├── .gitignore
├── main.py
├── mcp_server.py
├── pyproject.toml
├── requirements.txt
├── serve.py
└── README.md
```

---

# Configuration

## `.env`

Stores machine-specific settings such as:

- Qdrant URL
- collection name
- embedding model

These values should **not** be committed to source control.

---

## `config/appsettings.json`

Stores application configuration such as:

- allowed file extensions
- ignored directories
- chunk size
- chunk overlap
- logging level
- retrieval settings
- MCP settings

This file is version-controlled and shared across all environments.

### Logging Level

Logging is controlled by `logging.level` in `config/appsettings.json`.

Supported values:

- `INFO`
- `WARNING`
- `ERROR`

Example:

```json
"logging": {
   "level": "ERROR"
}
```

Behavior:

- `INFO`: shows info, warning, and error logs
- `WARNING`: shows warning and error logs
- `ERROR`: shows only error logs

---

# Dependencies

Whenever a new package is installed:

```bash
pip install <package>
```

Update the dependency list:

```bash
pip freeze > requirements.txt
```

This ensures anyone cloning the project can install the exact same package versions.

---

# Package Installation

The project uses the standard Python **src layout**.

The `pyproject.toml` file allows the project to be installed in **editable mode**:

```bash
pip install -e .
```

Benefits include:

- No `PYTHONPATH` configuration required.
- Clean imports (`from agents_framework...`).
- Standard Python packaging.
- Better IDE support.
- Easier testing and future publishing.

---

# Current Features

- Repository scanning
- Configurable scanner settings
- Configurable chunking settings
- Local embeddings with Ollama
- Semantic storage with Qdrant
- SQLite state tracking
- Incremental indexing
- Deterministic chunk IDs
- Automatic reindexing of modified files
- Config-driven architecture
- Score-threshold and top-k filtering in retrieval
- Soft fallback retrieval when threshold filters all results
- Token-bounded context assembly
- FastAPI REST API for retrieval and indexing
- MCP server (stdio) for Copilot and Claude Desktop integration
- TypeScript/JavaScript chunker (function, arrow function, class, method)
- C# chunker extracts full method bodies
- Markdown chunker with heading and section-path metadata
- Python chunker tracks class context for methods

---

# Chunk Update Logic

The indexer now works at chunk level for changed files.

For each scanned file:

1. Compute file hash and skip file if unchanged.
2. If changed, chunk and normalize the file to compute deterministic `chunk_hash` per chunk.
3. Read previous chunk hashes for the same file from SQLite `chunk_state`.
4. Compute set diff:
   - `to_add = new_hashes - old_hashes`
   - `to_delete = old_hashes - new_hashes`
5. Delete orphaned chunk IDs in Qdrant using `to_delete`.
6. Embed and upsert only chunks in `to_add`.
7. Persist new chunk hashes in `chunk_state` and refresh file hash in `file_state`.

This gives incremental add, update, and delete behavior without re-embedding unchanged chunks.

---

# Testing

## Unit tests

Run the full unit suite without any external services:

```bash
pytest tests/unit/ -v
```

Unit tests cover:

- `ContextBuilder` — empty input, header format, dedup by `chunk_hash`, `None` hash behavior, token budget truncation
- `RetrievalService` — `top_k` usage, limit override, `min_score` passthrough, empty text filter, soft fallback trigger
- `Config` loading — field types, `appsettings.json` values, environment variable overrides and defaults

All unit tests mock Qdrant and Ollama. No running containers required.

## Integration tests

Require live Qdrant and Ollama with an indexed repository.

```bash
pytest -m integration -v
```

Integration tests run parametrized (query, expected_file) pairs and verify that real retrieval returns relevant chunks. They are excluded from the default test run.

## Test structure

```text
tests/
├── conftest.py           — shared SearchResult factory
├── unit/
│   ├── test_config.py
│   ├── test_context_builder.py
│   └── test_retrieval_service.py
└── integration/
    └── test_retrieval_integration.py
```

---

# Roadmap

- [x] Chunk-level incremental indexing
- [x] Smarter chunking strategy
- [x] Metadata extraction (classes, methods, imports)
- [x] Retrieval service (RAG)
- [x] Context builder
- [x] MCP server
- [x] GitHub Copilot integration
- [x] Claude Code integration
- [ ] Multi-repository support
- [ ] Agent memory
- [ ] Performance optimizations (embedding cache, async pipeline)
