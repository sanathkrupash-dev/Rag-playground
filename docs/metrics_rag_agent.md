📏 Evaluation Metrics Spec — Snowflake RAG + Agent Assistant

Author: Sanath Srinivasan
Updated: {today}

🎯 Purpose

This document defines the evaluation framework for the Snowflake RAG + Agent platform.
It covers:

Retrieval quality

Grounded answer quality

Hallucination detection

Agent decision quality

UX-level success

These metrics ensure the assistant produces accurate, reliable, and grounded outputs — essential for a PM evaluating an LLM-powered system.

⭐ 1. Retrieval Metrics (Vector Search)
Metric	Definition	How to Calculate	Target
Recall@k	Out of all relevant chunks, how many were retrieved?	requires labeled gold set	> 0.80
Relevance Score	Semantic similarity between query and retrieved chunks	cosine_sim(query_emb, chunk_emb)	> 0.75
Distance Margin	Difference between top-1 and top-2 chunk scores	score1 - score2	> 0.10
Coverage	% of answers using >1 chunk	count(answers that used >=1 chunk) / total	> 90%
Latency	Time to retrieve chunks	measured in rag.retrieve()	< 300ms

These metrics measure how good the vector store is.

⭐ 2. RAG Answer Quality Metrics
Metric	Definition	Method	Target
Grounding Score	Similarity between answer and context	cosine_sim(answer_emb, context_emb)	> 0.75
Hallucination Risk	1 - grounding score	derived from above	< 0.25
Context Utilization	Degree to which the answer uses retrieved chunks	LLM judge: “Did answer use context?”	> 90%
Citation Coverage	% of answers including chunk sources	regex check	100%
Answer Accuracy	LLM evaluator correctness rating	evaluator_agent	> 0.85

These measure if the LLM answers correctly based on the provided context.

⭐ 3. Agent Performance Metrics
A. Tool-Calling Quality
Metric	Definition	Target
Tool Precision	% of times tool use was correct	> 90%
Tool Recall	% of times tool should be used and was used	> 85%
Misfires	Unnecessary tool calls	< 5%
Failovers	Agent retries after evaluator detects issues	tracked in orchestrator
B. Orchestrator Accuracy
Metric	Meaning
Retry Success Rate	% of retries resulting in better grounding
Route Accuracy	Does orchestrator send queries to correct agents?
Correction Quality	How much did query rewriting improve relevance?
⭐ 4. Evaluation via LLM-as-a-Judge (Evaluator Agent)

Your evaluator agent already produces JSON feedback.
Metrics extracted from evaluator:

relevance

grounding

hallucination_risk

missing_info

query_rewrite_needed

eval_notes

LLM-as-judge is essential for qualitative evaluation.

⭐ 5. Dataset for Evaluation (Mini Benchmark)

Your test set should include:

Atomic questions

Multi-hop questions

Definition questions

Operational questions

Cost, governance, architecture questions

Example benchmark:

ID	Query	Expected Chunks
1	What is a Snowflake warehouse?	warehouse definition chunk
2	How does Snowflake separate storage & compute?	scaling architecture chunk
3	What is the Data Cloud?	marketing chunk
4	What is RBAC?	security chunk

Aim for 20–50 questions.

⭐ 6. Metrics Dashboard (Future Work)

You will eventually build a dashboard with:

Retrieval latency chart

Grounding score histogram

Top queries by hallucination risk

Agent retry counts

Chunk distribution & size analytics

Source coverage

This fits your Week 4–5 roadmap.

⭐ 7. Acceptance Criteria (Launch-Ready)
Area	Requirement
Retrieval	Relevance > 0.75
Grounding	Grounding score > 0.75
Hallucination	Risk < 0.20
Agent Tool-Use	Correct tool call > 90%
UX	User task success > 90%
Stability	< 5% ingestion failures
⭐ 8. Risks & Mitigations
Risk	Impact	Mitigation
Poor embeddings	Wrong chunks retrieved	Use stronger models (MPNet)
Bad chunking	Missing context	Use semantic chunking + overlap
Tool misuse	Agent errors	Evaluator intervention
LLM hallucinations	Wrong answers	Grounding score + retry
Ingestion errors	Missing docs	Add alternative HTML extractor
🎉 End of Metrics Spec