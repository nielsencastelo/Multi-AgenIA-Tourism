# Multi-AgenIA-Tourism

**Multi-agent, locally runnable tourism assistant** for itinerary planning, logistics, policy Q&A, and trip reasoning.  
Designed to work **offline-first** with **Ollama (phi4)** or any OpenAI-compatible chat API, and to plug in a lightweight **RAG** layer for company docs (policies, fare rules, supplier T&Cs).

> Why multi-agent? Tourism workflows span data collection, constraints, optimization and tone-appropriate communication. Splitting work across specialized agents improves **traceability**, **robustness**, and **modularity**.

---

## ✨ Features

- **Agentic pipeline** split into:
  - **CityDataAgent** – fetch/parse destination facts (local DB/API or cached files)
  - **LogisticsAgent** – reason about transport options & constraints; outputs structured candidates
  - **ItineraryAgent** – builds day-by-day plans w/ alternates & assumptions
  - **PolicyAgent** – answers company policy Q&A using local RAG
  - **CommsAgent** – drafts short customer emails/messages
- **Local LLM** via **Ollama (phi4)** (no cloud required) or LangChain-compatible model
- **RAG-ready**: drop PDFs/CSVs/TXTs in `data/knowledge_base/` and index with a single command
- **FastAPI service** for programmatic use + **notebooks** for exploration
- **Deterministic JSON I/O** between agents for easier debugging and evaluation

---

## 🚀 Quickstart

### 1) Python & system prerequisites
- Python **3.10+**
- (Recommended) Create a virtual env:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

### 3) Run a local LLM (Ollama)
- Install Ollama: https://ollama.com/download
- Pull and run `phi4`:
```bash
ollama pull phi4
ollama serve
```

### 4) Environment variables
Copy `.env.example` to `.env` and set what you need:
```
# Choose your local endpoint/model (default matches Ollama)
OLLAMA_ENDPOINT=http://localhost:11434
OLLAMA_MODEL=phi4

# Optional: point to OpenAI-compatible provider
# OPENAI_API_KEY=...
# OPENAI_BASE_URL=...
```

### 5) Start the API
```bash
uvicorn src.api.app:app --reload --port 8000
```
Then open: `http://localhost:8000/docs`

---

## 🧠 Using the Agents

### Example payloads

**Itinerary (5-day plan)**
```json
{
  "traveler_profile": "couple in their 30s from Dublin",
  "destination": "Lisbon",
  "month": "September",
  "budget": "€1500",
  "interests": ["food markets", "historic neighborhoods", "scenic viewpoints"]
}
```

**Policy Q&A**
```json
{
  "policy_excerpt": "Refunds allowed within 24h for EU flights; non-EU depends on fare rules.",
  "question": "Can we refund a non-EU return ticket after 48 hours if the fare is Basic Economy?"
}
```

**Price/Option reasoning**
```json
{
  "origin": "Dublin (DUB)",
  "destination": "New York (JFK)",
  "dates": "2025-10-10 to 2025-10-17"
}
```

Each endpoint responds with:
- **assumptions** (explicit)
- **structured JSON** (candidates, day-by-day plan, trade-offs)
- **verification_steps** (to check live prices/availability)

---

## 🔌 LLM Integration

- Default client uses **Ollama** (chat endpoint `/api/chat`).
- Automatically falls back to LangChain `ChatOllama` if installed.
- To switch to OpenAI-compatible backends, set `OPENAI_API_KEY` and (optionally) `OPENAI_BASE_URL`.

> Keep **temperature** low (e.g., `0.2–0.4`) for business logic; use higher values only in the CommsAgent.

---

## 📚 RAG (Local Knowledge)

1) Put documents in `data/knowledge_base/` (PDF/CSV/TXT).  
2) Run the indexer (example CLI):
```bash
python -m src.rag.index --input data/knowledge_base --persist .chroma
```
3) PolicyAgent will use the vector store for semantic retrieval before answering.

---

## 🧪 Testing

- Unit tests in `tests/` (pytest).
- Contract tests validate the **schemas** (pydantic) exchanged between agents.
- Add sample inputs/outputs in `data/samples/` to lock baseline behavior.

---

## 🗺️ Roadmap

- [ ] Deterministic **LangGraph** orchestration option (besides CrewAI)
- [ ] Calendar-aware suggestions (opening hours, travel time buffers)
- [ ] Simple MILP heuristic for activity scheduling (hard constraints)
- [ ] Structured **critique/self-check** step for each agent
- [ ] Evaluation harness with human preference annotations

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Open an issue to discuss major changes.
2. Follow the code style used in `src/`.
3. Add tests when relevant.

---

## 📝 License

Choose a license that matches your goals. **MIT** is a good default for open projects.  
(If you add one, include a `LICENSE` file at the repo root.)

---

## 🔎 References & Background

- Repository landing page (this project): https://github.com/nielsencastelo/Multi-AgenIA-Tourism  
- Multi-agent tourism recommender (architectures, agents):  
  - Sebastia et al., *A Multi Agent Architecture for Tourism Recommendation* (Springer) – conceptual grounding for multi-agent flows.  
  - ResearchGate diagram of multiagent tourism recommender (T-Agent & P-Agents) – useful for role decomposition.  
- Sustainable tourism & datasets (for future RAG):  
  - Czech Journal of Tourism (2018) – MAS in sustainable tourism.  
  - EU tourism data overview – indicators & public datasets.

> These references inspire the **agent roles**, **data flows**, and **evaluation angles** but the code here is original and tailored for local LLMs.
