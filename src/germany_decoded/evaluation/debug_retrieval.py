import json
from germany_decoded.retrieval import search

with open(
    "src/germany_decoded/evaluation/retrieval_benchmark.json",
    encoding="utf8",
) as f:
    benchmark = json.load(f)

for entry in benchmark:
    results = search(
        entry["question"],
        top_k=3,
    )

    print("=" * 80)
    print(entry["question"])
    print()

    print("Expected")
    for doc in entry["expected"]:
        print(f"{doc['law']} {doc['section']}")
    print()

    print("Retrieved")
    print()
    for i, doc in enumerate(results, start=1):
        print(f"{i}. {doc['law']} {doc['section']}")
        print(f"Distance: {doc['distance']:.4f}")

        if doc["title"]:
            print(doc["title"])

        print()

        preview = doc["content"][:250]
        print(preview)

        print("\n" + "-" * 80)