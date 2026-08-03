from pathlib import Path


class FileScanner:

    def __init__(self, root_path: str, config):
        self.root_path = Path(root_path)
        self.allowed_extensions = set(config.allowed_extensions)
        self.ignore_dirs = set(config.ignored_directories)

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
