# RAG ANSWER PROMPT

Use ONLY the provided context to answer the user’s question.

Context:
{context}

User question:
{query}

Instructions:
- If the information is not available, say “I don’t know based on the ingested documents.”
- Summarize, do not copy entire chunks.
- Keep answers concise, unless the user asks for depth.
- Include a “Sources” section with the chunk IDs.

Output:
Answer:
<final answer>

Sources:
- <chunk_id: short reason>
