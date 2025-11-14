
Paste:

```md
# RAG (Retrieval-Augmented Generation) Pipeline

```mermaid
sequenceDiagram
    participant U as User
    participant E as Embedder
    participant DB as Vector DB (Chroma)
    participant LLM as OpenAI Model

    U->>E: Embed query
    E->>DB: Vector similarity search
    DB->>U: Return top-k chunks
    U->>LLM: Query + retrieved chunks
    LLM->>U: Grounded answer + citations
