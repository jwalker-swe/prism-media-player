import sqlite3

DB_PATH = "data/prism.db"

def define_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = define_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS tracks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT NOT NULL UNIQUE,
                title TEXT,
                album TEXT,
                artist TEXT,
                tracknumber INTEGER,
                duration REAL
            )
        """
    )
    conn.commit()
    conn.close()

