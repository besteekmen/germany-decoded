from germany_decoded.db.connection import get_connection

def save_conversation(record):
    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                INSERT INTO conversations (
                    question,
                    answer,
                    model,
                    instructions,
                    context,
                    prompt,
                    prompt_tokens,
                    completion_tokens,
                    total_tokens,
                    cost,
                    search_time,
                    llm_time,
                    total_time
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s,
                    %s, %s, %s,
                    %s,
                    %s, %s, %s
                )
                RETURNING id;
                """,
                (
                    record.question,
                    record.answer,
                    record.model,
                    record.instructions,
                    record.context,
                    record.prompt,
                    record.prompt_tokens,
                    record.completion_tokens,
                    record.total_tokens,
                    record.cost,
                    record.search_time,
                    record.llm_time,
                    record.total_time,
                ),
            )

            conversation_id = cur.fetchone()[0]

        conn.commit()
        
    return conversation_id