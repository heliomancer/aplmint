import sqlite3
import datetime
from . import config

DB_FILE = "bot_log.db"

def get_db_connection():
    """Helper function to create and return a database connection."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes the database with all required tables."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS query_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT,
            chat_id INTEGER NOT NULL,
            model_used TEXT NOT NULL, 
            timestamp TEXT NOT NULL
        )
    """)
    # Table to store user's preferences
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_preferences (
            user_id INTEGER PRIMARY KEY,
            selected_model TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    print("Database initialized.")

# --- log_query ---
def log_query(user_id: int, username: str, chat_id: int, model_used: str):
    """Logs the metadata of a user's query, including the model."""
    conn = get_db_connection()
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO query_log (user_id, username, chat_id, model_used, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, username, chat_id, model_used, timestamp))
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
    
    count = cursor.fetchone()[0]
    conn.close()
    return count


# --- NEW FUNCTIONS ---
def update_user_model(user_id: int, model_name: str):
    """Updates or inserts the user's selected model."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # "INSERT OR REPLACE" is a convenient SQLite command for this
    cursor.execute("""
        INSERT OR REPLACE INTO user_preferences (user_id, selected_model)
        VALUES (?, ?)
    """, (user_id, model_name))
    conn.commit()
    conn.close()

def get_user_model(user_id: int) -> str:
    """Gets the user's last selected model, or returns the default."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT selected_model FROM user_preferences WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return result['selected_model']
    else:
        # Return the first model from the config as the default
        return next(iter(config.models.values()))


