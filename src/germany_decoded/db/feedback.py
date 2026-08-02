from germany_decoded.db.connection import get_connection


def save_feedback(conversation_id, helpful):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO feedbacks
                (conversation_id, helpful)
                VALUES (%s, %s)
                """,
                (conversation_id, helpful),
            )

        conn.commit()