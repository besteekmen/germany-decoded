from germany_decoded.db.connection import get_connection

def get_summary():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    COUNT(*) AS total_questions,
                    AVG(search_time) AS avg_search_time,
                    AVG(llm_time) AS avg_llm_time,
                    AVG(total_time) AS avg_total_time,
                    AVG(total_tokens) AS avg_tokens,
                    AVG(cost) AS avg_cost
                FROM conversations;
            """)

            row = cur.fetchone()

    return {
        "total_questions": row[0],
        "avg_search_time": row[1],
        "avg_llm_time": row[2],
        "avg_total_time": row[3],
        "avg_tokens": row[4],
        "avg_cost": row[5],
    }

def get_feedback_summary():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    COUNT(*) FILTER (WHERE helpful = TRUE),
                    COUNT(*) FILTER (WHERE helpful = FALSE)
                FROM feedbacks;
            """)

            helpful, not_helpful = cur.fetchone()

    return {
        "helpful": helpful,
        "not_helpful": not_helpful,
    }

def get_recent_conversations(limit=20):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    c.id,
                    c.question,
                    c.total_time,
                    c.total_tokens,
                    f.helpful,
                    c.created_at
                FROM conversations c
                LEFT JOIN feedbacks f
                    ON c.id = f.conversation_id
                ORDER BY c.created_at DESC
                LIMIT %s;
            """, (limit,))

            rows = cur.fetchall()

    return rows