
Paste:

```md
# Ingestion Flow

```mermaid
flowchart TD
    A[User uploads file or adds URL] --> B[Extract text]
    B --> C[Semantic Chunking + Overlap]
    C --> D[Embedding Model]
    D --> E[Vector Store]
    E --> F[Metadata Storage]
    F --> G[Ingestion Success Response]
