import json

from dotenv import load_dotenv
from openai import OpenAI

from germany_decoded.db.judge import (
    get_unjudged_conversations,
    save_judge_result,
)

load_dotenv()
client = OpenAI()


JUDGE_INSTRUCTIONS = """
You evaluate answers produced by a German legal information assistant.

Evaluate whether the answer addresses the user's question.

Use exactly one relevance label:

RELEVANT:
The answer directly and sufficiently addresses the question.

PARTLY_RELEVANT:
The answer addresses the question but includes important omissions,
unnecessary information, or some unclear reasoning.

NOT_RELEVANT:
The answer does not address the question or is substantially incorrect.

Return only valid JSON in this exact format:

{
  "relevance": "RELEVANT",
  "reason": "Brief explanation"
}
""".strip()


def judge_answer(question, answer):
    prompt = f"""
Question:
{question}

Answer:
{answer}
""".strip()

    response = client.responses.create(
        model="gpt-5-mini",
        input=[
            {
                "role": "developer",
                "content": JUDGE_INSTRUCTIONS,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    result = json.loads(response.output_text)

    relevance = result["relevance"].strip().upper()
    reason = result["reason"].strip()

    allowed = {
        "RELEVANT",
        "PARTLY_RELEVANT",
        "NOT_RELEVANT",
    }

    if relevance not in allowed:
        raise ValueError(
            f"Unexpected relevance label: {relevance}"
        )

    return {
        "relevance": relevance,
        "reason": reason,
    }


def main():
    conversations = get_unjudged_conversations(
        limit=10,
    )

    if not conversations:
        print("No unjudged conversations found.")
        return

    for conversation_id, question, answer in conversations:
        print("=" * 80)
        print(f"Conversation ID: {conversation_id}")
        print(f"Question: {question}")

        try:
            result = judge_answer(
                question=question,
                answer=answer,
            )

            save_judge_result(
                conversation_id=conversation_id,
                relevance=result["relevance"],
                reason=result["reason"],
            )

            print(f"Result: {result['relevance']}")
            print(f"Reason: {result['reason']}")

        except (json.JSONDecodeError, KeyError, ValueError) as error:
            print(f"Judge failed: {error}")


if __name__ == "__main__":
    main()