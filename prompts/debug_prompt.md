# DEBUG PROMPT — Retrieval Inspector

Your job is to analyze whether the retrieved chunks are relevant to the query.

User Query:
{query}

Retrieved Chunks:
{chunks}

Tasks:
1. Rate each chunk for relevance (0–1).
2. Identify missing concepts.
3. Suggest better search terms (“query rewrites”).
4. Check whether answer is likely grounded.

Output:
- Relevance table
- Missing info
- Query rewrite suggestions
- Hallucination warning (Low/Medium/High)
