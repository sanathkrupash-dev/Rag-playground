
Paste:

```md
# Multi-Agent Orchestration Flow

```mermaid
flowchart LR
    U[User Query] --> O[Orchestrator Agent]

    O --> R(Retrieval Agent)
    R --> RC[Retrieved Chunks]
    O --> E(Evaluator Agent)

    RC --> E
    E -->|High Hallucination| Q[Query Rewrite Agent]
    Q --> R

    E -->|Good Answer| F[Final Answer]

    R --> A[Answer]
    A --> E

    F --> U
