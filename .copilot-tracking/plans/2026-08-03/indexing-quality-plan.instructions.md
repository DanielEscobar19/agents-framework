# Implementation Plan: Indexing Quality Improvements

## Overview

Improve indexing quality across all chunkers, fix a critical `chunk_size` config bug, add TypeScript/JavaScript chunker coverage, and update documentation.

## Phases

### Phase F1: Config Fix + C# Method Body — [x] Steps below

- [ ] F1-1: Fix `appsettings.json` — change `chunk_size: 1000 → 40`, `chunk_overlap: 100 → 10` (LineChunker uses these as LINE counts; 1000 lines makes most files one huge chunk)
- [ ] F1-2: Fix C# chunker to extract full method body via brace-depth scanning instead of `text=line` (single signature line)

### Phase F2: TypeScript/JavaScript Chunker — [x] Steps below

- [x] F2-1: Create `src/agents_framework/indexing/chunkers/typescript_chunker.py`
- [x] F2-2: Create `src/agents_framework/models/typescript_chunk_metadata.py`
- [x] F2-3: Wire TypeScript chunker into `factory.py` for `.ts` and `.js` extensions

### Phase F3: Markdown + Python Metadata — [x] Steps below

- [x] F3-1: Fix Markdown chunker to use `MarkdownChunkMetadata` and populate `heading`, `heading_level`, and `section_path`
- [x] F3-2: Fix Python chunker to track class context for method chunks (`class_name` currently always `None` for methods inside classes)

### Phase F4: Documentation Updates — [x] Steps below

- [x] F4-1: Update `design/rag-state-and-next-steps.md`
- [x] F4-2: Update `design/TODO.md`
- [x] F4-3: Update `design/roadmap.md`
- [x] F4-4: Update `README.md`

## Validation Commands

```bash
# Unit tests must stay green
pytest tests/unit/ -v

# Smoke test: confirm TS files produce multiple chunks (not one)
python main.py index . && python main.py retrieve --query "React component" --top-k 5

# Smoke test: confirm C# method chunks contain code body
python main.py retrieve --query "method implementation" --top-k 5
```

## Key Files

- `agents-framework/config/appsettings.json`
- `agents-framework/src/agents_framework/indexing/chunkers/csharp_chunker.py`
- NEW: `agents-framework/src/agents_framework/indexing/chunkers/typescript_chunker.py`
- NEW: `agents-framework/src/agents_framework/models/typescript_chunk_metadata.py`
- `agents-framework/src/agents_framework/indexing/chunkers/factory.py`
- `agents-framework/src/agents_framework/indexing/chunkers/markdown_chunker.py`
- `agents-framework/src/agents_framework/indexing/chunkers/python_chunker.py`
- `agents-framework/design/rag-state-and-next-steps.md`
- `agents-framework/design/TODO.md`
- `agents-framework/design/roadmap.md`
- `agents-framework/README.md`
