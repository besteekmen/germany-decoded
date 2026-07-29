from germany_decoded.ingestion import load_documents
from germany_decoded.retrieval import search
from germany_decoded.embeddings import create_embeddings
from germany_decoded.prompt import build_context, build_prompt
from germany_decoded.llm import ask_llm
import time

def main():
    t0 = time.time()
    documents = load_documents()
    print("Loading:", time.time() - t0)
    print(f"Loaded {len(documents)} legal sections")

    t0 = time.time()
    embeddings = create_embeddings(documents)
    print("Embedding:", time.time() - t0)

    question = "Can I reduce my rent because my apartment has defects?"

    t0 = time.time()
    results = search(
        question,
        documents,
        embeddings
    )
    print("Search:", time.time() - t0)

    context = build_context(results)

    answer = ask_llm(question, context)

    print(answer)

if __name__ == "__main__":
    main()