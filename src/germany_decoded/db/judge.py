from germany_decoded.db.connection import get_connection


def get_unjudged_conversations(limit=10):
    """
    Return conversations that do not have a judge result yet.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    c.id,
                    c.question,
                    c.answer
                FROM conversations c
                LEFT JOIN judge_results j
                    ON c.id = j.conversation_id
                WHERE j.id IS NULL
                ORDER BY c.created_at DESC
                LIMIT %s;
                """,
                (limit,),
            )

            rows = cur.fetchall()

    return rows


def save_judge_result(
    conversation_id,
    relevance,
    reason,
):
    """
    Save one judge result for a conversation.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO judge_results (
                    conversation_id,
                    relevance,
                    reason
                )
                VALUES (%s, %s, %s)
                ON CONFLICT (conversation_id)
                DO UPDATE SET
                    relevance = EXCLUDED.relevance,
                    reason = EXCLUDED.reason,
                    created_at = CURRENT_TIMESTAMP;
                """,
                (
                    conversation_id,
                    relevance,
                    reason,
                ),
            )

        conn.commit()