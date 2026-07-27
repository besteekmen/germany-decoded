from germany_decoded.ingestion import load_documents
from germany_decoded.retrieval import search
from germany_decoded.embeddings import create_embeddings

def main():
    documents = load_documents()

    #print(f"Loaded {len(documents)} documents")
    #print(documents[:5])

    #---

    #results = search(
    #    "Mietminderung bei Mängeln",
    #    documents
    #)
    #print(results)

    #---

    #embeddings = create_embeddings(documents)
    #print(embeddings.shape)

    #---

    embeddings = create_embeddings(documents)

    results = search(
        "Can my landlord keep my deposit?",
        documents,
        embeddings
    )

    for result in results:
        print(result["title"])
        print(result["content"][:200])
        print(result["source"])
        print("---")


if __name__ == "__main__":
    main()