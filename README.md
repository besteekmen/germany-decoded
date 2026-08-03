# 🇩🇪 Germany Decoded

> An AI-powered legal information assistant that helps English-speaking residents of Germany understand German legal information using trusted official sources.

---

## Overview

Germany Decoded is an AI application that combines document ingestion, retrieval systems, and large language models to make German legal information easier to access.

Many important legal and administrative resources in Germany are written in German and use complex legal terminology. This creates a barrier for people who need to understand their rights but are not familiar with the German legal system.

The goal of Germany Decoded is to provide clear English explanations of German legal information while grounding answers in official sources.

The project is designed as a **Retrieval-Augmented Generation (RAG) application**:

- retrieve relevant legal information from trusted sources,
- provide the retrieved context to an LLM,
- generate understandable explanations,
- include citations and legal disclaimers.

The assistant is designed to provide legal information, not legal advice.

---

# Project Goals

Germany Decoded aims to:

- Make German legal information more accessible.
- Retrieve information from trusted official sources.
- Explain legal concepts in clear English.
- Provide citations for retrieved sources.
- Communicate uncertainty when information is incomplete.
- Demonstrate a complete production-style AI application workflow.

---

# How It Works

The system consists of several components:

```
                 User Question
                      |
                      v
                AI Assistant
                      |
                      v
             Retrieval Pipeline
                      |
        +-------------+-------------+
        |                           |
        v                           v
 Semantic Search              Keyword Search
   (pgvector)                    (PostgreSQL FTS)
        |                           |
        +-------------+-------------+
                      |
                      v
              Relevant Documents
                      |
                      v
                  GPT-5 Mini
                      |
                      v
        English Explanation + Citations
```

---

# Architecture Components

## 1. Knowledge Ingestion

The system starts by building a legal knowledge base from official sources.

Current source:

- German Civil Code (Bürgerliches Gesetzbuch — BGB)

The ingestion pipeline:

- downloads legal documents,
- extracts legal sections,
- normalizes the data,
- stores documents in PostgreSQL.

Each document contains information such as:

- law name,
- section number,
- title,
- legal text,
- source information,
- language metadata.

---

## 2. Vector Database and Semantic Search

Legal questions are often expressed differently from legal documents.

For example:

User:

> Can my landlord keep my deposit?

Legal document:

> Begrenzung und Anlage von Mietsicherheiten

Because users do not always know legal terminology, Germany Decoded uses semantic search.

The system:

- creates embeddings for documents,
- stores them using PostgreSQL + pgvector,
- retrieves documents based on meaning rather than exact words.

This allows the system to connect everyday questions with relevant legal sections.

---

## 3. Hybrid Retrieval

Semantic search is powerful, but legal information also benefits from exact terminology matching.

Germany Decoded combines:

### Semantic Search

Uses embeddings to find documents with similar meaning.

### PostgreSQL Full Text Search

Uses German legal terminology matching.

The hybrid approach improves retrieval by combining:

- understanding of user intent,
- matching of official legal language.

---

## 4. Assistant Application

The assistant uses GPT-5 Mini to generate answers.

The assistant:

1. Receives the user's question.
2. Retrieves relevant legal documents.
3. Uses retrieved documents as context.
4. Generates an English explanation.
5. Provides citations.
6. Includes a legal disclaimer.

Example:

**Question**

> My apartment has mold. Can I reduce my rent?

**Assistant**

The system retrieves the relevant BGB sections and explains the applicable rules in English.

---

# Evaluation

A retrieval system needs to be measured, not only tested manually.

Germany Decoded includes a retrieval evaluation pipeline.

Current evaluation features:

- benchmark questions,
- expected legal sections,
- retrieval debugging,
- Hit@K metrics.

Example:

Question:

```
Can I reduce my rent because of mold?
```

Expected:

```
BGB §536
```

The system evaluates whether the correct document appears in the retrieved results.

Current experiments include:

- semantic retrieval,
- hybrid retrieval,
- retrieval weighting.

Current benchmark result:

- Total Questions = 10
- Hit@1 = 30%
- Hit@3 = 70%
- Hit@5 = 70%

The evaluation checks whether the expected legal section appears in the retrieved documents.

---

