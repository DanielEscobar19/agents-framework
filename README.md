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

From the project root:

```bash
python main.py <root_path>
```

Example:

```bash
python main.py .
```

`root_path` is required and points to the repository directory to index.

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

python main.py
```

If you want to index the current repository directory explicitly:

```cmd
python main.py .
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
│       ├── embeddings/
│       ├── indexing/
│       ├── retrieval/
│       ├── storage/
│       ├── models/
│       ├── mcp/
│       └── __init__.py
│
├── .env
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── main.py
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
- retrieval settings (future)
- MCP settings (future)

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

# Roadmap

- Chunk-level incremental indexing
- Smarter chunking strategy
- Metadata extraction (classes, methods, imports)
- Retrieval service (RAG)
- Context builder
- MCP server
- GitHub Copilot integration
- Claude Code integration
- Multi-repository support
- Agent memory
- Performance optimizations
