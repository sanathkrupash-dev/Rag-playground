import streamlit as st

from app import rag
from app import ingest_utils

# -------------------------------------------------------
# Streamlit Page Config
# -------------------------------------------------------
st.set_page_config(
    page_title="Snowflake RAG Playground",
    page_icon="❄️",
    layout="wide",
)

st.title("❄️ Snowflake RAG Playground")
st.write(
    "Ask questions about your ingested documents using embeddings + Chroma + OpenAI.\n"
    "Upload files or ingest webpages directly."
)

# -------------------------------------------------------
# Sidebar: File Upload
# -------------------------------------------------------
st.sidebar.header("📄 Upload & Ingest Local Files")

uploaded_file = st.sidebar.file_uploader(
    "Upload a .txt or .md file",
    type=["txt", "md"]
)

if uploaded_file:
    text = uploaded_file.read().decode("utf-8")
    num_chunks = ingest_utils.ingest_text(uploaded_file.name, text)
    st.sidebar.success(f"Added {num_chunks} chunks from {uploaded_file.name}")


# -------------------------------------------------------
# Sidebar: URL ingestion
# -------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("🌐 Ingest Webpage URL")

url = st.sidebar.text_input(
    "Enter webpage URL",
    placeholder="https://docs.snowflake.com/en/..."
)

if st.sidebar.button("Fetch & Ingest URL"):
    if not url.strip():
        st.sidebar.warning("Please enter a valid URL.")
    else:
        with st.spinner("Fetching and ingesting webpage..."):
            num_chunks = ingest_utils.ingest_url(url.strip())

        if num_chunks > 0:
            st.sidebar.success(f"Ingested {num_chunks} chunks from URL")
        else:
            st.sidebar.error("Could not extract text from that URL.")


# -------------------------------------------------------
# Sidebar: Debug view of DB
# -------------------------------------------------------
with st.sidebar.expander("🧪 View chunks in vector DB"):
    docs = ingest_utils.list_all_docs()
    st.write(f"Total chunks stored: {len(docs)}")
    for d in docs[:20]:
        st.text(d)


# -------------------------------------------------------
# Main Query Input
# -------------------------------------------------------
st.markdown("---")
st.subheader("💬 Ask a Question")

query = st.text_input(
    "Your Question",
    placeholder="e.g., What is Snowflake and what is it used for?"
)

top_k = st.slider(
    "Number of chunks to use (k)",
    min_value=1,
    max_value=10,
    value=3,
    help="Higher k gives more context but may slow down the model."
)

if st.button("Get Answer"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Running RAG pipeline..."):
            answer_text = rag.answer(query, k=top_k)

        st.subheader("💡 Answer")
        st.write(answer_text)

        # Debug chunk view
        with st.expander("🔍 Retrieved chunks (debug)"):
            ranked_docs = rag.retrieve(query, k=top_k)
            if not ranked_docs:
                st.write("No chunks retrieved. Did you run ingestion?")
            else:
                for i, d in enumerate(ranked_docs, start=1):
                    st.markdown(f"**Chunk {i} — score={d['score']:.4f}**")
                    st.code(d["text"])

st.markdown("---")
st.subheader("🧪 RAG Evaluation")

eval_query = st.text_input(
    "Evaluation Query",
    placeholder="Same or different question, e.g. 'What is Snowflake?'"
)

if st.button("Run Evaluation"):
    if not eval_query.strip():
        st.warning("Please enter a query to evaluate.")
    else:
        with st.spinner("Running RAG evaluation..."):
            from app.eval_utils import evaluate_rag
            result = evaluate_rag(eval_query)

        if result is None:
            st.error("No chunks retrieved — ingestion may be required.")
        else:
            st.write("### 📝 Answer")
            st.write(result["answer"])

            st.write(f"### 📊 Retrieval Quality")
            st.write(f"**Relevance score:** `{result['relevance_score']:.4f}`")

            st.write(f"### 🧱 Hallucination Check")
            st.write(f"**Hallucination risk:** `{1 - result['hallucination_score']:.4f}` (lower is better)")

            st.write("---")
            st.write("### 🔍 Retrieved Chunks")
            for i, c in enumerate(result["chunks"], start=1):
                st.markdown(f"**Chunk {i} — score={c['score']:.4f}**")
                st.code(c["text"])

st.markdown("---")
st.subheader("📦 Chunk Explorer")

from app.ingest_utils import semantic_chunk

debug_text = st.text_area(
    "Paste text to preview semantic chunking",
    placeholder="Paste a paragraph or page..."
)

if st.button("Preview Chunks"):
    if not debug_text.strip():
        st.warning("Paste some text first.")
    else:
        preview_chunks = semantic_chunk(debug_text)
        st.write(f"Generated {len(preview_chunks)} chunks.")

        for i, ch in enumerate(preview_chunks, start=1):
            st.markdown(f"**Chunk {i}**")
            st.code(ch)

# -------------------------------------------------------
# Footer
# -------------------------------------------------------
st.markdown("---")
st.caption("Snowflake RAG Playground — built by Sanath Srinivasan 🚀")
