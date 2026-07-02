class Chunker:

    def chunk(self, text: str, max_lines: int = 40):

        lines = text.split("\n")

        chunks = []

        for i in range(0, len(lines), max_lines):
            chunk = "\n".join(lines[i : i + max_lines])

            if chunk.strip():
                chunks.append(chunk)

        return chunks
