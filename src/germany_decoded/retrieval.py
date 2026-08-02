import numpy as np
from germany_decoded.embeddings import embed_query
from germany_decoded.db.query import search_documents


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