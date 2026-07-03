---
title: Agents Framework Roadmap
description: Implementation roadmap aligned with the current indexing system and planned RAG evolution
author: BrandCheck Team
ms.date: 2026-07-03
ms.topic: overview
keywords:
  - roadmap
  - rag
  - indexing
  - mcp
estimated_reading_time: 8
---

## Overview

This roadmap reflects the current implementation status and the next phases required to deliver a complete local RAG system.

## Current Phase Status

### Phase 1: Intelligent Indexing (Complete)

Implemented:

- Repository scanning
- Language-aware chunking (Python, C#, Markdown, fallback line chunker)
- Chunk normalization and deterministic chunk hashing
- Local embeddings through Ollama
- Qdrant vector storage integration
- SQLite state tracking
- File-level and chunk-level incremental indexing
- Chunk add, update, and delete synchronization
- Deleted-file synchronization
- Zero-chunk changed-file cleanup path

### Phase 2: Smarter Incremental Indexing (Partially Complete)

Implemented:

- Chunk-level diffing using `to_add`, `to_delete`, and unchanged sets
- Selective embedding only for changed/new chunks
- Orphaned chunk deletion from Qdrant

Remaining:

- Embedding cache keyed by chunk hash
- Optional hash migration strategy (MD5 to SHA-256)
- Automated regression tests for indexing transitions

## Planned Next Phases

### Phase 3: Retrieval Engine (RAG Core)

Goals:

- Implement retrieval service for semantic code lookup
- Add ranking pipeline for better relevance
- Add context builder for LLM-ready prompt context

### Phase 4: MCP Server Tools

Goals:

- Expose indexing and retrieval capabilities as MCP tools
- Support operations such as indexing, semantic search, and context retrieval

### Phase 5: Agent Orchestration

Goals:

- Add planner, retriever, coder, verifier, and reviewer flows
- Connect orchestration to retrieval and context builder

### Phase 6: VS Code and Tooling Integration

Goals:

- Provide repository-aware coding workflows through MCP-compatible clients
- Improve developer interaction loops for assisted coding

## Priority Backlog

1. Build retrieval service and context builder
2. Add embedding cache to reduce repeated embedding work
3. Add regression tests for chunk transition edge cases
4. Expose retrieval/indexing surface through MCP
5. Add dependency-aware context expansion

## Related Documents

- Architecture: design/ARCHITECTURE.md
- Current state and near-term next steps: design/rag-state-and-next-steps.md
