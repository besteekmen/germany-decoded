from germany_decoded.db.connection import get_connection

def store_documents(documents):
    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute("DELETE FROM documents")

            for doc in documents:
                cur.execute(
                    """
                    INSERT INTO documents
                    (law, section, title, content, source, language)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        doc["law"],
                        doc["section"],
                        doc["title"],
                        doc["content"],
                        doc["source"],
                        doc["language"],
                    ),
                )

        conn.commit()

    print(f"Stored {len(documents)} documents.")
