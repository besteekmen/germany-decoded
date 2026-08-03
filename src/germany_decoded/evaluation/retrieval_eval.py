import json
from germany_decoded.retrieval import search_hybrid

# normalize sections for comparison
def normalize_section(section):
    return section.replace("§", "").strip()

# load sample data for evaluation
with open(
    "src/germany_decoded/evaluation/retrieval_benchmark.json",
    encoding="utf8",
) as f:
    benchmark = json.load(f)

correct_at_1 = 0
correct_at_3 = 0
correct_at_5 = 0

for entry in benchmark:
    results = search_hybrid(entry["question"], top_k=5)

    retrieved = [
        (doc["law"], normalize_section(doc["section"]))
        for doc in results
    ]
    retrieved_at_1 = retrieved[:1]
    retrieved_at_3 = retrieved[:3]
    retrieved_at_5 = retrieved[:5]

    expected = [
        (doc["law"], doc["section"])
        for doc in entry["expected"]
    ]

    #hit = any(x in retrieved for x in expected)
    hit1 = any(x in retrieved_at_1 for x in expected)
    hit3 = any(x in retrieved_at_3 for x in expected)
    hit5 = any(x in retrieved_at_5 for x in expected)
    #if hit:
    #    correct += 1

    if hit1:
        correct_at_1 += 1

    if hit3:
        correct_at_3 += 1

    if hit5:
        correct_at_5 += 1

    print("=" * 80)
    print(entry["question"])
    print()

    print("Expected")
    print(expected)

    print()

    print("Retrieved")

    for i, doc in enumerate(retrieved, start=1):
        print(f"{i}. {doc}")

    print()

    #print("✓" if hit else "✗")
    print(f"Hit@1: {'✓' if hit1 else '✗'}")
    print(f"Hit@3: {'✓' if hit3 else '✗'}")
    print(f"Hit@5: {'✓' if hit5 else '✗'}")

#accuracy = correct / len(benchmark)
hit1 = correct_at_1 / len(benchmark)
hit3 = correct_at_3 / len(benchmark)
hit5 = correct_at_5 / len(benchmark)

print()
print(f"Total Questions = {len(benchmark)}")
#print(f"Correct = {correct}")
#print(f"Incorrect = {len(benchmark) - correct}")
#print(f"Hit Rate = {accuracy:.2%}")
print(f"Hit@1 = {hit1:.2%}")
print(f"Hit@3 = {hit3:.2%}")
print(f"Hit@5 = {hit5:.2%}")