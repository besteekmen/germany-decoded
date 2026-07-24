# Development Log

This document records important engineering decisions made throughout the project.
The goal is not to document every code change, but to capture the reasoning behind architectural and implementation decisions.

---

## Session 1

### Project Idea

Defined the project vision.
The assistant will help English-speaking residents of Germany understand their rights and obligations using trusted legal and governmental sources.
The project is intended to demonstrate an end-to-end AI engineering workflow rather than function as a replacement for legal professionals.

---

### Key Decisions

* The assistant communicates in English.
* The knowledge base remains in German.
* Official sources are preferred over unofficial summaries.
* Every factual answer should include citations.
* The assistant provides legal information rather than legal advice.

---

### Technology Choices

* Python
* uv
* GitHub Codespaces
* PostgreSQL + pgvector
* OpenAI API
* OpenTelemetry

---

### Next Steps

Begin building the knowledge ingestion pipeline by selecting the first trusted source and implementing the initial document loader.
