import sqlite3
from pathlib import Path


def connect(path: str) -> sqlite3.Connection:
    connection = sqlite3.connect(path, timeout=10, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    return connection


def initialize(path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    connection = connect(path)
    try:
        with connection:
            connection.execute("PRAGMA journal_mode=WAL")
            connection.execute("""
                CREATE TABLE IF NOT EXISTS todos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL DEFAULT '',
                    priority TEXT NOT NULL CHECK(priority IN ('low', 'medium', 'high')),
                    due_date TEXT,
                    completed INTEGER NOT NULL DEFAULT 0 CHECK(completed IN (0, 1)),
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
    finally:
        connection.close()
