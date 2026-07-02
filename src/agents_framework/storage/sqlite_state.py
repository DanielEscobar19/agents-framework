import sqlite3
import time


class SQLiteState:

    def __init__(self, db_path="index_state.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS file_state (
                file_path TEXT PRIMARY KEY,
                file_hash TEXT,
                last_indexed INTEGER
            )
        """)
        self.conn.commit()

    # -------------------------
    # Get stored file hash
    # -------------------------
    def get_hash(self, file_path: str):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT file_hash FROM file_state WHERE file_path = ?", (file_path,)
        )
        row = cursor.fetchone()
        return row[0] if row else None

    # -------------------------
    # Upsert file state
    # -------------------------
    def update_file(self, file_path: str, file_hash: str):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO file_state (file_path, file_hash, last_indexed)
            VALUES (?, ?, ?)
            ON CONFLICT(file_path)
            DO UPDATE SET
                file_hash = excluded.file_hash,
                last_indexed = excluded.last_indexed
        """,
            (file_path, file_hash, int(time.time())),
        )
        self.conn.commit()

    # -------------------------
    # Check if file changed
    # -------------------------
    def has_changed(self, file_path: str, new_hash: str) -> bool:
        old_hash = self.get_hash(file_path)
        return old_hash != new_hash
