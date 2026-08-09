import json

from germany_decoded.retrieval import search, search_hybrid


BENCHMARK_PATH = (
    "src/germany_decoded/evaluation/retrieval_benchmark.json"
)


def normalize_section(section):
    return section.replace("§", "").strip()


def evaluate_retrieval(name, search_fn, benchmark):
    correct_at_1 = 0
    correct_at_3 = 0
    correct_at_5 = 0
    reciprocal_ranks = []

    print()
    print("=" * 80)
    print(f"{name.upper()} RETRIEVAL")
    print("=" * 80)

    for entry in benchmark:
        results = search_fn(entry["question"], top_k=5)

        retrieved = [
            (doc["law"], normalize_section(doc["section"]))
            for doc in results
        ]

        expected = [
            (doc["law"], normalize_section(doc["section"]))
            for doc in entry["expected"]
        ]

        hit1 = any(doc in expected for doc in retrieved[:1])
        hit3 = any(doc in expected for doc in retrieved[:3])
        hit5 = any(doc in expected for doc in retrieved[:5])

        if hit1:
            correct_at_1 += 1

        if hit3:
            correct_at_3 += 1

        if hit5:
            correct_at_5 += 1

        reciprocal_rank = 0.0

        for rank, doc in enumerate(retrieved, start=1):
            if doc in expected:
                reciprocal_rank = 1 / rank
                break

        reciprocal_ranks.append(reciprocal_rank)

        print()
        print(entry["question"])
        print()
        print("Expected")
        print(expected)
        print()
        print("Retrieved")

        for i, doc in enumerate(retrieved, start=1):
            print(f"{i}. {doc}")

        print()
        print(f"Hit@1: {'✓' if hit1 else '✗'}")
        print(f"Hit@3: {'✓' if hit3 else '✗'}")
        print(f"Hit@5: {'✓' if hit5 else '✗'}")

    total = len(benchmark)

    metrics = {
        "hit@1": correct_at_1 / total,
        "hit@3": correct_at_3 / total,
        "hit@5": correct_at_5 / total,
        "mrr": sum(reciprocal_ranks) / total,
    }

    print()
    print("-" * 80)
    print(f"{name} results")
    print("-" * 80)
    print(f"Total Questions = {total}")
    print(f"Hit@1 = {metrics['hit@1']:.2%}")
    print(f"Hit@3 = {metrics['hit@3']:.2%}")
    print(f"Hit@5 = {metrics['hit@5']:.2%}")
    print(f"MRR = {metrics['mrr']:.3f}")

    return metrics


def main():
    with open(BENCHMARK_PATH, encoding="utf8") as f:
        benchmark = json.load(f)

    semantic_metrics = evaluate_retrieval(
        "Semantic",
        search,
        benchmark,
    )

    hybrid_metrics = evaluate_retrieval(
        "Hybrid",
        search_hybrid,
        benchmark,
    )

    print()
    print("=" * 80)
    print("RETRIEVAL COMPARISON")
    print("=" * 80)
    print(
        f"{'Method':<15}"
        f"{'Hit@1':>10}"
        f"{'Hit@3':>10}"
        f"{'Hit@5':>10}"
        f"{'MRR':>10}"
    )

    for name, metrics in [
        ("Semantic", semantic_metrics),
        ("Hybrid", hybrid_metrics),
    ]:
        print(
            f"{name:<15}"
            f"{metrics['hit@1']:>10.2%}"
            f"{metrics['hit@3']:>10.2%}"
            f"{metrics['hit@5']:>10.2%}"
            f"{metrics['mrr']:>10.3f}"
        )

    # The production assistant sends the top 3 retrieved documents
    # to the LLM, so Hit@3 is the primary selection metric.
    if hybrid_metrics["hit@3"] > semantic_metrics["hit@3"]:
        best_method = "Hybrid"
    elif semantic_metrics["hit@3"] > hybrid_metrics["hit@3"]:
        best_method = "Semantic"
    else:
        # Use MRR as a tiebreaker.
        best_method = (
            "Hybrid"
            if hybrid_metrics["mrr"] >= semantic_metrics["mrr"]
            else "Semantic"
        )

    print()
    print(f"Best retrieval method: {best_method}")
    print("Production retrieval method: Hybrid")

    if best_method == "Hybrid":
        print("✓ Production uses the best evaluated retrieval method.")
    else:
        print("⚠ Production does not use the best evaluated method.")


if __name__ == "__main__":
    main()