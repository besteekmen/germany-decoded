# 🇩🇪 Germany Decoded

> An AI-powered legal information assistant that helps English-speaking residents of Germany understand their rights and obligations using official German legal and governmental sources.

---

## Motivation

Living in Germany often means navigating legal and administrative information that is primarily available in German and spread across many official websites. While large language models can provide helpful answers, they may not always rely on authoritative or up-to-date sources.

This project aims to make trusted German legal information more accessible by retrieving relevant official documents and explaining them in clear English.

The assistant is designed to answer practical questions related to everyday life in Germany while always citing the sources used to generate its responses.

Examples include questions about:

* Housing and tenancy
* Employment rights
* Consumer protection
* Contracts and debt
* Official procedures
* Everyday civil law

---

## Project Goals

* Retrieve information from trusted German legal and governmental sources.
* Explain legal information in clear English.
* Cite every relevant source.
* Communicate uncertainty when information is incomplete.
* Suggest practical next steps.
* Demonstrate a complete Retrieval-Augmented Generation (RAG) pipeline.

---

## Current Status

🚧 This project is currently under active development.

The initial focus is building a reliable knowledge ingestion and retrieval pipeline before adding advanced agent capabilities.

---

## Planned Features

* [ ] Knowledge ingestion pipeline
* [ ] Vector database with pgvector
* [ ] Retrieval-Augmented Generation (RAG)
* [ ] English responses from German source material
* [ ] Source citations
* [ ] Confidence estimation
* [ ] Suggested next steps
* [ ] Evaluation pipeline
* [ ] Monitoring and tracing
* [ ] Official web search fallback

---

## Example Interaction (Planned)

**Question**

> My landlord wants to renovate my apartment next week. Is this allowed?

**Assistant**

* Retrieves relevant German legislation.
* Retrieves official government guidance.
* Explains the applicable rules in English.
* Cites every source used.
* Indicates confidence.
* Suggests possible next steps.
* Reminds the user that the response is legal information rather than legal advice.

---

## Tech Stack

* Python
* uv
* GitHub Codespaces
* PostgreSQL
* pgvector
* OpenAI API
* OpenTelemetry
* VS Code

---

## Repository Documentation

* **PROJECT_BLUEPRINT.md** — Overall vision, design decisions, and project scope.
* **TODO.md** — Development roadmap and milestones.
* **DEVLOG.md** — Engineering journal documenting project progress.

---

## Disclaimer

This project provides legal information based on trusted German legal and governmental sources.

It is **not** a substitute for professional legal advice and should not be relied upon for legal decisions. Users should consult a qualified legal professional when appropriate.

---

## License

MIT License
