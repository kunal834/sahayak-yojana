"""Yojana Sahayak API server."""
import logging
import re
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from fastapi import FastAPI, HTTPException  # noqa: E402
from fastapi.responses import FileResponse  # noqa: E402
from fastapi.staticfiles import StaticFiles  # noqa: E402
from pydantic import BaseModel  # noqa: E402

import eligibility  # noqa: E402
import llm  # noqa: E402
from rag import Index, detect_schemes, expand_query, has_devanagari, is_generic, tokenize  # noqa: E402

log = logging.getLogger("yojana")
FRONTEND = Path(__file__).resolve().parent.parent / "frontend"
MIN_SCORE = 6.0  # below this BM25 score, no passage is relevant enough to answer from

index = Index()
app = FastAPI(title="Yojana Sahayak")

NOT_FOUND = {
    "en": "Sorry, I could not find this in the scheme documents I have. Please check the official portal myscheme.gov.in or ask at your nearest Common Service Centre (CSC).",
    "hi": "क्षमा करें, यह जानकारी मेरे पास मौजूद योजना दस्तावेज़ों में नहीं मिली। कृपया आधिकारिक पोर्टल myscheme.gov.in देखें या नज़दीकी कॉमन सर्विस सेंटर (CSC) पर पूछें।",
}

WHICH_SCHEME = {
    "en": "Which scheme are you asking about? For example: PM-KISAN, Ayushman Bharat, Ujjwala, Mudra loan, Sukanya Samriddhi or a scholarship. You can also use the \"Check eligibility\" tab to find schemes that match you.",
    "hi": "आप किस योजना के बारे में पूछ रहे हैं? जैसे: पीएम किसान, आयुष्मान भारत, उज्ज्वला, मुद्रा लोन, सुकन्या समृद्धि या छात्रवृत्ति। आप \"पात्रता जाँचें\" टैब से अपने लिए योजनाएँ भी खोज सकते हैं।",
}


