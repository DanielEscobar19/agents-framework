---
title: Agents Framework TODO
description: Prioritized engineering backlog aligned with current indexing and RAG roadmap
author: BrandCheck Team
ms.date: 2026-08-03
ms.topic: how-to
keywords:
	- todo
	- backlog
	- rag
	- indexing
estimated_reading_time: 4
---

## Purpose

This file tracks actionable engineering tasks that are not yet complete.

## Priority 1: RAG Core Delivery

- [x] Implement retrieval API layer for user queries
- [x] Implement ranking and context assembly pipeline
- [x] Implement end-to-end RAG request flow (`question -> retrieve -> rank -> context -> answer`)
- [x] Expose indexing and retrieval operations through MCP tools
- [x] Add payload filtering to retrieval (language, element_type, file_path, class_name, namespace) via `SearchFilter` across API and MCP

## Priority 2: Indexing Performance and Reliability

- [ ] Add embedding cache keyed by `chunk_hash`
- [ ] Add full rebuild index option
- [x] Add configurable logging level from `appsettings`
- [x] Add automated regression tests for indexing and retrieval transitions
- [x] Add indexing-specific transition tests (changed, deleted, zero-chunk)

## Priority 3: Chunker Quality Improvements

- [x] Improve C# chunker — full method body extraction via brace-depth scanning
- [x] Improve Python chunker — class context (`class_name`) now set on method chunks
- [x] Improve Markdown chunker — `heading`, `heading_level`, and `section_path` now populated
- [x] Add TypeScript/JavaScript chunker — regex-based function, arrow function, class, and method extraction
- [ ] Improve fallback line chunker metadata extraction

## Priority 4: Optional Hardening

- [ ] Evaluate migration path from MD5 to SHA-256 for chunk hashing
- [ ] Evaluate async indexing pipeline

## Priority 5: MCP Distribution and Packaging

- [ ] Add `[project.dependencies]` to `pyproject.toml`
- [ ] Add `agents-framework-mcp` console script entry point to `pyproject.toml`
- [ ] Create `src/agents_framework/setup/bootstrap.py` — installs Qdrant container and Ollama model automatically
- [ ] Add `agents-framework-setup` console script entry point
- [ ] Update `README.md` with one-command install instructions for each platform
- [ ] Evaluate `uvx` / PyPI publishing path

## Priority 6: Chunkers per file

- [ ] Add chunker for json files
- [ ] Add chunker for HTML files
- [ ] Add chunker for css/scss files
- [ ] Add chunker for tsx files
- [ ] Improve the C# chunker
- [ ] Improve the Python chunker

## Notes

- Completed chunk-level diffing is intentionally not listed here.
- Roadmap: `design/roadmap.md`
- Current RAG state: `design/rag-state-and-next-steps.md`
