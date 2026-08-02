import streamlit as st
from germany_decoded.assistant import Assistant
from germany_decoded.db.feedback import save_feedback

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
    with st.spinner("Searching and generating answer..."):
        result = assistant.ask(question)
        st.session_state["result"] = result
        st.session_state["feedback_given"] = False

if "result" in st.session_state:
    result = st.session_state["result"]

    st.markdown("## Answer")
    st.write(result["answer"])

    st.markdown("## Sources")
    for source in result["sources"]:
        st.markdown(
            f"**{source['law']} {source['section']}** — {source['title']}"
        )
        st.caption(source["source"])

    if not st.session_state.get("feedback_given", False):
        col1, col2 = st.columns(2)

        with col1:
            if st.button("👍 Helpful"):
                save_feedback(result["conversation_id"], True)
                st.session_state["feedback_given"] = True
                st.rerun()

        with col2:
            if st.button("👎 Not Helpful"):
                save_feedback(result["conversation_id"], False)
                st.session_state["feedback_given"] = True
                st.rerun()
    else:
        st.success("Thanks for your feedback!")

with st.sidebar:
    st.caption("Search backend: PostgreSQL + pgvector")

    if assistant.last_call:
        st.divider()
        st.caption(f"Search: {assistant.last_call.search_time:.2f}s")
        st.caption(f"LLM: {assistant.last_call.llm_time:.2f}s")
        st.caption(f"Tokens: {assistant.last_call.total_tokens}")