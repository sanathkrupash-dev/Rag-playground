import json
from openai import OpenAI
import os
from app.agent import run_agent
from app.evaluator_agent import evaluate_retrieval
from app import rag

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def orchestrate(user_query: str):
    """
    Orchestrator decides:
    1. Use retrieval agent?
    2. Ask evaluator to validate?
    3. If poor grounding, rewrite query & retry
    """

    # Step 1: Run Retrieval Agent
    answer = run_agent(user_query)

    # Step 2: Rerun retrieval directly to get chunks
    chunks = rag.retrieve(user_query, k=3)

    # Step 3: Evaluate answer quality
    evaluation = evaluate_retrieval(
        user_query=user_query,
        chunks=chunks,
        answer=answer
    )

    # If hallucination is high → ask LLM to rewrite query and retry
    if evaluation["hallucination_risk"] > 0.35:
        retry_prompt = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "Rewrite the query to improve retrieval relevance."
                },
                {"role": "user", "content": user_query}
            ]
        ).choices[0].message.content.strip()

        retry_answer = run_agent(retry_prompt)

        return {
            "initial_answer": answer,
            "evaluation": evaluation,
            "retry_query": retry_prompt,
            "retry_answer": retry_answer,
            "used_retry": True
        }

    return {
        "initial_answer": answer,
        "evaluation": evaluation,
        "used_retry": False
    }
