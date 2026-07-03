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
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chunk_state (
                chunk_hash TEXT PRIMARY KEY,
                file_path TEXT NOT NULL,
                last_indexed INTEGER
            )
        """)
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_chunk_state_file ON chunk_state(file_path)"
        )
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
        return old_hash is None or old_hash != new_hash

    def get_all(self) -> list[dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT file_path, file_hash, last_indexed FROM file_state")
        rows = cursor.fetchall()

        return [
            {
                "file_path": r[0],
                "file_hash": r[1],
                "last_indexed": r[2],
            }
            for r in rows
        ]

    def delete_file(self, file_path: str):
        self.delete_chunks_for_file(file_path)
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM file_state WHERE file_path = ?", (file_path,))
        self.conn.commit()

    def get_all_files(self) -> set[str]:
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT file_path FROM file_state
        """)

        rows = cursor.fetchall()

        return {row[0] for row in rows}

    def get_chunk_hashes(self, file_path: str) -> set[str]:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT chunk_hash FROM chunk_state WHERE file_path = ?", (file_path,)
        )
        return {row[0] for row in cursor.fetchall()}

    def upsert_chunks(self, file_path: str, chunk_hashes: set[str]):
        ts = int(time.time())
        with self.conn:
            self.conn.execute(
                "DELETE FROM chunk_state WHERE file_path = ?", (file_path,)
            )
            if chunk_hashes:
                self.conn.executemany(
                    """
                    INSERT INTO chunk_state (chunk_hash, file_path, last_indexed)
                    VALUES (?, ?, ?)
                    """,
                    [(chunk_hash, file_path, ts) for chunk_hash in chunk_hashes],
                )

    def delete_chunks_for_file(self, file_path: str):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM chunk_state WHERE file_path = ?", (file_path,))
        self.conn.commit()
