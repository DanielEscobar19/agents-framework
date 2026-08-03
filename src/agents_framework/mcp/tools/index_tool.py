from app import App
from config.config import Config


def make_index_tool(config: Config):

    def index_codebase(root_path: str) -> str:
        """Incrementally index a repository at the given path into the vector store."""
        App(root_path, config).run()
        return f"Indexing complete for {root_path}"

    return index_codebase
