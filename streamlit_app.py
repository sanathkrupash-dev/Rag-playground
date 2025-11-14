import streamlit as st

from app import rag

st.set_page_config(
    page_title="Snowflake RAG Playground",
    page_icon="❄️",
    layout="wide",
)

st.title("❄️ Snowflake RAG Playground")
st.write(
    "Ask questions about your ingested docs. "
    "Behind the scenes, this uses embeddings + Chroma + OpenAI."
)

# Sidebar
st.sidebar.header("Settings")
top_k = st.sidebar.slider("Number of chunks to retrieve (k)", min_value=1, max_value=10, value=3)

st.sidebar.markdown("---")
st.sidebar.write("Tips:")
st.sidebar.write("- Run ingestion first: `python -m app.ingest`")
st.sidebar.write("- Add more `.md` / `.txt` files to the `data/` folder")


# Main input area
query = st.text_input("🔎 Ask a question", placeholder="e.g., What is Snowflake and what is it used for?")

if st.button("Get Answer") and query.strip():
    with st.spinner("Running RAG pipeline..."):
        # Get full RAG answer (with sources text at the bottom)
        answer_text = rag.answer(query, k=top_k)

    st.subheader("💡 Answer")
    st.write(answer_text)

    # Also show retrieved chunks separately using the inspect-like view
    with st.expander("🔍 View retrieved chunks (debug)"):
        ranked_docs = rag.retrieve(query, k=top_k)
        if not ranked_docs:
            st.write("No chunks retrieved. Did you run ingestion?")
        else:
            for i, d in enumerate(ranked_docs, start=1):
                st.markdown(f"**Chunk {i} — score={d['score']:.4f}**")
                st.code(d["text"])
else:
    st.write("Enter a question above and click **Get Answer** to run the RAG pipeline.")
