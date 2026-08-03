from agents_framework.models.search_result import SearchResult


class ContextBuilder:

    # ~4 chars per token is a reliable estimate for code/English
    _CHARS_PER_TOKEN = 4

    def __init__(self, max_tokens: int):
        self.max_chars = max_tokens * self._CHARS_PER_TOKEN

    def build(self, results: list[SearchResult]) -> str:

        seen: set[str | None] = set()
        blocks: list[str] = []
        remaining = self.max_chars

        for result in results:

            chunk_id = result.metadata.chunk_hash
            if chunk_id is not None:
                if chunk_id in seen:
                    continue
                seen.add(chunk_id)

            header = f"# {result.file}:{result.start_line}-{result.end_line} [{result.element_type}]\n"
            block = header + result.text.strip() + "\n"

            if len(block) > remaining:
                break

            blocks.append(block)
            remaining -= len(block)

        return "\n".join(blocks)
