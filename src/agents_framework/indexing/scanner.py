from pathlib import Path


class FileScanner:

    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        # this is a tets

        self.allowed_extensions = {
            ".cs",
            ".ts",
            ".js",
            ".py",
            ".java",
            ".md",
            ".json",
            ".html",
            ".css",
        }

        self.ignore_dirs = {
            ".venv",
            "venv",
            "env",
            ".env",
            "node_modules",
            "bin",
            "obj",
            ".git",
            "dist",
            "build",
            "__pycache__",
        }

    def scan(self):

        files = []

        for path in self.root_path.rglob("*"):

            if path.is_dir():
                continue

            if any(part in self.ignore_dirs for part in path.parts):
                continue

            if path.suffix not in self.allowed_extensions:
                continue

            files.append(path)

        return files
