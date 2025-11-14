"""
RAG module for Snowflake RAG Playground.

- Connects to the local Chroma store created by ingest.py
- Retrieves and ranks relevant chunks for a query
- Uses OpenAI to generate an answer grounded in those chunks
- Adds simple logging and citations for debugging / explainability
"""

from typing import List, Dict
import os

import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from openai import OpenAI

from .logger import timed, log_info, log_debug, log_section

# ---------------------------------------------------------------------
# Setup: environment + OpenAI client
# ---------------------------------------------------------------------

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

client = OpenAI(api_key=OPENAI_API_KEY)

# ---------------------------------------------------------------------
# Setup: embeddings + vector store
# ---------------------------------------------------------------------

CHROMA_DB_DIR = "chroma_store"
COLLECTION_NAME = "docs"

_model = SentenceTransformer("all-MiniLM-L6-v2")
_client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
_collection = _client.get_or_create_collection(COLLECTION_NAME)


# ---------------------------------------------------------------------
# Retrieval
# ---------------------------------------------------------------------

@timed
def retrieve(query: str, k: int = 3) -> List[Dict[str, float | str]]:
    """
    Retrieve top-k most relevant document chunks for the query.

    Returns a list of dicts:
    [
      {"text": "<chunk text>", "score": <distance>},
      ...
    ]
    """
    query_embedding = _model.encode([query]).tolist()

    result = _collection.query(
        query_embeddings=query_embedding,
        n_results=k,
        include=["documents", "distances"],
    )

    docs = result.get("documents", [[]])[0]
    distances = result.get("distances", [[]])[0]

    ranked: List[Dict[str, float | str]] = []
    for text, dist in zip(docs, distances):
        ranked.append(
            {
                "text": text,
                "score": float(dist),  # lower distance = more similar
            }
        )

    # Sort by similarity (ascending distance)
    ranked.sort(key=lambda x: x["score"])

    log_debug(f"Retrieved {len(ranked)} docs for query: {query!r}")
    return ranked


# ---------------------------------------------------------------------
# LLM call
# ---------------------------------------------------------------------

def _llm_answer(query: str, context: str) -> str:
    """
    Call OpenAI chat completions using the v1 client.
    """

    if not OPENAI_API_KEY:
        return (
            "OPENAI_API_KEY is not set. "
            "Add it to your .env file before running RAG."
        )

    messages = [
        {
            "role": "system",
            "content": (
                "You are an assistant helping a data platform product manager "
                "understand a Snowflake-like analytics platform. "
                "Answer using the provided context as your primary source. "
                "Quote or summarize it directly when possible. "
                "If the context is clearly unrelated or completely missing, "
                "say you don't know. Otherwise, give your best concise answer."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Context:\n{context}\n\n"
                f"User question:\n{query}"
            ),
        },
    ]

    completion = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=0.2,
    )

    return completion.choices[0].message.content.strip()


# ---------------------------------------------------------------------
# Public API: answer + helpers
# ---------------------------------------------------------------------

def answer(query: str, k: int = 3) -> str:
    """
    Full RAG flow:
    - retrieve top-k chunks (ranked)
    - pass them plus the query to the LLM
    - return the model's answer with simple citations
    """
    log_section("NEW QUERY")
    log_info(f"Q: {query}")

    ranked_docs = retrieve(query, k=k)

    if not ranked_docs:
        return (
            "No documents were retrieved. "
            "Did you run the ingestion step and add files to /data?"
        )

    context = "\n\n---\n\n".join(d["text"] for d in ranked_docs)

    citations = "\n".join(
        f"[{i + 1}] score={d['score']:.4f}"
        for i, d in enumerate(ranked_docs)
    )

    try:
        response = _llm_answer(query, context)
    except Exception as e:
        # Fallback: show retrieved context when LLM fails
        return (
            f"(LLM call failed: {e})\n\n"
            "Here are the most relevant snippets I found:\n\n"
            f"{context}\n\n"
            "---\nSources:\n{citations}"
        )

    return f"{response}\n\n---\nSources:\n{citations}"


def batch_answer(queries: List[str], k: int = 3) -> List[str]:
    """Batch version, in case we want it later."""
    return [answer(q, k=k) for q in queries]


def inspect(query: str, k: int = 3) -> None:
    """
    Debug/PM helper: print the retrieved chunks and scores without calling the LLM.
    """
    log_section("CHUNK INSPECTOR")
    log_info(f"Inspecting query: {query!r}")

    ranked_docs = retrieve(query, k=k)

    if not ranked_docs:
        log_warn("No documents retrieved.")
        return

    for i, d in enumerate(ranked_docs, start=1):
        log_info(f"[{i}] score={d['score']:.4f}")
        print(d["text"])
        print("\n---\n")


# ---------------------------------------------------------------------
# Manual test
# ---------------------------------------------------------------------

if __name__ == "__main__":
    test_query = "What is Snowflake and what is it used for?"
    print(answer(test_query))
