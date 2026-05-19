import sqlite3

DB_NAME = "voice_agent.db"


def get_connection():

    return sqlite3.connect(
        DB_NAME
    )


def init_db():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sessions (

            session_id TEXT PRIMARY KEY,

            full_name TEXT,
            dob TEXT,
            pan TEXT,
            address TEXT,

            transcript TEXT,

            status TEXT
        )
        """
    )

    conn.commit()

    conn.close()