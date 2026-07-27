import numpy as np
from germany_decoded.embeddings import embed_query


def search(query, documents, embeddings, top_k=3):
    query_embedding = embed_query(query)

    scores = embeddings @ query_embedding

    top_indices = np.argsort(scores)[::-1][:top_k]

    return [
        documents[i]
        for i in top_indices
    ]