class Turn(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    lang: str | None = None
    history: list[Turn] = []


class Profile(BaseModel):
    age: int | None = None
    gender: str | None = None
    income: int | None = None
    occupation: str | None = None
    state: str | None = None
    area: str | None = None
    category: str | None = None
    owns_land: bool | None = None
    income_tax_payer: bool | None = None
    has_pucca_house: bool | None = None
    has_bank_account: bool | None = None
    has_daughter_under_10: bool | None = None
    pregnant_or_lactating: bool | None = None
    class12_top20: bool | None = None
    has_lpg: bool | None = None


def _norm(s: str) -> str:
    s = s.lower().replace("**", "")
    s = re.sub(r"^\s*-\s*", " ", s, flags=re.M)
    return re.sub(r"\s+", " ", s).strip(" .")


def verify_quote(quote: str, chunk_text: str) -> bool:
    q, c = _norm(quote), _norm(chunk_text)
    if not q:
        return False
    if q in c:
        return True
    q_tokens = tokenize(q)
    c_tokens = set(tokenize(c))
    return bool(q_tokens) and sum(t in c_tokens for t in q_tokens) / len(q_tokens) >= 0.9


def _citation(chunk, quote: str, verified: bool) -> dict:
    doc = index.docs[chunk.doc_id]
    return {"chunk_id": chunk.id, "doc_id": doc.id, "title": doc.title, "title_hi": doc.title_hi,
            "section": chunk.section, "source": doc.source, "quote": quote, "verified": verified}


def offline_answer(question: str, lang: str, hits) -> dict:
    """Extractive answer used when no LLM is configured or the LLM call fails."""
    chunk = hits[0][0]
    q = set(expand_query(question))
    lines = [ln.strip("- ").strip() for ln in chunk.text.splitlines() if ln.strip()]
    ranked = sorted(lines, key=lambda ln: -len(q & set(tokenize(ln))))
    picked = [ln for ln in lines if ln in ranked[:4]]
    doc = index.docs[chunk.doc_id]
    head = (f"(ऑफ़लाइन मोड — स्रोत दस्तावेज़ का अंश)\n{doc.title_hi} — {chunk.section}:\n" if lang == "hi"
            else f"{doc.title} — {chunk.section}:\n")
    return {
        "found": True,
        "answer": head + "\n".join(f"- {ln}" for ln in picked),
        "citations": [_citation(chunk, ln, True) for ln in picked[:2]],
    }


@app.post("/api/chat")
def chat(req: ChatRequest):
    question = req.message.strip()
    if not question:
        raise HTTPException(400, "empty message")
    lang = req.lang if req.lang in ("en", "hi") else ("hi" if has_devanagari(question) else "en")

    # Follow-ups like "what documents do I need?" inherit the scheme named earlier in the chat.
    focus = []
    for turn in reversed(req.history):
        focus = detect_schemes(turn.content)
        if focus:
            break

    if not focus and is_generic(question):
        return {"found": False, "answer": WHICH_SCHEME[lang], "citations": [], "lang": lang,
                "mode": "clarify", "grounding": None, "retrieved": [], "search_query": question, "focus": []}

    search_query = question
    translated = None
    if has_devanagari(question) and llm.available():
        try:
            translated = llm.translate_query(question)
            search_query = f"{question} {translated}"
        except Exception as e:  # retrieval still works through the glossary
            log.warning("translation failed: %s", e)

    hits = index.search(search_query, k=6, focus_schemes=focus)
    retrieved = [{"chunk_id": c.id, "score": round(s, 2)} for c, s in hits]
    debug = {"retrieved": retrieved, "search_query": translated or question, "focus": focus}

    if not hits or hits[0][1] < MIN_SCORE:
        return {"found": False, "answer": NOT_FOUND[lang], "citations": [], "lang": lang,
                "mode": "retrieval", "grounding": None, **debug}

    if not llm.available():
        return {**offline_answer(question, lang, hits), "lang": lang, "mode": "offline",
                "grounding": None, **debug}

    by_id = {c.id: c for c, _ in hits}
    passages = [{"chunk_id": c.id, "title": index.docs[c.doc_id].title, "section": c.section, "text": c.text}
                for c, _ in hits]
    try:
        result = llm.answer(question, lang, passages, [t.model_dump() for t in req.history])
    except Exception as e:
        log.exception("LLM call failed")
        out = offline_answer(question, lang, hits)
        return {**out, "lang": lang, "mode": "offline", "error": str(e), "grounding": None, **debug}

    if not result.get("found"):
        return {"found": False, "answer": result.get("answer") or NOT_FOUND[lang], "citations": [],
                "lang": lang, "mode": "llm", "grounding": None, **debug}

    citations = []
    for s in result.get("sources", []):
        chunk = by_id.get(s.get("chunk_id"))
        if chunk:
            citations.append(_citation(chunk, s["quote"], verify_quote(s["quote"], chunk.text)))
        else:
            citations.append({"chunk_id": s.get("chunk_id"), "doc_id": None, "title": "Unknown passage",
                              "title_hi": "", "section": "", "source": "", "quote": s.get("quote", ""),
                              "verified": False})
    verified = sum(c["verified"] for c in citations)
    grounding = {"verified": verified, "total": len(citations),
                 "score": round(verified / len(citations), 2) if citations else 0.0}
    return {"found": True, "answer": result["answer"], "citations": citations, "lang": lang,
            "mode": "llm", "grounding": grounding, **debug}


@app.post("/api/eligibility")
def check_eligibility(profile: Profile):
    results = eligibility.evaluate(profile.model_dump())
    for r in results:
        doc = index.docs[r["scheme_id"]]
        r.update(title=doc.title, title_hi=doc.title_hi, source=doc.source, category=doc.category)
    return {"results": results}


@app.get("/api/schemes")
def schemes():
    return [{"id": d.id, "title": d.title, "title_hi": d.title_hi, "category": d.category,
             "source": d.source, "chunks": sum(c.doc_id == d.id for c in index.chunks)}
            for d in index.docs.values()]


@app.get("/api/schemes/{doc_id}")
def scheme(doc_id: str):
    doc = index.docs.get(doc_id)
    if not doc:
        raise HTTPException(404, "unknown scheme")
    return {"id": doc.id, "title": doc.title, "title_hi": doc.title_hi, "source": doc.source, "body": doc.body}


@app.get("/api/status")
def status():
    return {"llm": llm.available(), "model": llm.MODEL if llm.available() else None,
            "documents": len(index.docs), "chunks": len(index.chunks)}


@app.get("/")
def home():
    return FileResponse(FRONTEND / "index.html")


app.mount("/static", StaticFiles(directory=FRONTEND), name="static")
