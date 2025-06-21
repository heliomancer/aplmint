import sqlite3
import datetime

DB_FILE = "bot_log.db"

def get_db_connection():
    """Helper function to create and return a database connection."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database with a simplified query_log table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS query_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT,
            chat_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL  
        )
    """)
    conn.commit()
    conn.close()
    print("Database initialized.")

def log_query(user_id: int, username: str, chat_id: int):
    """Logs the metadata of a user's query."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # datetime.datetime.now().isoformat() is perfect for storing precise timestamps
    timestamp = datetime.datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO query_log (user_id, username, chat_id, timestamp)
        VALUES (?, ?, ?, ?)
    """, (user_id, username, chat_id, timestamp))
    conn.commit()
    conn.close()


def get_user_query_count_today(user_id: int) -> int:
    """Counts how many queries a user has made today."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get the current date in 'YYYY-MM-DD' format.
    today_str = datetime.date.today().isoformat()

    # SQLite's DATE() function can extract the date part from our timestamp string.
    cursor.execute("""
        SELECT COUNT(*) FROM query_log
        WHERE user_id = ? AND DATE(timestamp) = ?
    """, (user_id, today_str))
    
    # fetchone() returns a tuple, e.g., (5,). We want the first element.
    count = cursor.fetchone()[0]
    conn.close()
    return count
