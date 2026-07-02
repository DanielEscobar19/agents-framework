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

This project implements a local AI-powered code understanding system inspired by Copilot-style indexing. It converts a codebase into a searchable semantic memory using embeddings + vector search + persistent state tracking.

# 🧠 Agents Framework — Local Code Intelligence System

## Overview

This project implements a local AI-powered code understanding system inspired by Copilot-style indexing. It converts a codebase into a searchable semantic memory using embeddings, vector search, and persistent state tracking.

---

# 🏗️ Architecture

The system is composed of 3 main layers:

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
└────────────────────────────┘
```

---

# ⚙️ Components

## 1. FileScanner

Scans repository and returns files to index.

## 2. Chunker

Splits file content into logical chunks for embedding.

## 3. OllamaEmbedder

Generates embeddings using a local model (e.g. `nomic-embed-text`).

## 4. QdrantService

Handles:

- vector storage
- deletion
- semantic search

## 5. SQLiteState

Stores file-level metadata:

- file path
- file hash
- last indexed timestamp

Used for incremental indexing.

---

# 🔁 Indexing Pipeline

```text
1. Scan files
2. Compute file hash
3. Check SQLite state
   ├─ unchanged → skip
   └─ changed → continue
4. Ensure Qdrant collection exists
5. Delete old vectors (if file changed)
6. Chunk file
7. Embed chunks
8. Store in Qdrant
9. Update SQLite state
```

---

# 🧠 Incremental Indexing Logic

```python
if not file_changed and qdrant_exists:
    skip_file()
```

Ensures:

- no unnecessary embeddings
- fast re-runs
- persistent memory across sessions

---

# 🧩 Storage Strategy

## SQLite (Control Layer)

Used for:

- file hashes
- change detection
- indexing state

## Qdrant (Memory Layer)

Used for:

- embeddings
- semantic search
- code retrieval

---

# 🚀 Key Design Decisions

### 1. Separation of concerns

- SQLite = control plane
- Qdrant = semantic memory

### 2. Deterministic chunk IDs

Ensures stable updates:

```python
md5(file_path + chunk_index + chunk_text)
```

### 3. Incremental indexing

Avoids reprocessing unchanged files.

---

# ⚠️ Current Limitations

- No chunk-level diffing yet
- Full file re-embedding on change
- No async pipeline
- No retrieval API (yet)

---

# 🔮 Roadmap

## Phase 1 (DONE)

- indexing pipeline
- embeddings
- Qdrant integration
- SQLite state tracking

## Phase 2 (NEXT)

- chunk-level change detection
- embedding optimization

## Phase 3

- retrieval API (RAG engine)

## Phase 4

- MCP server for agents

## Phase 5

- Copilot integration

---

# 🧠 Goal

Build a local AI system that can:

- understand codebases semantically
- retrieve relevant code instantly
- act as backend memory for agents
- integrate with VSCode / Copilot

---

# 🧪 Tech Stack

- Python
- Qdrant (vector DB)
- SQLite (state tracking)
- Ollama (local embeddings)
- VSCode (future MCP integration)

```

```
