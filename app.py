import streamlit as st
from germany_decoded.retrieval import search
from germany_decoded.prompt import build_context
from germany_decoded.llm import ask_llm
import time

st.title("Germany Decoded 🇩🇪")

question = st.text_input(
    "Ask a question",
    placeholder="Can my landlord keep my deposit?"
)

if st.button("Ask") and question:
    with st.spinner("Searching legal database..."):
        t0 = time.time()

        results = search(question)

        st.caption(f"Search time: {time.time()-t0:.2f}s")

    context = build_context(results)

    with st.spinner("Generating answer..."):
        t0 = time.time()

        answer = ask_llm(
            question,
            context
        )

        st.caption(f"LLM time: {time.time()-t0:.2f}s")

    st.markdown("## Answer")
    st.write(answer)

    st.markdown("## Sources")
    for result in results:
        st.markdown(
            f"**{result['law']} {result['section']}** — {result['title']}"
        )
        st.caption(result["source"])

with st.sidebar:
    st.caption("Search backend: PostgreSQL + pgvector")