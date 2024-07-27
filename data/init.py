"""Initialize SQLite database"""
import os

from pathlib import Path
from sqlite3 import connect, Connection, Cursor, IntegrityError

conn: Connection | None = None
curs: Cursor | None = None


def get_db(name: str | None = None, reset: bool = False):
    """Connect to SQLite database file"""
    global conn, curs
    if conn:
        if not reset:
            return
        conn = None
    if not name:
        name = os.getenv("LIBRARY_SQLITE_DB")
        top_dir = Path(__file__).resolve().parents[1]  # repo top
        db_dir = top_dir / "db"
        db_name = "library.db"
        db_path = str(db_dir / db_name)
        name = db_path
        #print(name)
    conn = connect(name, check_same_thread=False)
    curs = conn.cursor()


get_db()
