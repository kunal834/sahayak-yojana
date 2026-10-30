# Yojana Sahayak — योजना सहायक

A multilingual (Hindi + English) AI assistant that tells citizens which government schemes they qualify for, what documents they need and how to apply. **Every answer cites its source document, and every cited quote is verified in code against the source.**

INNOVISTA 36-hour hackathon · Problem Statement 03.

## What it does

| Requirement | How it is built |
|---|---|
| 10–20 public scheme documents | 17 documents in [data/schemes/](data/schemes/): PM-KISAN, Ayushman Bharat PM-JAY, Ujjwala, PMAY-Urban 2.0, Sukanya Samriddhi, Atal Pension, PMJJBY, PMSBY, PM Fasal Bima, Kisan Credit Card, Post-Matric Scholarship (SC), Central Sector Scholarship, PM Mudra, PM SVANidhi, PMMVY, MGNREGA, Majhi Ladki Bahin (Maharashtra). Each records its official source URL. Drop extra `.md`, `.txt` or `.pdf` files into the folder and they are indexed on start. |
| RAG chatbot in Hindi and English | BM25 retrieval over section-level chunks → Claude answers **only** from the retrieved passages. Hindi questions are matched through a Hindi/Hinglish glossary and an LLM query translation step. |
| Cite every answer | Each answer lists the scheme, section and an exact quote. Click a citation to open the document with the quote highlighted. |
| No guessing | Three layers. (1) If no passage scores above a relevance threshold, the bot says "not in my documents" without calling the LLM. (2) The model returns `found: false` when the passages don't answer the question. (3) Questions with no topic ("What documents are required?") get a "which scheme?" reply. |
| Eligibility questionnaire | Rule engine ([backend/eligibility.py](backend/eligibility.py)) written from the documents. Returns **eligible / maybe / not eligible** with a ✅ ❌ ❔ checklist per condition. Unknown answers give "maybe", never a false "yes". |
| **Bonus:** hallucination detection | The model must copy verbatim English quotes for each fact. The server checks every quote against the cited passage and shows "✓ 3/3 quotes verified" or "⚠ 2/3 verified". |
| **Bonus:** voice | 🎤 speech input (hi-IN / en-IN) and 🔊 read-aloud, using the browser Web Speech API (Chrome / Edge). |
| **Bonus:** WhatsApp-style UI | Chat bubbles, suggestion chips, mobile-first layout, dark mode. |

Follow-up questions keep context: ask about Mudra, then "what documents are required?", and the answer stays on Mudra.

## Run it

```bash
pip install -r requirements.txt
copy .env.example .env        # then put your ANTHROPIC_API_KEY in .env
cd backend
python -m uvicorn app:app --port 8000
```

Open http://localhost:8000. On Windows you can just double-click `run.bat`.

**No API key?** The app still runs. It works in offline mode and shows the most relevant passage from the source document with its citation. The header shows which mode is active.

## Architecture

```
frontend/ (HTML + JS, no build step)
   │  POST /api/chat        POST /api/eligibility      GET /api/schemes[/id]
backend/app.py (FastAPI)
   ├─ rag.py          load .md/.pdf → chunk by section → BM25 + Hindi glossary
   │                  + scheme-name detection + section-intent boost
   ├─ llm.py          Claude (claude-opus-5-5): Hindi→English query translation,
   │                  grounded answer as JSON {found, answer, sources[{chunk_id, quote}]}
   ├─ quote verifier  every quote string-matched against its passage
   └─ eligibility.py  deterministic rules → eligible / maybe / not eligible
```

Claude calls use structured JSON output, low effort for speed, and server-side refusal fallbacks (`fallbacks: "default"`). If the LLM call fails, the bot falls back to the extractive offline answer instead of crashing.

## Demo script (3 minutes)

1. **English Q&A:** "Am I eligible for PM-KISAN?" → answer, citations and a "✓ verified" badge. Click a citation to show the highlighted source.
2. **Follow-up:** "What documents do I need?" → stays on PM-KISAN.
3. **Hindi:** switch to हिं and ask "गर्भवती महिला को कितना पैसा मिलता है?" → Hindi answer citing PMMVY. Tap 🔊.
4. **Voice:** tap 🎤 and say "मुद्रा लोन कैसे मिलेगा".
5. **No guessing:** "What is the capital of France?" → "Not found in documents".
6. **Eligibility:** enter a 34-year-old woman farmer in rural Maharashtra with income ₹1.8 lakh → PM-KISAN, Fasal Bima, KCC, Ladki Bahin and more, each with a checklist. Then tap "Ask about this".

## Future ideas

- Scrape myscheme.gov.in to cover 500+ central and state schemes, with automatic refresh when rules change.
- Multilingual embeddings for hybrid search; Bhashini / AI4Bharat for Marathi, Tamil, Bengali and more.
- WhatsApp Business API bot, so citizens can use it without installing anything.
- Help-desk mode: save a citizen profile and generate a printable document checklist.
- Deploy on Cloud Run / AWS App Runner with the index in a managed vector store.

## Data note

Scheme documents summarise publicly available information from official government portals (linked in each file). Amounts and rules change, so always confirm on the official source before applying. No personal data is stored.
