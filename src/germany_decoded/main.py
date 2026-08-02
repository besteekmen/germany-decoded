from germany_decoded.retrieval import search
from germany_decoded.prompt import build_context
from germany_decoded.llm import ask_llm
import time

def main():
    question = "Can I reduce my rent because my apartment has defects?"

    t0 = time.time()
    #results = search(
    #    question,
    #    documents,
    #    embeddings
    #)
    results = search(question)
    print("Search:", time.time() - t0)

    context = build_context(results)

    answer = ask_llm(question, context)

    print(answer)

if __name__ == "__main__":
    main()