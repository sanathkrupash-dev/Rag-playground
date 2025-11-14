📍 6-Month Roadmap — Snowflake RAG + Agent Assistant

Author: Sanath Srinivasan
Version: v1.0
Status: Draft

Product Vision

Make Snowflake platform knowledge instantly accessible using an AI-powered, retrieval-augmented, multi-agent assistant capable of grounded answers, self-evaluation, orchestration, and domain reasoning.

The goal is to support:

Product managers

Data engineers

Analysts

New team members

…with fast, accurate access to platform knowledge and documentation.

Roadmap Overview (6 Months)
Month	Phase	Theme	Key Outcome
Month 1	Phase 1	Foundation	Basic RAG + ingestion
Month 2	Phase 2	Agentic Capabilities	Agents + function calling
Month 3	Phase 3	Retrieval Quality	Re-ranking, hybrid search
Month 4	Phase 4	Content Expansion	PDF, HTML tables, metadata
Month 5	Phase 5	Production UX	Latency, caching, UI polish
Month 6	Phase 6	Self-Improvement	Auto-eval, auto-rewrite, knowledge graph
⭐ PHASE 1 — RAG Foundation (Month 1)
Theme:

"Grounded retrieval for Snowflake knowledge"

Deliverables:

Chroma persistent store

Semantic chunking

URL ingestion

File ingestion

Query answering with citations

Streamlit UI

Logging & monitoring

Success Criteria:

Retrieval < 300ms

Grounded answers with citations

Ingestion success > 90%

⭐ PHASE 2 — Agentic Framework (Month 2)
Theme:

“Make the assistant intelligent enough to call tools.”

Deliverables:

Tool-based retrieval agent

Function calling (OpenAI)

Agent loop (ReAct-lite)

Evaluator Agent (hallucination detection)

Orchestrator Agent

Retry logic via query rewriting

Success Criteria:

Agent corrects itself when ungrounded

Retry accuracy improves results by 20%

Reasoning trace viewable in UI

⭐ PHASE 3 — Retrieval Quality & Search (Month 3)
Theme:

“Improve retrieval accuracy and relevance.”

Deliverables:

Reranking with cross-encoders

Hybrid search (embedding + keyword)

Reciprocal Rank Fusion (RRF)

Metadata-augmented search (file name, URL, tags)

Query rewriting agent improvements

Duplicate-chunk detection

Success Criteria:

Relevance score > 0.80

Hallucination rate < 15%

Retrieval improvements validated over baseline

⭐ PHASE 4 — Content Expansion (Month 4)
Theme:

“Support real enterprise content formats.”

Deliverables:

PDF ingestion

PPT ingestion (title + content extraction)

DOCX ingestion

Webpage full DOM extraction

Table extraction from PDFs/HTML

Multi-file batch ingestion

Metadata tagging (topic, source, timestamp)

Success Criteria:

Ingest > 95% of Snowflake documentation formats

Extract table content successfully

Context relevance stable with expanded content

⭐ PHASE 5 — Production Readiness & UX (Month 5)
Theme:

“Make it look and feel like a real product.”

Deliverables:

Caching for embeddings & retrieval

Asynchronous ingestion

FastAPI backend (optional)

Streamlit UX redesign

Dark mode

Chat interface

User feedback loop (“Was this answer helpful?”)

Analytics dashboard (queries, latency, score)

Success Criteria:

Average latency < 2 seconds

95th percentile latency < 3.5 seconds

UX satisfaction > 90%

⭐ PHASE 6 — Self-Improving AI System (Month 6)
Theme:

“Make the assistant smarter over time.”

Deliverables:

Auto-eval pipeline (daily self-checking)

Auto-rewrite for bad answers

Auto-ingest new URLs

Knowledge graph extraction

Agent that labels & organizes documents

LLM self-improvement loops (reflection)

Success Criteria:

Automated ingestion pipeline

Automated evals for retrieval & grounding

Knowledge graph with > 1000 edges

⭐ Cross-Cutting Themes
Security

API key rotation

Config file sanitization

PII inspection for documents

Privacy

Local-only ingestion mode

Access control for private documents

Observability

Retrieval logs

Latency logs

Evaluation dashboard

⭐ Risks
Risk	Impact	Mitigation
Poor chunking → low recall	High	Hybrid chunking + eval agent
Model hallucinations	High	Evaluator agent + grounding score
Large files slow ingestion	Medium	Async ingestion + chunk caching
URL extraction fails	Medium	Backup HTML parser, copy-paste
Embedding model limitations	Medium	Swap to stronger models (all-MPNet)
⭐ Dependencies

OpenAI API availability

External websites for ingestion

Local storage for Chroma

Python model compatibility

🎉 End of Roadmap