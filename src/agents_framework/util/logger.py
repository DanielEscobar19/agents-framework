from agents_framework.enums.log_level import LogLevel


class Logger:
    def __init__(self, level: LogLevel):
        self.logFile = ""
        self.level = level

    def log(self, message: str, level: LogLevel = LogLevel.INFO):

        if level.value >= self.level.value:
            print(f"[{level.name}] {message}")

    def status(self, message: str):
        print(f"[{LogLevel.INFO.name}] {message}")

    def warning(self, message: str):
        print(f"[{LogLevel.WARNING.name}] {message}")

    def error(self, message: str):
        print(f"[{LogLevel.ERROR.name}] {message}")
