---
title: RAG System State and Next Steps
description: Current implementation status and immediate next actions for the BrandCheck agents-framework RAG system
author: BrandCheck Team
ms.date: 2026-07-03
ms.topic: how-to
keywords:
  - rag
  - retrieval
  - indexing
  - next steps
estimated_reading_time: 6
---

## Current State

The system currently behaves as an indexing and semantic storage foundation for RAG, not a complete RAG runtime yet.

### What is implemented

- File scanning and extension-aware filtering
- Language-specific chunk generation
- Deterministic chunk identity (`chunk_hash`)
- Local embedding generation with Ollama
- Vector persistence and deletion in Qdrant
- SQLite state management for file and chunk tracking
- Incremental indexing with chunk-level add/update/delete behavior
- Deleted file synchronization across SQLite and Qdrant

### What is not implemented yet

- Retrieval API layer for user queries
- Ranking and context assembly pipeline
- MCP server tools for retrieval/indexing operations
- End-to-end RAG request flow (`question -> retrieve -> rank -> context -> answer`)

## How the current indexing helps RAG

The current pipeline already provides the core memory substrate required by RAG:

- Chunks are normalized into stable identities
- Changed chunks are selectively re-embedded
- Removed chunks are removed from vector storage
- Unchanged chunks are not reprocessed

This keeps vector memory consistent and efficient, which is a prerequisite for good retrieval quality.

## Immediate Next Steps

1. Implement retrieval service

- Add a retrieval module that accepts a query, generates query embeddings, and fetches top-k chunks from Qdrant

2. Implement context builder

- Assemble retrieved chunks into LLM-ready context with de-duplication and token-aware truncation

3. Add retrieval validation

- Add evaluation checks for retrieval precision and relevance over representative repository queries

4. Add embedding cache

- Cache vectors by `chunk_hash` to avoid duplicate embedding calls across rebuilds and repeated indexing operations

5. Expose MCP interface

- Add MCP tools for indexing and retrieval operations to integrate with Copilot and other agent runtimes

## Suggested Build Order

- Milestone A: Retrieval and context builder
- Milestone B: MCP tool surface
- Milestone C: Evaluation harness and optimization (cache, ranking improvements)

## Acceptance Criteria for RAG Readiness

- Query returns relevant chunks with measurable precision targets
- Context builder produces deterministic, bounded prompt context
- MCP tools can invoke retrieval and indexing without manual intervention
- Index and retrieval paths pass smoke and regression scenarios
