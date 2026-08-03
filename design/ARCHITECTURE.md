```text
                          User
                            │
                            ▼
                  GitHub Copilot Agent
                            │
                            ▼
                   Intent Classification
                            │
                            ▼
               Planner Agent (GPT-5-mini)
                            │
            ┌───────────────┴───────────────┐
            ▼                               ▼
     Dependency Graph                Vector Retrieval
            │                               │
            └───────────────┬───────────────┘
                            ▼
                   Context Builder
                            │
        ┌───────────────────┴───────────────────┐
        │                                       │
 Project Knowledge Base                 Short Task Memory
        │                                       │
        └───────────────────┬───────────────────┘
                            ▼
                   Coding Agent
                 (Claude / GPT-5)
                            │
                            ▼
                  Verification Agent
                            │
                            ▼
                  Reviewer Agent
                            │
                            ▼
                    Final Response
```

# 🧠 Agents Framework — Local Code Intelligence System

## Overview

This project implements a local AI-powered code understanding system inspired by Copilot-style indexing. It converts a codebase into a searchable semantic memory using embeddings, vector search, and persistent state tracking.

---

# 🏗️ Architecture

The system is composed of 5 main layers:

```
Codebase
   ↓
Indexing Pipeline
   ↓
┌────────────────────────────┐
│ SQLite (State Layer)       │ ← tracks file changes
└────────────┬───────────────┘
             ↓
┌────────────────────────────┐
│ Embedding Layer (Ollama)   │ ← converts chunks → vectors
└────────────┬───────────────┘
             ↓
┌────────────────────────────┐
│ Qdrant Vector DB           │ ← semantic storage
└────────────┬───────────────┘
             ↓
┌────────────────────────────┐
│ Retrieval Engine           │ ← score-filtered top-k search
│ ContextBuilder             │ ← token-bounded prompt assembly
└────────────┬───────────────┘
             ↓
┌──────────────────────────────────────┐
│ Delivery Layer                       │
│  FastAPI REST  │  MCP Server (stdio) │
└──────────────────────────────────────┘
```

---

---

# ⚙️ Components

## 1. FileScanner

Scans repository and returns files to index.

## 2. Chunker Factory

Selects the correct chunker based on file type:

- PythonChunker (AST-based, with class context on methods)
- CSharpChunker (regex + brace-depth method body extraction)
- MarkdownChunker (heading segmentation with section-path breadcrumb)
- TypeScriptChunker (regex — functions, arrow functions, classes, methods)
- LineChunker (fallback for all other extensions)

## 3. Chunkers

Each chunker produces:

- text
- start_line
- end_line
- element_type
- metadata (language-specific enrichment)

## 4. ChunkNormalizer

Ensures every chunk has:

- deterministic chunk_hash
- file context metadata
- stable identity across re-indexing

## 5. OllamaEmbedder

Generates embeddings using a local model (e.g. nomic-embed-text).

## 6. QdrantService

Handles:

- vector storage
- deletion by file
- semantic search

## 7. RetrievalService

Facade over the Retriever that applies `top_k` from config and filters empty results.

Exposes:

- `retrieve(query)` → ranked `RetrievalContext`
- `build_context(query)` → token-bounded context string via `ContextBuilder`

## 8. ContextBuilder

Assembles retrieved chunks into an LLM-ready context string.

Behavior:

- Deduplicates chunks by `chunk_hash`
- Applies `max_context_tokens` character budget from config
- Formats each chunk with a `# file:start-end [type]` header

## 9. FastAPI REST API

HTTP interface for retrieval and indexing.

Endpoints:

- `POST /retrieval/retrieve` — returns ranked results as JSON
- `POST /retrieval/context` — returns assembled context string
- `POST /indexing/index` — triggers incremental indexer for a given `root_path`

Entrypoint: `python serve.py`

## 10. MCP Server

Exposes retrieval and indexing as MCP tools via stdio transport.

Tools:

- `search_code(query, top_k?)` — semantic chunk search
- `get_context(query)` — token-bounded context string
- `index_codebase(root_path)` — incremental indexer trigger

Compatible with VS Code Copilot and Claude Desktop via stdio MCP configuration.

Entrypoint: `python mcp_server.py`

---

# 🔁 Indexing Pipeline

```text
1.Scan files
2.Compute file hash (md5 of file content)
3.Check SQLite state
   ├─ file not in DB → index
   ├─ hash unchanged → skip
   └─ hash changed → reindex
4.Sync deletions (remove missing files from Qdrant + SQLite)
5.Ensure Qdrant collection exists
6.Select chunker via factory
7.Chunk file into semantic units
8.Normalize chunks (generate chunk_hash)
9.Load old chunk hashes from SQLite
10.Compute diff (`to_add`, `to_delete`)
11.Delete only orphaned chunk IDs from Qdrant (`to_delete`)
12.Embed and upsert only changed/new chunks (`to_add`)
13.Update SQLite file and chunk state
```

---

# 🧠 Incremental Indexing Logic

```python
if state.has_changed(file_path, file_hash):
    old_hashes = state.get_chunk_hashes(file_path)
    new_hashes = {chunk.chunk_hash for chunk in normalized_chunks}
    to_add = new_hashes - old_hashes
    to_delete = old_hashes - new_hashes
    delete_orphan_chunks(to_delete)
    upsert_changed_chunks(to_add)
else:
    skip_file()

```

Ensures:

- no unnecessary embeddings
- fast re-runs
- persistent memory across sessions

Additionally:

```python
sync_deletions(current_files)
```

Ensures deleted files are removed from both:

- SQLite state
- Qdrant vector DB

---

# 🧩 Storage Strategy

## SQLite (Control Plane)

Used for:

- file hashes
- change detection
- deletion tracking
- incremental indexing state

## Qdrant (Memory Layer)

Used for:

- embeddings
- semantic search
- chunk-level retrieval

---

# 🧬 Chunk Identity System

Each chunk has a deterministic identity:

```python
chunk.metadata.chunk_hash = md5(
    file_path + start_line + end_line + element_type + text
)
```

Used as:

- Qdrant point ID
- deduplication key
- stable re-indexing reference

---

# 🚀 Key Design Decisions

### 1. Separation of concerns

- SQLite = control layer (state)
- Chunkers = structure layer
- Normalizer = identity layer
- Qdrant = memory laye

### 2. Language-aware chunking

Each file type has a specialized strategy:

- AST parsing (Python, with parent class tracking)
- Regex + brace-depth body extraction (C#)
- Regex-based function/class/method extraction (TypeScript, JavaScript)
- Heading segmentation with breadcrumb path (Markdown)
- Fallback line chunking (all other types)

### 3. Incremental indexing

Avoids reprocessing unchanged files.

### 4. Deterministic chunk identity

Prevents duplicate embeddings and enables safe updates.

---

# ⚠️ Current Limitations

- No async indexing pipeline
- No embedding cache layer (vectors are re-computed on full rebuild)

---

# 📌 Planning Documents

- Roadmap has been moved to `design/roadmap.md`
- Current RAG state and next steps are in `design/rag-state-and-next-steps.md`

---

# 🧠 Goal

Build a local AI system that can:

- understand entire codebases semantically
- retrieve relevant code instantly
- act as long-term memory for AI agents
- power Copilot-style development workflows

---

# 🧪 Tech Stack

- Python 3.12+
- Qdrant (vector DB)
- SQLite (state tracking)
- Ollama (local embeddings)
- FastAPI + uvicorn (REST API)
- MCP Python SDK (stdio tool server)
- AST + regex parsing
