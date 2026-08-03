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
                    language,
                    embedding <=> %s::vector AS distance
                FROM documents
                ORDER BY embedding <=> %s::vector
                LIMIT %s
                """,
                (
                    query_embedding.tolist(),
                    query_embedding.tolist(),
                    limit
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
                "distance": row[6]
            }
        )

    return documents

def keyword_search(query, limit=3):
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
                    language,
                    ts_rank(
                        search_vector,
                        websearch_to_tsquery('german', %s)
                    ) AS score
                FROM documents
                WHERE search_vector @@ websearch_to_tsquery('german', %s)
                ORDER BY score DESC
                LIMIT %s
                """,
                (query, query, limit),
            )

            rows = cur.fetchall()

            print("\nRows from PostgreSQL:")
            for row in rows:
                print(row[1], row[2], row[6])

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
                "score": row[6],
            }
        )

    return documents