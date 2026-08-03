<!-- markdownlint-disable-file -->

# Release Changes: Indexing Quality Improvements

**Related Plan**: indexing-quality-plan.instructions.md
**Implementation Date**: 2026-08-03

## Summary

Fixes a critical chunk_size config bug, improves C# method body extraction, adds TypeScript/JavaScript chunker, and fixes Markdown and Python metadata population.

## Changes

### Added

- `src/agents_framework/models/typescript_chunk_metadata.py` — `TypeScriptChunkMetadata` dataclass with `class_name`, `function_name`, `is_arrow_function`
- `src/agents_framework/indexing/chunkers/typescript_chunker.py` — regex-based extraction of functions, arrow functions, classes, and methods from `.ts`/`.js` files; whole-file fallback for type-only files

### Modified

- `config/appsettings.json` — `chunk_size` 1000→40, `chunk_overlap` 100→10 (LineChunker uses these as line counts; previous values produced single-chunk files)
- `src/agents_framework/indexing/chunkers/csharp_chunker.py` — extracts full method body via brace-depth scanning instead of single signature line
- `src/agents_framework/indexing/chunkers/factory.py` — added `.ts`/`.js` → `TypeScriptChunker()`
- `src/agents_framework/indexing/chunkers/markdown_chunker.py` — uses `MarkdownChunkMetadata`; populates `heading`, `heading_level`, `section_path` breadcrumb
- `src/agents_framework/indexing/chunkers/python_chunker.py` — replaced `ast.walk` with `tree.body`/`node.body` iteration; method chunks now carry `class_name`
- `src/agents_framework/models/markdown_chunk_metadata.py` — `section_path` type corrected `list[str] | None` → `str | None`
- `design/rag-state-and-next-steps.md` — updated implemented list
- `design/TODO.md` — checked off Priority 3 chunker items
- `README.md` — updated Current Features list

### Removed

## Additional or Deviating Changes

- `markdown_chunk_metadata.py` `section_path` type annotation fixed from `list[str] | None` to `str | None` — the chunker stores it as a string breadcrumb; the old type was incorrect

## Release Summary

6 files changed, 2 files created. Critical config bug fixed (chunk_size). C# method bodies now indexed as full code, not signatures. TypeScript/JavaScript files now structurally chunked. Markdown and Python metadata fields populated. All 17 unit tests pass.
