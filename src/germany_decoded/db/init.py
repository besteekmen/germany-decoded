from germany_decoded.db.connection import get_connection

def init_db(drop=False):
    """
    Initialize the database by creating the necessary tables.
    all-MiniLM-L6-v2 produces 384-dimensional embeddings.

    Set drop=True only to drop the existing table and recreate it. It will delete all existing data.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:

            if drop:
                cur.execute("""
                    DROP TABLE IF EXISTS documents;
                """)

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
                    language TEXT,
                    embedding VECTOR(384)
                );
            """)

            conn.commit()

if __name__ == "__main__":
    init_db()