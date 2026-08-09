import json
from collections import Counter
from pathlib import Path

from germany_decoded.assistant import Assistant, INSTRUCTIONS
from germany_decoded.evaluation.judge_eval import judge_answer


BENCHMARK_PATH = Path(__file__).with_name("retrieval_benchmark.json")
RESULTS_PATH = Path(__file__).with_name("rag_eval_results.json")


INSTRUCTIONS_V2 = """
You are Germany Decoded, an AI assistant that helps English speakers understand German law.

Rules:

- Answer in clear English.
- Start by directly answering the user's exact question in 1-2 sentences.
- Base every answer ONLY on the provided legal context.
- Do not invent facts, legal rules, exceptions, deadlines, or legal conclusions.
- Do not provide definitive legal advice or make legal decisions.
- Clearly distinguish between what the retrieved context establishes and what it does not establish.
- Do not treat a related legal provision as answering the question unless it actually addresses the issue.
- If the context answers only part of the question, explain which part can be answered and which part cannot.
- If the context is insufficient, say so clearly instead of filling the gap from general knowledge.
- Explain the relevant law in plain English.
- Mention only the legal sections that are relevant to the explanation.
- Include the official source URL(s).
- Keep answers under 250 words unless the user explicitly asks for more detail.

Structure every answer as:

1. Short answer
2. What the retrieved law says
3. Limits or missing information, if applicable
4. Relevant legal sections
5. Official sources
""".strip()


SCORE_MAP = {
    "RELEVANT": 2,
    "PARTLY_RELEVANT": 1,
    "NOT_RELEVANT": 0,
}


def evaluate_version(records, version):
    labels = [
        record[version]["judge"]["relevance"]
        for record in records
    ]

    counts = Counter(labels)

    total_score = sum(
        SCORE_MAP[label]
        for label in labels
    )

    max_score = len(labels) * 2

    return {
        "relevant": counts["RELEVANT"],
        "partly_relevant": counts["PARTLY_RELEVANT"],
        "not_relevant": counts["NOT_RELEVANT"],
        "score": total_score,
        "max_score": max_score,
        "percentage": total_score / max_score,
    }


def print_summary(name, metrics):
    print(
        f"{name:<12}"
        f"{metrics['relevant']:>10}"
        f"{metrics['partly_relevant']:>12}"
        f"{metrics['not_relevant']:>10}"
        f"{metrics['percentage']:>12.2%}"
    )


def main():
    with open(BENCHMARK_PATH, encoding="utf8") as file:
        benchmark = json.load(file)

    assistant_v1 = Assistant(
        instructions=INSTRUCTIONS,
    )

    assistant_v2 = Assistant(
        instructions=INSTRUCTIONS_V2,
    )

    records = []

    for number, entry in enumerate(benchmark, start=1):
        question = entry["question"]

        print()
        print("=" * 80)
        print(f"Question {number}/{len(benchmark)}")
        print(question)
        print("=" * 80)

        # Retrieve once so both prompt versions receive
        # exactly the same legal context.
        results = assistant_v1.search(
            question,
            top_k=3,
        )

        context = assistant_v1.build_context(results)

        prompt_v1 = assistant_v1.build_prompt(
            question,
            context,
        )

        prompt_v2 = assistant_v2.build_prompt(
            question,
            context,
        )

        response_v1 = assistant_v1.llm(prompt_v1)
        response_v2 = assistant_v2.llm(prompt_v2)

        answer_v1 = response_v1.output_text
        answer_v2 = response_v2.output_text

        judge_v1 = judge_answer(
            question,
            answer_v1,
        )

        judge_v2 = judge_answer(
            question,
            answer_v2,
        )

        print()
        print(f"V1: {judge_v1['relevance']}")
        print(f"Reason: {judge_v1['reason']}")

        print()
        print(f"V2: {judge_v2['relevance']}")
        print(f"Reason: {judge_v2['reason']}")

        records.append(
            {
                "question": question,
                "retrieved_sections": [
                    {
                        "law": result["law"],
                        "section": result["section"],
                    }
                    for result in results
                ],
                "v1": {
                    "answer": answer_v1,
                    "judge": judge_v1,
                },
                "v2": {
                    "answer": answer_v2,
                    "judge": judge_v2,
                },
            }
        )

    metrics_v1 = evaluate_version(
        records,
        "v1",
    )

    metrics_v2 = evaluate_version(
        records,
        "v2",
    )

    print()
    print("=" * 80)
    print("RAG PROMPT COMPARISON")
    print("=" * 80)

    print(
        f"{'Prompt':<12}"
        f"{'Relevant':>10}"
        f"{'Partly':>12}"
        f"{'Not Rel.':>10}"
        f"{'Score':>12}"
    )

    print_summary(
        "V1",
        metrics_v1,
    )

    print_summary(
        "V2",
        metrics_v2,
    )

    if metrics_v2["percentage"] > metrics_v1["percentage"]:
        best_prompt = "V2"
    elif metrics_v1["percentage"] > metrics_v2["percentage"]:
        best_prompt = "V1"
    else:
        # Prefer the version with more fully relevant answers
        # if the weighted score is tied.
        best_prompt = (
            "V2"
            if metrics_v2["relevant"] > metrics_v1["relevant"]
            else "V1"
        )

    print()
    print(f"Best RAG prompt: {best_prompt}")

    report = {
        "summary": {
            "v1": metrics_v1,
            "v2": metrics_v2,
            "best_prompt": best_prompt,
        },
        "results": records,
    }

    with open(
        RESULTS_PATH,
        "w",
        encoding="utf8",
    ) as file:
        json.dump(
            report,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print()

if __name__ == "__main__":
    main()