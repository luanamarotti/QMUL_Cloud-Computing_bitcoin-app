import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("cryptodb.sqlite3")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # rows behave like dicts
    return conn


def _convert_placeholders(sql: str) -> str:
    """
    Convert Postgres-style %s placeholders to SQLite ? placeholders.
    """
    return sql.replace("%s", "?")


def query_all(sql, params=None):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(_convert_placeholders(sql), params or [])
        rows = cur.fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def query_one(sql, params=None):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(_convert_placeholders(sql), params or [])
        row = cur.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def execute(sql, params=None):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(_convert_placeholders(sql), params or [])
        conn.commit()
        return cur.rowcount
    finally:
        conn.close()


# ---------- DB INIT (run once on import) ----------

def init_db():
    conn = get_connection()
    try:
        cur = conn.cursor()

        # users table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                email TEXT
            );
            """
        )

        # coins table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS coins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL UNIQUE,
                name TEXT
            );
            """
        )

        # favourites table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS favourites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                coin_id INTEGER NOT NULL,
                added_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

        # seed one user (id = 1) if table empty
        cur.execute("SELECT COUNT(*) AS c FROM users;")
        if cur.fetchone()["c"] == 0:
            cur.execute(
                "INSERT INTO users (username, email) VALUES (?, ?);",
                ("testuser", "test@example.com"),
            )

        # seed some coins if empty
        cur.execute("SELECT COUNT(*) AS c FROM coins;")
        if cur.fetchone()["c"] == 0:
            cur.executemany(
                "INSERT INTO coins (symbol, name) VALUES (?, ?);",
                [
                    ("btc", "Bitcoin"),
                    ("eth", "Ethereum"),
                    ("sol", "Solana"),
                ],
            )

        conn.commit()
    finally:
        conn.close()


# Run initialization when module is imported
init_db()
