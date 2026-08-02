from germany_decoded.db.connection import get_connection

def store_documents(documents, embeddings):
    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute("DELETE FROM documents")

            for doc, embedding in zip(documents, embeddings):
                cur.execute(
                    """
                    INSERT INTO documents
                    (law, section, title, content, source, language, embedding)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        doc["law"],
                        doc["section"],
                        doc["title"],
                        doc["content"],
                        doc["source"],
                        doc["language"],
                        embedding.tolist()  # Convert numpy array to list for insertion
                    ),
                )

        conn.commit()
