# TODO

## ✅ Milestone 1 — Project Setup

- [x] Create GitHub repository
- [x] Initialize project with `uv`
- [x] Configure environment variables
- [x] Create project structure
- [x] Add project documentation
- [x] Configure Docker + PostgreSQL
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
- [ ] Evaluate retrieval quality

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

## 🔄 Milestone 5 — Monitoring (Current)

- [x] Log every conversation
- [x] Measure latency
- [x] Measure token usage
- [x] Measure costs
- [x] Store conversations in PostgreSQL
- [x] Store user feedback
- [x] Build monitoring dashboard
- [ ] Build admin dashboard

---

## ⏳ Milestone 6 — Evaluation

- [ ] Retrieval evaluation
- [ ] LLM-as-a-Judge
- [ ] Improve chunking
- [ ] Improve prompts
- [ ] Build retrieval debugger

---

## ⏳ Milestone 7 — Search Improvements

- [ ] Hybrid search (semantic + keyword)
- [ ] PostgreSQL Full Text Search
- [ ] Reranking

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