import streamlit as st
import pandas as pd

from germany_decoded.assistant import Assistant
from germany_decoded.db.feedback import save_feedback
from germany_decoded.db.monitoring import (
    get_summary,
    get_feedback_summary,
    get_recent_conversations,
    get_judge_summary,
)

# =============================================================================
# Configuration
# =============================================================================

ADMIN = True  # Set to True to enable the admin dashboard

st.set_page_config(
    page_title="Germany Decoded",
    page_icon="🇩🇪",
    layout="wide",
)

# =============================================================================
# Backend
# =============================================================================

@st.cache_resource
def load_assistant():
    return Assistant()


assistant = load_assistant()

# =============================================================================
# Sidebar
# =============================================================================

with st.sidebar:

    st.title("Germany Decoded")

    st.caption(
        "AI-powered legal assistant for Germany."
    )

    st.divider()

    if ADMIN:
        page = st.radio(
            "Navigation",
            [
                "Assistant",
                "Admin Dashboard",
            ],
        )
    else:
        page = "Assistant"

    st.divider()

    st.subheader("System")

    st.markdown("##### :material/memory: Model")
    st.caption("GPT-5 Mini")

    st.markdown("##### :material/search: Retrieval")
    st.caption("Hybrid Search")

    st.markdown("##### :material/database: Database")
    st.caption("PostgreSQL + pgvector")

    if assistant.last_call:

        st.divider()

        st.subheader("Last Request")

        st.metric(
            "Search",
            f"{assistant.last_call.search_time:.2f}s",
        )

        st.metric(
            "LLM",
            f"{assistant.last_call.llm_time:.2f}s",
        )

        st.metric(
            "Tokens",
            assistant.last_call.total_tokens,
        )
    
    if page == "Assistant":
        st.divider()
        st.subheader("Conversation History")

        history_rows = get_recent_conversations(limit=10)

        if history_rows:
            history_options = {}

            for row in history_rows:
                (
                    conversation_id,
                    question,
                    answer,
                    total_time,
                    total_tokens,
                    helpful,
                    created_at,
                ) = row

                label = (
                    question[:42] + "..."
                    if len(question) > 42
                    else question
                )

                history_options[label] = {
                    "id": conversation_id,
                    "question": question,
                    "answer": answer,
                    "created_at": created_at,
                }

            selected_history = st.selectbox(
                "Recent questions",
                options=list(history_options.keys()),
                label_visibility="collapsed",
            )

            if st.button(
                "Open conversation",
                use_container_width=True,
            ):
                st.session_state["selected_history"] = (
                    history_options[selected_history]
                )
                st.rerun()

        else:
            st.caption("No conversations yet.")

# =============================================================================
# Assistant Page
# =============================================================================

def assistant_page():

    st.title("Germany Decoded")

    st.caption(
        "Trusted German Legal Information • Powered by Hybrid Retrieval + GPT-5 Mini"
    )

    if "selected_history" in st.session_state:
        history_item = st.session_state["selected_history"]

        with st.container(border=True):
            col1, col2 = st.columns(
                [5, 1],
                vertical_alignment="center",
            )

            with col1:
                st.markdown("### Previous Conversation")

            with col2:
                if st.button(
                    "Close",
                    key="close_history",
                    use_container_width=True,
                ):
                    del st.session_state["selected_history"]
                    st.rerun()

            st.caption(
                history_item["created_at"].strftime(
                    "%Y-%m-%d %H:%M"
                )
            )

            st.markdown("**Question**")
            st.write(history_item["question"])

            st.markdown("**Answer**")
            st.markdown(history_item["answer"])

        st.write("")

    st.write("")

    with st.container(border=True):

        st.markdown(
            """
        ### Ask a Question

        Ask about housing, employment, rental deposits,
        consumer rights, contracts, and other everyday
        German legal topics.
        """
        )

        question = st.text_input(
            "",
            placeholder="e.g. Can my landlord keep my rental deposit?",
            label_visibility="collapsed",
        )

        ask = st.button("Ask")

    if ask and question:

        st.session_state.pop(
            "selected_history",
            None,
        )

        with st.spinner(
            "Searching legal documents and generating an answer..."
        ):

            result = assistant.ask(question)

            st.session_state["result"] = result
            st.session_state["feedback_given"] = False

    if "result" not in st.session_state:
        return

    result = st.session_state["result"]

    st.write("")

    with st.container(border=True):

        st.subheader("Answer")

        st.markdown(result["answer"])

    st.write("")

    st.subheader("Official Sources")

    for source in result["sources"]:
        with st.container(border=True):

            st.markdown(
                f"**{source['law']} {source['section']}**"
            )

            st.write(source["title"])

            st.caption(source["source"])

    st.write("")

    with st.container(border=True):

        st.subheader("Was this answer helpful?")

        if not st.session_state.get("feedback_given", False):

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "👍 Helpful",
                    use_container_width=True,
                ):

                    save_feedback(
                        result["conversation_id"],
                        True,
                    )

                    st.session_state["feedback_given"] = True

                    st.rerun()

            with col2:

                if st.button(
                    "👎 Not Helpful",
                    use_container_width=True,
                ):

                    save_feedback(
                        result["conversation_id"],
                        False,
                    )

                    st.session_state["feedback_given"] = True

                    st.rerun()

        else:
            st.success("Thank you for your feedback!")

    st.divider()

    st.caption(
        "Germany Decoded • AI Engineering Project • LLM Zoomcamp 2026"
    )

