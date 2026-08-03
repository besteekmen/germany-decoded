import numpy as np
import re
from germany_decoded.embeddings import embed_query
from germany_decoded.rewrite import extract_legal_concept
from germany_decoded.db.query import search_documents, keyword_search

def search_numpy(query, documents, embeddings, top_k=3):
    query_embedding = embed_query(query)

    scores = embeddings @ query_embedding

    top_indices = np.argsort(scores)[::-1][:top_k]

    return [
        documents[i]
        for i in top_indices
    ]

def search(query, top_k=3):
    query_embedding = embed_query(query)

    return search_documents(
        query_embedding,
        limit=top_k,
    )

def search_english_keyword(query, top_k=3):
    german_query = extract_legal_concept(query)

    print()
    print("German query:")
    print(german_query)
    print()

    return keyword_search(german_query, limit=top_k)

def search_hybrid(query, top_k=5):
    semantic_results = search(query, top_k=10)

    keyword_results = search_english_keyword(query, top_k=10)

    documents = {}

    # Add semantic results
    for doc in semantic_results:
        key = (doc["law"], doc["section"])

        documents[key] = {
            **doc,
            "semantic_score": 1 - doc["distance"],
            "keyword_score": 0,
        }


    # Add keyword results
    for doc in keyword_results:
        key = (doc["law"], doc["section"])

        if key in documents:
            documents[key]["keyword_score"] = doc["score"]
        else:
            documents[key] = {
                **doc,
                "semantic_score": 0,
                "keyword_score": doc["score"],
            }


    # Normalize keyword scores
    max_keyword = max(
        [
            d["keyword_score"]
            for d in documents.values()
        ],
        default=1,
    )


    for doc in documents.values():

        if max_keyword:
            doc["keyword_score"] /= max_keyword


        doc["hybrid_score"] = (
            0.4 * doc["semantic_score"]
            +
            0.6 * doc["keyword_score"]
        )


    ranked = sorted(
        documents.values(),
        key=lambda x: x["hybrid_score"],
        reverse=True,
    )


    return ranked[:top_k]