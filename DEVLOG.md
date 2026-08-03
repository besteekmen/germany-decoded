# Development Log

This document records important engineering decisions made throughout the project.

The goal is not to document every code change, but to capture the reasoning behind architectural decisions, experiments, and implementation choices.

---

# Session 1 — Project Idea and Scope

## Project Idea

Defined the project vision.

Germany Decoded is an AI-powered legal information assistant that helps English-speaking residents of Germany understand German legal information using trusted official sources.

The goal is to demonstrate an end-to-end AI engineering workflow, including:

- data ingestion,
- retrieval systems,
- LLM integration,
- evaluation,
- monitoring,
- application development.

The assistant is designed to provide legal information, not replace professional legal advice.

---

## Key Decisions

- The assistant communicates in English.
- The knowledge base remains in German because official legal sources are primarily German.
- Official sources are preferred over unofficial summaries.
- Answers should always be grounded in retrieved documents.
- Responses should include citations and a legal disclaimer.

---

# Session 2 — Knowledge Ingestion Pipeline

## Source Selection

The first integrated source was:

**Gesetze im Internet**

Published by:

Federal Ministry of Justice  
(Bundesministerium der Justiz)

The German Civil Code (BGB) was selected as the initial knowledge source.

Reasons:

- It is an official source.
- It contains many everyday legal topics.
- It provides structured legal sections suitable for retrieval.

---

## Document Processing Decisions

Implemented a pipeline to:

- retrieve legal documents,
- extract legal sections,
- normalize content,
- store documents in PostgreSQL.

Each document stores:

- law name,
- section number,
- title,
- legal content,
- source metadata,
- language information.

---

# Session 3 — Retrieval System

## Initial Approach

Implemented semantic search using embeddings.

The reasoning:

Users usually describe problems in everyday language rather than legal terminology.

Example:

User:

> Can my landlord keep my deposit?

Legal source:

> Mietsicherheit

Semantic search allows matching by meaning instead of exact wording.

---

## Vector Storage

Selected:

- PostgreSQL
- pgvector

Reasons:

- keeps application data and vectors together,
- simple local deployment,
- suitable for RAG applications.

Added vector indexing using HNSW for efficient similarity search.

---

# Session 4 — Assistant and RAG Pipeline

## LLM Integration

Connected GPT-5 Mini to generate answers from retrieved legal context.

The assistant workflow:

1. Receive user question.
2. Retrieve relevant legal sections.
3. Provide retrieved context to the LLM.
4. Generate an English explanation.
5. Include citations and disclaimer.

---

## Prompt Design

Added instructions to:

- avoid unsupported claims,
- explain legal concepts clearly,
- reference retrieved sources,
- avoid presenting answers as legal advice.

---

# Session 5 — Monitoring and Application Features

## Conversation Tracking

Implemented PostgreSQL logging for:

- questions,
- generated answers,
- token usage,
- API costs,
- response timing.

---

## Feedback System

Added user feedback storage to collect information about answer usefulness.

---

## Admin Dashboard

Created an admin interface for inspecting:

- conversations,
- usage statistics,
- feedback.

---

# Session 6 — Retrieval Evaluation

## Evaluation Motivation

Retrieval quality is critical for RAG systems.

A good answer depends on retrieving the correct legal documents first.

Created:

- benchmark questions,
- expected legal sections,
- retrieval evaluation scripts,
- retrieval debugging tools.

---

## Evaluation Metrics

Implemented Hit@K evaluation.

Example:

Question:

> Can I reduce my rent because of mold?

Expected:
