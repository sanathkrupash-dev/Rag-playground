import json
import os
from openai import OpenAI
from sentence_transformers import SentenceTransformer, util

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
_embed = SentenceTransformer("all-MiniLM-L6-v2")


def semantic_similarity(a: str, b: str) -> float:
    emb_a = _embed.encode(a, convert_to_tensor=True)
    emb_b = _embed.encode(b, convert_to_tensor=True)
    return util.cos_sim(emb_a, emb_b).item()


def evaluate_retrieval(user_query: str, chunks: list, answer: str):
    """
    Evaluates:
    - Chunk relevance
    - Grounding / hallucination risk
    - Missing info
    """

    concatenated = "\n".join([c["text"] for c in chunks])

    relevance = semantic_similarity(user_query, concatenated)
    grounding = semantic_similarity(answer, concatenated)
    hallucination_risk = max(0, 1 - grounding)

    # Ask LLM for human-style evaluation message
    llm_eval = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an evaluator agent. "
                    "Analyze whether the answer is grounded in the retrieved chunks. "
                    "Provide JSON only."
                )
            },
            {
                "role": "user",
                "content": json.dumps({
                    "query": user_query,
                    "chunks": concatenated,
                    "answer": answer
                })
            }
        ]
    )

    try:
        llm_data = json.loads(llm_eval.choices[0].message.content)
    except Exception:
        llm_data = {"llm_notes": "Failed to parse evaluator output."}

    return {
        "relevance": relevance,
        "grounding": grounding,
        "hallucination_risk": hallucination_risk,
        "llm_feedback": llm_data
    }
