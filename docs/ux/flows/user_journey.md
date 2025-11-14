
---

# ✅ **5. user_journey.md (End-to-End User Journey)**

```md
# RAG Playground — User Journey

```mermaid
flowchart TD
    A[User Opens App] --> B[Uploads Docs or Webpages]
    B --> C[System Ingests + Embeds Content]
    C --> D[User Asks a Question]
    D --> E[System Retrieves Relevant Chunks]
    E --> F[LLM Produces Grounded Answer]
    F --> G[User Reads Answer]
    G --> H[User Iterates with More Questions]
