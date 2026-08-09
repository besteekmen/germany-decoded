# TODO

## ✅ Milestone 1 — Project Setup

- [x] Create GitHub repository
- [x] Initialize project with `uv`
- [x] Configure environment variables
- [x] Create project structure
- [x] Add project documentation
- [x] Fully containerize application + PostgreSQL with Docker Compose
- [x] Configure pgvector
- [x] Create Makefile

> Codespaces skipped for now (local WSL development).

---

## ✅ Milestone 2 — Knowledge Ingestion

- [x] Select first official source (BGB)
- [x] Implement BGB loader
- [x] Normalize legal sections
- [ ] Add additional official sources
- [x] Design document schema
- [x] Build indexing pipeline
- [x] Store documents in PostgreSQL

---

## ✅ Milestone 3 — Retrieval

- [x] Generate multilingual embeddings
- [x] Store vectors in PostgreSQL + pgvector
- [x] Build semantic search
- [x] Create HNSW vector index
- [x] Evaluate retrieval quality

---

## ✅ Milestone 4 — Question Answering

- [x] Connect GPT-5 Mini
- [x] Build prompt template
- [x] Build legal instructions
- [x] Generate English answers
- [x] Add citations
- [x] Add legal disclaimer
- [ ] Add confidence estimation

---

## ✅ Milestone 5 — Monitoring

- [x] Log every conversation
- [x] Measure latency
- [x] Measure token usage
- [x] Measure actual API costs
- [x] Store conversations in PostgreSQL
- [x] Store user feedback
- [x] Build monitoring dashboard
- [x] Build admin dashboard
- [x] Add 5 monitoring charts

---

## ✅ Milestone 6 — Evaluation

- [x] Build benchmark dataset
- [x] Retrieval evaluation
- [x] Compare semantic vs hybrid retrieval
- [x] Evaluate Hit@1 / Hit@3 / Hit@5 / MRR
- [x] Select best retrieval approach for production
- [x] Build retrieval debugger
- [x] Hybrid search (semantic + keyword)
- [x] PostgreSQL Full Text Search
- [x] Query rewriting
- [x] LLM-as-a-Judge
- [ ] Compare multiple RAG prompt approaches
- [ ] Experiment with chunking
- [ ] Reranking

---

## ⏳ Milestone 7 — Product Polish

- [x] Merge Assistant + Admin
- [x] Admin-only navigation
- [x] Better dashboard visuals
- [x] Charts
- [x] Better branding
- [x] Loading animations
- [x] Conversation history
- [ ] Better citations
- [ ] Deployment

---

## 🌟 Future Features

- [ ] Official web search fallback
- [ ] Conversation memory
- [ ] Explain official letters
- [ ] Deadline extraction
- [ ] Draft response letters
- [ ] Bureaucracy assistant
- [ ] Upload German documents
- [ ] Multi-source legal retrieval

---

## 🚀 Stretch Goal

- [ ] OpenTelemetry tracing
- [ ] Grafana dashboards
- [ ] Production observability