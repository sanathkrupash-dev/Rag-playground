
Paste:

```md
# Retrieval Agent Flow

```mermaid
flowchart TD
    A[User Query] --> B[LLM: Decide action]
    B -->|Call retrieve_tool| C[Retrieve Chunks]
    C --> D[Return Chunks as JSON]
    D --> E[LLM: Use chunks to generate answer]
    B -->|Direct Answer| F[LLM answers w/o retrieval]
    E --> G[Return Final Answer]
    F --> G
