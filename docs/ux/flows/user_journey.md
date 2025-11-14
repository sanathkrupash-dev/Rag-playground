# User Journey — Snowflake RAG + Agent Assistant

```mermaid
flowchart TD
    A[User opens interface] --> B[Decides ingestion type]
    B -->|Upload File| C[File Ingestion]
    B -->|Paste URL| D[URL Ingestion]
    C --> E[Semantic Chunking]
    D --> E[Semantic Chunking]

    E --> F[Embeddings Created]
    F --> G[Chroma Vector Store]

    G --> H[User Asks Question]
    H --> I[Orchestrator Agent]

    I -->|Needs Retrieval| J[Retrieval Agent]
    J --> K[Relevant Chunks]

    I -->|Evaluate Quality| L[Evaluator Agent]
    L -->|High Risk| M[Query Rewrite + Retry]
    L -->|Low Risk| N[Use Original Answer]

    M --> J
    K --> O[Final Answer Generated]
    N --> O

    O --> P[User Views Answer + Sources]



