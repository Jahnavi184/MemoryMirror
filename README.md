# 🪞 MemoryMirror

> *It connects the dots between your days, so you can finally see the pattern.*

An AI reflection companion powered by **Cognee** (graph-vector memory) and **Gemini**.
Unlike normal chatbots, MemoryMirror never forgets. It builds a knowledge graph of your
life and surfaces connections across weeks of entries.

---

## Setup

### 1. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 2. Add your API keys
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY and OPENAI_API_KEY
```
- **Gemini API key** (free) → https://aistudio.google.com/app/apikey
- **OpenAI API key** → https://platform.openai.com (used by Cognee for embeddings)

### 4. Seed demo data (run once, takes ~2 minutes)
```bash
python seed_data.py
```

### 4. Start the app
```bash
uvicorn main:app --reload
```

Open **http://localhost:8000** in your browser.

---

## Project structure

```
memorymirror/
├── main.py             # FastAPI backend — serves API + index.html
├── index.html          # React UI (no npm/node needed)
├── memory_engine.py    # All Cognee logic (store, retrieve, connect)
├── ai_companion.py     # Gemini API calls and prompt logic
├── seed_data.py        # Script to pre-load 3 weeks of journal entries
├── requirements.txt    # Python dependencies
├── .env.example        # Template for API keys
└── README.md
```

---

## Troubleshooting

**Page not loading?** — Make sure `uvicorn main:app --reload` is running, then open http://localhost:8000.

**Cognee errors during seed?** — Re-run `python seed_data.py`. It handles duplicates gracefully.

**`asyncio` errors?** — FastAPI handles async natively, so these should no longer occur.
