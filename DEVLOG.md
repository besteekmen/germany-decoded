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

A good answer depends on retrieving the correct legal documents before generation.

Created:

- benchmark questions,
- expected legal sections,
- retrieval evaluation scripts,
- retrieval debugging tools.

---

## Evaluation Metrics

The retrieval benchmark uses:

- Hit@1
- Hit@3
- Hit@5
- Mean Reciprocal Rank (MRR)

Hit@K measures whether the expected legal section appears within the first K retrieved documents.

MRR also considers how highly the correct section is ranked.

Because the production assistant passes the top 3 retrieved documents to the LLM, Hit@3 is used as the primary retrieval-selection metric.

---

# Session 7 — Hybrid Retrieval and Query Rewriting

## Hybrid Search

The initial retrieval system used semantic vector search only.

To improve retrieval of exact legal terminology and section-specific language, PostgreSQL Full Text Search was added.

Hybrid retrieval combines:

- semantic search using multilingual embeddings,
- PostgreSQL Full Text Search,
- LLM-based rewriting of English user questions into short German legal search terms.

The semantic and keyword scores are combined to produce the final ranking.

---

## Retrieval Comparison

Semantic and hybrid retrieval were evaluated on the same benchmark.

| Metric | Semantic | Hybrid |
|:------:|---------:|-------:|
| Hit@1 | 40% | 30% |
| Hit@3 | 40% | 70% |
| Hit@5 | 50% | 70% |
| MRR | 0.420 | 0.483 |

Semantic retrieval performed better at Hit@1, but hybrid retrieval substantially improved Hit@3, Hit@5, and MRR.

Since the production assistant uses the top 3 retrieved documents as context, hybrid retrieval was selected as the production strategy.

---

# Session 8 — Monitoring Improvements

The monitoring dashboard was expanded to satisfy both operational needs and project evaluation requirements.

The dashboard now includes five charts:

1. Response Time
2. Token Usage
3. Feedback Distribution
4. LLM Judge Distribution
5. Questions Over Time

User thumbs-up and thumbs-down feedback continues to be stored in PostgreSQL.

The Admin Dashboard therefore provides both user feedback collection and visual monitoring of system behavior.

---

# Session 9 — Full Docker Containerization

## Previous Setup

Initially, Docker Compose was used only for PostgreSQL/pgvector while the Python application, indexing pipeline, and evaluations ran directly in the local WSL environment.

## Updated Architecture

The project was fully containerized using:

- `Dockerfile` for the Python/Streamlit application,
- Docker Compose for the application and PostgreSQL/pgvector,
- a persistent PostgreSQL volume,
- a Hugging Face model cache volume.

The application connects to PostgreSQL through the Docker Compose service hostname `postgres`.

The Makefile was updated so database initialization, indexing, CLI execution, Streamlit, and evaluation commands can all run inside the application container.

A fresh environment can now be prepared with:

```bash
make setup
```

This builds the application image, starts PostgreSQL, initializes the database, indexes the BGB knowledge base, and starts Streamlit.

# Session 10 — RAG Prompt Evaluation

Two generation prompts were evaluated while keeping retrieval and the
retrieved context identical.

| Prompt | Relevant | Partly Relevant | Not Relevant | Score |
|:------:|---------:|----------------:|-------------:|------:|
| V1 | 6 | 4 | 0 | 80% |
| V2 | 5 | 5 | 0 | 75% |

The existing V1 prompt performed better and was retained as the production
prompt. This experiment showed that adding more explicit instructions did
not automatically improve answer relevance.
