"""
RAG module for Snowflake RAG Playground.

Week 1 / Day 6:
- This is a placeholder file.
- In Week 2 we'll make this:
  - query the vector store,
  - build a prompt with retrieved context,
  - call an LLM to generate an answer.
"""

from typing import List


def answer(query: str) -> str:
    """
    Placeholder RAG answer function.

    In the future, this will:
    - retrieve top-k relevant chunks for `query`
    - call an LLM with those chunks as context
    - return the model's answer
    """
    return (
        "RAG not implemented yet. "
        f"You asked: '{query}'. This is just a placeholder response."
    )


def batch_answer(queries: List[str]) -> List[str]:
    """Placeholder batch answering, for future use."""
    return [answer(q) for q in queries]


if __name__ == "__main__":
    # Allow: python app/rag.py
    print(answer("How do I size a Snowflake warehouse?"))
