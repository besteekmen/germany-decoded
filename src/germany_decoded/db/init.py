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
                    DROP TABLE IF EXISTS conversations;
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

            cur.execute("""
                CREATE INDEX IF NOT EXISTS documents_embedding_idx
                ON documents
                USING hnsw (embedding vector_cosine_ops);
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id SERIAL PRIMARY KEY,

                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,

                    model TEXT NOT NULL,

                    instructions TEXT,
                    context TEXT,
                    prompt TEXT,

                    prompt_tokens INTEGER,
                    completion_tokens INTEGER,
                    total_tokens INTEGER,

                    cost DOUBLE PRECISION,

                    search_time DOUBLE PRECISION,
                    llm_time DOUBLE PRECISION,
                    total_time DOUBLE PRECISION,

                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            conn.commit()

if __name__ == "__main__":
    init_db()