import streamlit as st
from germany_decoded.assistant import Assistant

st.title("Germany Decoded 🇩🇪")

@st.cache_resource
def load_assistant():
    return Assistant()
assistant = load_assistant()

question = st.text_input(
    "Ask a question",
    placeholder="Can my landlord keep my deposit?"
)

if st.button("Ask") and question:
    with st.spinner("Searching legal database..."):
        result = assistant.ask(question)

    st.markdown("## Answer")
    st.write(result["answer"])

    st.markdown("## Sources")
    for source in result["sources"]:
        st.markdown(
            f"**{source['law']} {source['section']}** — {source['title']}"
        )
        st.caption(source["source"])

with st.sidebar:
    st.caption("Search backend: PostgreSQL + pgvector")