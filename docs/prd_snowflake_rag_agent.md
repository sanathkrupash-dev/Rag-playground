PRD: Snowflake RAG + Agent Assistant

Author: Sanath Srinivasan
Last Updated: {today}
Version: v1.0
Status: Draft

1. Overview

The Snowflake RAG + Agent Assistant is an intelligent, retrieval-augmented system designed to help users understand Snowflake concepts, internal documentation, architecture, and operational processes by grounding answers in ingested files, URLs, and data sources.

The product combines:

RAG (Retrieval-Augmented Generation)

Semantic embeddings

URL + document ingestion

Function-calling agents

Evaluator & Orchestrator Agents

Streamlit UI for interaction & debugging

This PRD defines the goals, scope, capabilities, success criteria, and roadmap for the assistant.

2. Problem Statement

Snowflake documentation, internal architecture details, and platform knowledge are scattered across:

Docs pages

Internal technical notes

Architecture diagrams

Slack threads

PDFs

Confluence

This results in:

Problems

Engineers waste time searching for answers

PMs struggle to onboard quickly

Documentation goes stale

Operational tribal knowledge is lost

Repeated questions burden senior engineers

Opportunity

A retrieval-augmented, agentic knowledge assistant that indexes everything and answers Snowflake questions reliably.

3. Target Users / Personas
1. Data Platform PM (Primary)

Needs quick understanding of:

Snowflake architecture

Cost models

Governance

Workflows

Engineering decisions

2. Data Engineers

Need grounded answers on:

Warehouses

Query performance

RBAC

Storage structure

Materialized views

3. New Team Members

Need fast onboarding to Snowflake concepts.

4. Goals
🎯 Primary Goals

Provide accurate, grounded answers using Retrieval-Augmented Generation.

Support ingestion from local files & URLs.

Add agentic reasoning for better grounding & correction.

Provide debugging tools for transparency (chunks, embeddings, evaluation).

Serve as a PM portfolio case study showcasing PM + AI + engineering skills.

🚫 Non-Goals

Not a full enterprise search engine

Not real-time synced with Snowflake datasets

Not a replacement for Snowflake’s official documentation

5. Capabilities (Functional Requirements)
1. Document Ingestion

Upload .txt, .md, .pdf (future)

Ingest external URLs

Chunk documents semantically

Create embeddings using SentenceTransformer

Store in Chroma persistent vector DB

2. Retrieval

Embed user query

Perform similarity search

Return top-k relevant chunks

Show chunk text + scores

3. RAG Answering

Pass retrieved chunks into OpenAI LLM

Produce grounded answer

Provide source citations

Catch LLM errors

4. Agent Mode

Tools: retrieval, re-ranking (future)

Function calling

Tool execution

LLM reasoning trace

Answer generation with context

5. Multi-Agent Mode

Orchestrator Agent

Evaluator Agent

Query rewriting when retrieval fails

Hallucination detection

Final answer synthesis

6. Evaluation Tools

Relevance scoring

Grounding score

Hallucination risk

Chunk explorer

Retrieval logs

7. Streamlit UI

Query input

Agent mode panel

Multi-agent mode panel

Chunk explorer

RAG evaluation section

URL upload + file upload panels

6. Non-Functional Requirements
Performance

Retrieval under 300ms for 10k chunks

LLM latency depends on model, target < 1.5s

Reliability

Persistent vector store

Stable ingestion

Fail gracefully on bad URLs

Observability

Logging for retrieval, timing, chunks

UX

Clear answer + sources

Debug panels

Multi-agent explanation

7. User Stories
Core

As a PM, I want to ask any Snowflake question so that I can learn quickly.

As a data engineer, I want grounded answers so that I avoid incorrect assumptions.

As a new joiner, I want a fast way to onboard onto Snowflake.

Ingestion

As a user, I want to upload files so that I can use my own documentation.

As a PM, I want to ingest URLs so that I can reference external docs.

Agentic workflows

As a user, I want the agent to retry when it’s unsure.

As a PM, I want an evaluator agent that explains answer quality.

Debugging

As a developer, I want to see retrieved chunks so that I understand model behavior.

As a PM, I want grounding score so that I know if the answer is reliable.

8. Success Metrics
Category	Metric	Target
Retrieval Quality	relevance_score (0–1)	>0.75
Hallucination	hallucination_risk	<0.25
User Trust	Source citation completeness	100%
Performance	Retrieval latency	<300ms
Coverage	Questions answered w/o retry	80%
UX	Task success rate	90%
9. Roadmap (High-Level)
Phase	Timeline	Deliverable
Phase 1	Week 1–2	Basic RAG (you completed this)
Phase 2	Week 3	Agent + Multi-agent system
Phase 3	Week 4	Reranking, hybrid retrieval
Phase 4	Week 5	PDF ingestion, images, tables
Phase 5	Week 6	Production-ready UX, caching, embedding tuning
Phase 6	Week 7	Auto-reflection agent + eval harness
10. Open Questions

Should we support Snowflake SQL execution?

Should we store metadata (file source, URL, timestamp)?

Should we support vector re-ranking at scale?

🎉 End of PRD