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

## Priority 2: Indexing Performance and Reliability

- [ ] Add embedding cache keyed by `chunk_hash`
- [ ] Add full rebuild index option
- [ ] Add configurable logging level from `appsettings`
- [ ] Add automated regression tests for indexing transitions (changed, deleted, zero-chunk)

## Priority 3: Chunker Quality Improvements

- [ ] Improve C# chunker with parser-based extraction
- [ ] Improve Python chunker metadata extraction
- [ ] Improve Markdown chunker metadata extraction
- [ ] Improve fallback line chunker metadata extraction

## Priority 4: Optional Hardening

- [ ] Evaluate migration path from MD5 to SHA-256 for chunk hashing
- [ ] Evaluate async indexing pipeline

## Notes

- Completed chunk-level diffing is intentionally not listed here.
- Roadmap: `design/roadmap.md`
- Current RAG state: `design/rag-state-and-next-steps.md`
