"""
RAG module for Snowflake RAG Playground.

Week 2 / Day 2:
- Connects to the local Chroma vector store created by ingest.py
- Retrieves the most relevant chunks for a given query
- Returns a simple "answer" built from those chunks

Tomorrow we'll plug in a real LLM on top of this.
"""

from typing import List
import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_DB_DIR = "chroma_store"
COLLECTION_NAME = "docs"

# Load model & vector store once when the module is imported
_model = SentenceTransformer("all-MiniLM-L6-v2")
_client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
_collection = _client.get_or_create_collection(COLLECTION_NAME)


def retrieve(query: str, k: int = 3) -> List[str]:
    """
    Retrieve top-k most relevant document chunks for the query.
    """
    query_embedding = _model.encode([query]).tolist()

    results = _collection.query(
        query_embeddings=query_embedding,
        n_results=k,
    )

    # results["documents"] is a list of lists: [[chunk1, chunk2, ...]]
    documents = results.get("documents", [[]])[0]
    return documents


def answer(query: str) -> str:
    """
    Very simple "answer":
    - fetch top-k chunks
    - stitch them together as context

    Tomorrow, we'll send this context + query to an LLM.
    """
    docs = retrieve(query, k=3)

    if not docs:
        return (
            "No documents were retrieved. "
            "Did you run the ingestion step and add files to /data?"
        )

    context = "\n\n---\n\n".join(docs)

    return (
        "Here are the most relevant snippets I found:\n\n"
        f"{context}\n\n"
        "(LLM-powered answer coming in the next step.)"
    )


def batch_answer(queries: List[str]) -> List[str]:
    """Batch version, in case we want it later."""
    return [answer(q) for q in queries]


if __name__ == "__main__":
    # Quick local test: python -m app.rag
    test_query = "What is Snowflake and what is it good at?"
    print(answer(test_query))
