from typing import List, Dict
from app import rag
from sentence_transformers import SentenceTransformer, util
import torch

# Use the same embedding model
_model = SentenceTransformer("all-MiniLM-L6-v2")


# ------------------------------------------------------------
# 1. Semantic similarity between query & retrieved chunks
# ------------------------------------------------------------
def score_chunk_relevance(query: str, chunks: List[Dict]) -> float:
    """
    Computes average semantic similarity between the query and the retrieved chunks.
    Higher = better retrieval relevance.

    Returns a value between 0 and 1.
    """
    query_emb = _model.encode(query, convert_to_tensor=True)
    scores = []

    for c in chunks:
        chunk_emb = _model.encode(c["text"], convert_to_tensor=True)
        sim = util.cos_sim(query_emb, chunk_emb).item()
        scores.append(sim)

    if not scores:
        return 0.0

    return sum(scores) / len(scores)


# ------------------------------------------------------------
# 2. Hallucination detection using context overlap
# ------------------------------------------------------------
def hallucination_score(answer: str, context: str) -> float:
    """
    Checks if the answer is similar to the context.
    Low similarity = high hallucination risk.

    Returns a value between 0 and 1.
    """
    answer_emb = _model.encode(answer, convert_to_tensor=True)
    context_emb = _model.encode(context, convert_to_tensor=True)

    sim = util.cos_sim(answer_emb, context_emb).item()
    return sim  # closer to 0 = likely hallucination


# ------------------------------------------------------------
# 3. Combined evaluation: retrieval, grounding, hallucination
# ------------------------------------------------------------
def evaluate_rag(query: str, k: int = 3):
    """
    Runs retrieval, generates answer, and scores:
    - chunk relevance
    - hallucination risk
    """
    # Retrieve first
    ranked_docs = rag.retrieve(query, k=k)
    if not ranked_docs:
        return None

    # Build context
    context = "\n\n".join(d["text"] for d in ranked_docs)

    # Get LLM answer
    answer = rag.answer(query, k=k)

    # Extract answer content without the Sources section
    if "---\nSources" in answer:
        answer_only = answer.split("---\nSources")[0].strip()
    else:
        answer_only = answer.strip()

    relevance = score_chunk_relevance(query, ranked_docs)
    hallucination = hallucination_score(answer_only, context)

    return {
        "answer": answer_only,
        "relevance_score": relevance,
        "hallucination_score": hallucination,
        "chunks": ranked_docs,
    }
