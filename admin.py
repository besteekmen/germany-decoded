import streamlit as st
import pandas as pd

from germany_decoded.db.monitoring import (
    get_summary,
    get_feedback_summary,
    get_recent_conversations,
)

st.title("Germany Decoded Monitoring")

summary = get_summary()
feedback = get_feedback_summary()
rows = get_recent_conversations()

# ----------- Summary Metrics -----------
col1, col2, col3 = st.columns(3)

col1.metric(
    "Questions",
    summary["total_questions"],
)

col2.metric(
    "Avg Search",
    f"{summary['avg_search_time']:.2f}s",
)

col3.metric(
    "Avg LLM",
    f"{summary['avg_llm_time']:.2f}s",
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Avg Total",
    f"{summary['avg_total_time']:.2f}s",
)

col2.metric(
    "Avg Tokens",
    f"{summary['avg_tokens']:.0f}",
)

col3.metric(
    "Avg Cost",
    f"${summary['avg_cost']:.5f}",
)

# ---------- Feedback Metrics -----------
st.subheader("Feedback")

col1, col2 = st.columns(2)

col1.metric(
    "Helpful 👍",
    feedback["helpful"],
)

col2.metric(
    "Not Helpful 👎",
    feedback["not_helpful"],
)

# ---------- Recent Conversations -----------
st.subheader("Recent Conversations")

df = pd.DataFrame(
    rows,
    columns=[
        "ID",
        "Question",
        "Time (s)",
        "Tokens",
        "Helpful",
        "Created",
    ],
)

st.dataframe(df, use_container_width=True)