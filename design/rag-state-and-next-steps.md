---
title: RAG System State and Next Steps
description: Current implementation status and immediate next actions for the BrandCheck agents-framework RAG system
author: BrandCheck Team
ms.date: 2026-08-03
ms.topic: how-to
keywords:
  - rag
  - retrieval
  - indexing
  - next steps
estimated_reading_time: 6
---

## Current State

The system is now a functioning RAG runtime with an HTTP API and an MCP server.

### What is implemented

- File scanning with config-driven extension and directory filtering
- Language-specific chunk generation
- Deterministic chunk identity (`chunk_hash`)
- Local embedding generation with Ollama
- Vector persistence and deletion in Qdrant
- SQLite state management for file and chunk tracking
- Incremental indexing with chunk-level add/update/delete behavior
- Deleted file synchronization across SQLite and Qdrant
- Config-driven `score_threshold` filtering in retrieval
- Config-driven `top_k` result limiting
- `ContextBuilder` for token-bounded, deduped LLM prompt assembly
- FastAPI REST API: `POST /retrieval/retrieve`, `POST /retrieval/context`, `POST /indexing/index`
- MCP server with `search_code`, `get_context`, and `index_codebase` tools (stdio transport)
- CLI retrieve command: `python main.py retrieve --query "..."` with `--language`, `--element-type`, `--file-path`, `--class-name`, `--namespace` filter flags
- Soft fallback retrieval when score threshold filters all results
- TypeScript/JavaScript chunker with regex-based function, arrow function, class, and method extraction
- C# chunker now extracts full method bodies via brace-depth scanning
- Markdown chunker populates `heading`, `heading_level`, and `section_path` breadcrumb metadata
- Python chunker tracks parent class context for method chunks (`class_name` on methods)
- Payload filtering via `SearchFilter` (language, element_type, file_path, class_name, namespace) across REST API and MCP tools
- `TypeScriptChunkMetadata` registered in `MetadataFactory` for correct metadata reconstruction

### What is not implemented yet

- Embedding cache keyed by `chunk_hash`
- Ranking pipeline (reranking beyond vector score)
- Automated regression tests for indexing and retrieval transitions
- Async indexing pipeline

## How the current indexing helps RAG

The current pipeline already provides the core memory substrate required by RAG:

- Chunks are normalized into stable identities
- Changed chunks are selectively re-embedded
- Removed chunks are removed from vector storage
- Unchanged chunks are not reprocessed

This keeps vector memory consistent and efficient, which is a prerequisite for good retrieval quality.

## Immediate Next Steps

1. Add embedding cache keyed by `chunk_hash`
2. Add regression tests for indexing and retrieval edge cases
3. Explore reranking strategies to improve result relevance
4. Add async indexing pipeline for large repositories

## Suggested Build Order

- Milestone A: Embedding cache and regression tests
- Milestone B: Reranking and relevance improvements
- Milestone C: Async indexing pipeline

## Acceptance Criteria for RAG Readiness

- Query returns relevant chunks with measurable precision targets
- Context builder produces deterministic, bounded prompt context
- MCP tools can invoke retrieval and indexing without manual intervention
- Index and retrieval paths pass smoke and regression scenarios
