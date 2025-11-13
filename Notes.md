# Week 1 Notes – RAG Basics

- RAG = Retrieval-Augmented Generation: retrieve relevant chunks from a knowledge base and feed them into the LLM.
- Useful when:
  - You have private / internal docs (Snowflake runbooks, governance docs, etc.)
  - You want answers grounded in specific content, not general web knowledge.
- Core steps:
  1. Ingestion: load docs → chunk → embed → store in vector DB.
  2. Retrieval: for a query, find top-k similar chunks.
  3. Generation: build a prompt with chunks + query → ask LLM.
