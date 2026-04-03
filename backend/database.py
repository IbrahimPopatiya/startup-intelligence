import sqlite3

DATABASE_NAME = "data.db"

def get_connection():
    """Create a connection to the SQLite database."""
    return sqlite3.connect(DATABASE_NAME)

def create_table():
    """Initialize the startups table with all required Phase 7 columns and migrations."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS startups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            mrr INTEGER,
            source TEXT DEFAULT 'Unknown',
            url TEXT DEFAULT 'N/A',
            category TEXT DEFAULT 'Utility/Other',
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Migrations for existing tables
    migration_columns = [
        ("source", "TEXT", "'Unknown'"),
        ("url", "TEXT", "'N/A'"),
        ("category", "TEXT", "'Utility/Other'")
    ]
    
    for col_name, col_type, default_val in migration_columns:
        try:
            cursor.execute(f"ALTER TABLE startups ADD COLUMN {col_name} {col_type} DEFAULT {default_val}")
        except sqlite3.OperationalError:
            pass

    conn.commit()
    conn.close()

def insert_startup(name, description, mrr, source="Unknown", url="N/A", category="Utility/Other"):
    """Insert a new startup entry with its metadata and category."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO startups (name, description, mrr, source, url, category)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, description, mrr, source, url, category))
    conn.commit()
    conn.close()

def get_latest_startups():
    """
    Retrieve the most recent MRR for each startup.
    Returns: dict mapping name -> mrr.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, mrr FROM startups 
        WHERE id IN (SELECT MAX(id) FROM startups GROUP BY name)
    """)
    rows = cursor.fetchall()
    conn.close()
    return {row[0]: row[1] for row in rows}

def get_all_startup_details():
    """
    Retrieve full details for the most recent entry per startup.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, description, mrr, source, url, category FROM startups 
        WHERE id IN (SELECT MAX(id) FROM startups GROUP BY name)
    """)
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {
            "name": row[0], 
            "description": row[1], 
            "mrr": row[2], 
            "source": row[3],
            "url": row[4],
            "category": row[5]
        }
        for row in rows
    ]
