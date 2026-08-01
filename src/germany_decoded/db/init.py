from germany_decoded.db.connection import get_connection

def init_db():
    """
    Initialize the database by creating the necessary tables.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE EXTENSION IF NOT EXISTS vector;
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id SERIAL PRIMARY KEY,
                    law TEXT NOT NULL,
                    section TEXT NOT NULL,
                    title TEXT,
                    content TEXT NOT NULL,
                    source TEXT,
                    language TEXT
                );
            """)
            conn.commit()

if __name__ == "__main__":
    init_db()