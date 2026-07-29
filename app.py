import streamlit as st
from germany_decoded.ingestion import load_documents
from germany_decoded.embeddings import create_embeddings
from germany_decoded.retrieval import search
from germany_decoded.prompt import build_context
from germany_decoded.llm import ask_llm

@st.cache_resource
def load_resources():
    documents = load_documents()
    embeddings = create_embeddings(documents)
    return documents, embeddings


st.title("Germany Decoded 🇩🇪")

with st.spinner("Loading legal knowledge..."):
    documents, embeddings = load_resources()

question = st.text_input(
    "Ask a question",
    placeholder="Can my landlord keep my deposit?"
)

if st.button("Ask") and question:
    results = search(
        question,
        documents,
        embeddings
    )

    context = build_context(results)

    with st.spinner("Thinking..."):
        answer = ask_llm(
            question,
            context,
        )

    st.markdown("## Answer")
    st.write(answer)

    st.markdown("## Sources")
    for result in results:
        st.markdown(
            f"**{result['law']} {result['section']}** — {result['title']}"
        )
        st.caption(result["source"])

with st.sidebar:
    st.caption(f"Loaded {len(documents)} legal sections.")