import sqlite3
import os

# Path to the database file
DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'threats.db')

def get_connection():
    """Returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Creates the threats table if it doesn't already exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS threats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            indicator TEXT NOT NULL,
            indicator_type TEXT,
            threat_type TEXT,
            severity TEXT,
            country TEXT,
            description TEXT,
            ai_summary TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

def cleanup_old_threats(days=7):
    """Deletes threat records older than the specified number of days."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM threats
        WHERE timestamp < datetime('now', ?)
    ''', (f'-{days} days',))
    deleted_count = cursor.rowcount
    conn.commit()
    conn.close()
    print(f"Cleaned up {deleted_count} threats older than {days} days.")

if __name__ == "__main__":
    init_db()