from germany_decoded.db.connection import get_connection

def search_documents(query_embedding, limit=3):
    """
    Search documents using pgvector.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT
                    law,
                    section,
                    title,
                    content,
                    source,
                    language
                FROM documents
                ORDER BY embedding <=> %s::vector
                LIMIT %s
                """,
                (
                    query_embedding.tolist(),
                    limit,
                ),
            )

            rows = cur.fetchall()

    documents = []

    for row in rows:
        documents.append(
            {
                "law": row[0],
                "section": row[1],
                "title": row[2],
                "content": row[3],
                "source": row[4],
                "language": row[5],
            }
        )

    return documents