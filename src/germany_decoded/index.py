import time
from germany_decoded.ingestion import load_documents
from germany_decoded.db.save import store_documents
from germany_decoded.embeddings import create_embeddings

def index():
    t0 = time.time()
    documents = load_documents()
    print("Loading:", time.time() - t0)

    t0 = time.time()
    embeddings = create_embeddings(documents)
    print("Embedding documents:", time.time() - t0)

    t0 = time.time()
    store_documents(documents, embeddings)
    print("Saving to database:", time.time() - t0)

    print(f"Indexed {len(documents)} legal sections.")

if __name__ == "__main__":
    index()