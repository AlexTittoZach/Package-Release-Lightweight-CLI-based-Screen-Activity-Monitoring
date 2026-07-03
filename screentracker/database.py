import sqlite3

from .storage import DB_PATH

def init_db():
    
    conn = sqlite3.connect(DB_PATH)

    # App Usage
    conn.execute("""
        CREATE TABLE IF NOT EXISTS app_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            app_name TEXT,
            window_title TEXT,
            start_time TEXT,
            end_time TEXT,
            duration INTEGER
        )
    """)

    # Idle Usage

    conn.execute("""
        CREATE TABLE IF NOT EXISTS idle_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_time TEXT,
            end_time TEXT,
            duration INTEGER
        )
    """)

    conn.commit()
    conn.close()



# APP TRACKING

def save_usage(
        app_name,
        window_title,
        start_time,
        end_time,
        duration):

    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
        INSERT INTO app_usage (
            app_name,
            window_title,
            start_time,
            end_time,
            duration
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        app_name,
        window_title,
        start_time,
        end_time,
        duration
    ))

    conn.commit()
    conn.close()



# IDLE TRACKING

def save_idle(
        start_time,
        end_time,
        duration):

    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
        INSERT INTO idle_usage (
            start_time,
            end_time,
            duration
        )
        VALUES (?, ?, ?)
    """, (
        start_time,
        end_time,
        duration
    ))

    conn.commit()
    conn.close()