from agents_framework.indexing.indexer import Indexer
from agents_framework.util.logger import Logger
from agents_framework.enums.log_level import LogLevel


class App:
    def __init__(self, root_path, config):
        self.config = config

        self.logger = Logger(LogLevel[config.logging_level.upper()])

        self.indexer = Indexer(
            root_path=root_path, logger=self.logger, config=self.config
        )
        self.root_path = root_path

    def run(self):
        self.logger.status(f"Starting indexing with root_path {self.root_path}")
        self.indexer.index()
        self.logger.status("Done indexing ✔")