# Monitoring and Admin Features

The application also includes monitoring functionality.

Tracked information:

- conversations,
- response latency,
- token usage,
- API costs,
- user feedback.

The project includes a separate Streamlit admin dashboard for inspecting application usage, performance metrics, and user feedback.

---

# Running Locally

Germany Decoded can be run locally with your own API key and database.

The project uses:

- Python
- uv for dependency management
- Docker for PostgreSQL + pgvector
- OpenAI API for answer generation

---

## Requirements

Install:

- Python 3.12+
- uv
- Docker

You also need an OpenAI API key.

---

## 1. Clone the repository

```bash
git clone <repository-url>

cd germany-decoded
```

---

## 2. Install dependencies

Install the project environment:

```bash
uv sync
```

---

## 3. Configure environment variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key

POSTGRES_DB=germany_decoded
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=admin
POSTGRES_PASSWORD=password
```

---

## 4. Start PostgreSQL

Start the database:

```bash
make up
```

This starts PostgreSQL with pgvector enabled.
---

## 5. Initialize the database

Create the required tables:

```bash
make init-db
```

---

## 6. Build the knowledge base

Download and process the legal source documents:

```bash
make index
```
This creates embeddings and stores the legal documents in PostgreSQL.
---

## 7. Run the assistant

Start the main Streamlit application:

```bash
make app
```

The application allows users to:
- ask questions in English,
- retrieve relevant German legal sections,
- receive English explanations,
- view source citations,
- provide feedback.

---

## 8. Run the monitoring dashboard

The project also includes an admin dashboard:

```bash
make monitor
```

The dashboard displays:
- total questions,
- latency metrics,
- token usage,
- API costs,
- user feedback.

---

## 8. Run evaluation

The retrieval pipeline can be evaluated with:

```bash
make eval-retrieval
```

Debug retrieval results with:

```bash
make debug-retrieval
```

---

## Database Management

Reset the database:

```bash
make reset-db
```

Stop services:

```bash
make down
```

---

# Tech Stack

## Backend

- Python
- PostgreSQL
- pgvector
- Docker
- uv

## AI

- OpenAI API
- GPT-5 Mini
- Sentence Transformers
- Embeddings

## Retrieval

- Multilingual embeddings
- PostgreSQL + pgvector
- Vector similarity search
- PostgreSQL Full Text Search
- Hybrid retrieval

## Application

- Streamlit assistant interface
- Streamlit admin dashboard
- Monitoring system
- Makefile-based workflow

---

# Development Progress

## Completed

### Project Setup

- Python project setup
- Dependency management with uv
- Docker configuration
- PostgreSQL setup
- pgvector configuration

### Knowledge Ingestion

- BGB source selection
- Legal document loader
- Document normalization
- Database storage pipeline

### Retrieval

- Multilingual embeddings
- Vector storage with PostgreSQL + pgvector
- Semantic search
- PostgreSQL Full Text Search
- Hybrid retrieval
- Retrieval evaluation pipeline

### Assistant

- GPT-5 Mini integration
- Prompt design
- English explanations
- Source citations
- Legal disclaimer

### Monitoring

- Conversation logging
- Token tracking
- Cost tracking
- Feedback collection
- Admin dashboard

---

# Future Improvements

Planned improvements:

- Better document chunking strategies
- Retrieval reranking
- Confidence estimation
- LLM-as-a-Judge evaluation
- Better citation formatting
- Conversation history
- Official web search fallback
- Multi-source legal retrieval
- Deployment

---

# Why This Project?

Germany Decoded was built as a practical AI engineering project to demonstrate the complete lifecycle of an LLM application.

The project covers:

- building a knowledge pipeline,
- storing and retrieving documents,
- implementing RAG,
- evaluating retrieval quality,
- monitoring AI systems,
- connecting an LLM to real-world data,
- building a usable AI product.

---

# Data Sources

Germany Decoded uses publicly available official sources.

Legal documents are generated locally and are not stored inside this repository.

See:

```
SOURCES.md
```

for more information.

---

# Disclaimer

Germany Decoded provides legal information based on retrieved official sources.

It is not a substitute for professional legal advice.

Users should consult qualified legal professionals when making important legal decisions.

---

# License

MIT License