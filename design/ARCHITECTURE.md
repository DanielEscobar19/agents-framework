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

---

# ⚙️ Components

## 1. FileScanner

Scans repository and returns files to index.

## 2. Chunker Factory

Selects the correct chunker based on file type:

- PythonChunker (AST-based)
- CSharpChunker (regex + structure heuristics)
- MarkdownChunker (heading-based segmentation)
- LineChunker (fallback strategy)

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

## 7. SQLiteState

Stores file-level metadata:

- file path
- file hash
- last indexed timestamp

Used for incremental indexing and change detection.

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
6.Delete old vectors for changed files
7.Select chunker via factory
8.Chunk file into semantic units
9.Normalize chunks (generate chunk_hash)
10.Embed chunks
11.Store in Qdrant with deterministic ID
12.Update SQLite state
```

---

# 🧠 Incremental Indexing Logic

```python
if state.has_changed(file_path, file_hash):
    reindex_file()
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

- AST parsing (Python)
- Regex structure detection (C#)
- heading segmentation (Markdown)
- fallback line chunking

### 3. Incremental indexing

Avoids reprocessing unchanged files.

### 4. Deterministic chunk identity

Prevents duplicate embeddings and enables safe updates.

---

# ⚠️ Current Limitations

- No chunk-level diffing (full file re-embedding on change)
- No async indexing pipeline
- No embedding cache layer
- No retrieval API yet

---

# 🔮 Roadmap

## Phase 1 (DONE)

- indexing pipeline
- chunking system
- embedding layer
- Qdrant integration
- SQLite state tracking
- deletion sync

## Phase 2 (NEXT)

- chunk-level diff detection
- smarter incremental updates (partial reindex)
- embedding caching layer

## Phase 3

- retrieval API (RAG engine)
- context builder

## Phase 4

- MCP server integration
- agent tool exposure

## Phase 5

- VS Code Copilot-style integration

---

# 🧠 Goal

Build a local AI system that can:

- understand entire codebases semantically
- retrieve relevant code instantly
- act as long-term memory for AI agents
- power Copilot-style development workflows

---

# 🧪 Tech Stack

- Python
- Qdrant (vector DB)
- SQLite (state tracking)
- Ollama (local embeddings)
- AST + regex parsing
- VSCode (future MCP integration)
