def search(query, documents):
    results = []

    query_words = query.lower().split()

    for doc in documents:
        text = doc["content"].lower()

        score = sum(
            word in text
            for word in query_words
        )

        if score > 0:
            results.append((score, doc))

    results.sort(reverse=True, key=lambda x: x[0])

    return [doc for score, doc in results]