# =============================================================================
# Admin Dashboard
# =============================================================================

def admin_page():

    st.markdown("# :material/dashboard: Admin Dashboard")

    st.caption(
        "Monitor usage, performance, feedback, and answer quality."
    )

    summary = get_summary()
    feedback = get_feedback_summary()
    judge = get_judge_summary()
    rows = get_recent_conversations()

    st.subheader("Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Questions",
            summary["total_questions"],
        )

    with col2:
        st.metric(
            "Avg Search",
            f"{summary['avg_search_time']:.2f}s",
        )

    with col3:
        st.metric(
            "Avg LLM",
            f"{summary['avg_llm_time']:.2f}s",
        )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Avg Total",
            f"{summary['avg_total_time']:.2f}s",
        )

    with col2:
        st.metric(
            "Avg Tokens",
            f"{summary['avg_tokens']:.0f}",
        )

    with col3:
        st.metric(
            "Avg Cost",
            f"${summary['avg_cost']:.5f}",
        )

    st.divider()

    # -------------------------------------------------------------------------
    # Feedback and Judge Metrics
    # -------------------------------------------------------------------------

    st.subheader("Evaluation Overview")

    feedback_col, judge_col = st.columns(2)

    with feedback_col:
        with st.container(border=True):
            st.markdown("#### User Feedback")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Helpful 👍",
                    feedback["helpful"],
                )

            with col2:
                st.metric(
                    "Not Helpful 👎",
                    feedback["not_helpful"],
                )

    with judge_col:
        with st.container(border=True):
            st.markdown("#### LLM Judge")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Relevant",
                    judge["relevant"],
                )

            with col2:
                st.metric(
                    "Partly Relevant",
                    judge["partly_relevant"],
                )

            with col3:
                st.metric(
                    "Not Relevant",
                    judge["not_relevant"],
                )

    st.divider()

    # -------------------------------------------------------------------------
    # Charts
    # -------------------------------------------------------------------------

    st.subheader("Performance Trends")

    df = pd.DataFrame(
        rows,
        columns=[
            "ID",
            "Question",
            "Answer",
            "Time (s)",
            "Tokens",
            "Helpful",
            "Created",
        ],
    )

    if not df.empty:
        df["Created"] = pd.to_datetime(df["Created"])

        chart_df = df.sort_values("Created")

        col1, col2 = st.columns(2)

        with col1:
            with st.container(border=True):
                st.markdown("#### Response Time")

                st.line_chart(
                    chart_df,
                    x="Created",
                    y="Time (s)",
                    x_label="Time",
                    y_label="Seconds",
                )

        with col2:
            with st.container(border=True):
                st.markdown("#### Token Usage")

                st.line_chart(
                    chart_df,
                    x="Created",
                    y="Tokens",
                    x_label="Time",
                    y_label="Tokens",
                )

        col1, col2 = st.columns(2)

        with col1:
            with st.container(border=True):
                st.markdown("#### Feedback Distribution")

                feedback_chart = pd.DataFrame(
                    {
                        "Feedback": [
                            "Helpful",
                            "Not Helpful",
                        ],
                        "Count": [
                            feedback["helpful"],
                            feedback["not_helpful"],
                        ],
                    }
                )

                st.bar_chart(
                    feedback_chart,
                    x="Feedback",
                    y="Count",
                    x_label="Feedback",
                    y_label="Responses",
                )

        with col2:
            with st.container(border=True):
                st.markdown("#### LLM Judge Distribution")

                judge_chart = pd.DataFrame(
                    {
                        "Relevance": [
                            "Relevant",
                            "Partly Relevant",
                            "Not Relevant",
                        ],
                        "Count": [
                            judge["relevant"],
                            judge["partly_relevant"],
                            judge["not_relevant"],
                        ],
                    }
                )

                st.bar_chart(
                    judge_chart,
                    x="Relevance",
                    y="Count",
                    x_label="Judge Result",
                    y_label="Conversations",
                )

    else:
        st.info("Charts will appear after conversations are recorded.")

    st.divider()

    # -------------------------------------------------------------------------
    # Recent Conversations
    # -------------------------------------------------------------------------

    st.subheader("Recent Conversations")

    if not df.empty:
        display_df = (
            df.sort_values(
                "Created",
                ascending=False,
            )
            .drop(columns=["Answer"])
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Time (s)": st.column_config.NumberColumn(
                    "Time (s)",
                    format="%.2f",
                ),
                "Helpful": st.column_config.TextColumn(
                    "Helpful",
                ),
                "Created": st.column_config.DatetimeColumn(
                    "Created",
                    format="YYYY-MM-DD HH:mm",
                ),
            },
        )

    else:
        st.info("No conversations recorded yet.")
    
    st.divider()

    st.caption(
        "Germany Decoded • AI Engineering Project • LLM Zoomcamp 2026"
    )

# =============================================================================
# Router
# =============================================================================

if page == "Assistant":
    assistant_page()
else:
    admin_page()