
---

# ✅ **3. multi_agent_flow.md (Multi-Agent Orchestrator Flow)**

```md
# Multi-Agent Orchestration Flow

```mermaid
flowchart TD
    A[User Query] --> B[Orchestrator Agent]

    B -->|Ask: Retrieval Needed?| C{Need Retrieval?}

    C -->|Yes| D[Retrieval Agent]
    D --> E[Return Chunks]
    E --> F[LLM Answer Generator]
    F --> G[Final Answer]

    C -->|No| H[Direct LLM Answer]
    H --> G
