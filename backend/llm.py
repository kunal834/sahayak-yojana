"""Claude calls: Hindi query translation and grounded answer generation."""
import json
import os

import anthropic

MODEL = os.getenv("YOJANA_MODEL", "claude-opus-5-5")

ANSWER_SCHEMA = {
    "type": "object",
    "properties": {
        "found": {"type": "boolean"},
        "answer": {"type": "string"},
        "sources": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "chunk_id": {"type": "string"},
                    "quote": {"type": "string"},
                },
                "required": ["chunk_id", "quote"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["found", "answer", "sources"],
    "additionalProperties": False,
}

SYSTEM_PROMPT = """You are Yojana Sahayak, a helpful assistant that explains Indian government schemes to citizens, farmers, students and help-desk volunteers.

You answer ONLY from the numbered passages provided in the user message. Never use outside knowledge, even if you know the scheme well, because the person will act on your answer and it must be traceable to an official document.

How to answer:
- Write the answer in the language requested (English or Hindi). For Hindi, use simple everyday Hindi in Devanagari; keep scheme names, amounts and portal names recognisable (e.g. "PM-KISAN", "Rs 6,000", "pmkisan.gov.in").
- Use plain words a first-time reader understands. Short sentences. Use "-" bullet lists for eligibility conditions, documents and steps.
- If the person describes their situation ("I am a 25 year old farmer..."), compare it with the conditions in the passages and say clearly whether they appear eligible, not eligible, or what extra detail is needed.
- Name the scheme(s) the answer is about.
- If the passages do not contain the information needed, set "found" to false and say briefly (in the requested language) that the documents you have do not cover this, and suggest the official source if one appears in the passages. Do not guess.

Sources: for every fact in your answer, add an entry to "sources" with the passage's chunk_id and a short quote copied EXACTLY, word for word, from that passage (in its original English). These quotes are verified automatically by string matching, so do not paraphrase, translate or merge sentences inside a quote."""


def available() -> bool:
    return bool(os.getenv("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_AUTH_TOKEN"))


_client = None


def client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(timeout=90.0)
    return _client


def _text(response) -> str:
    return next((b.text for b in response.content if b.type == "text"), "")


def translate_query(query: str) -> str:
    response = client().messages.create(
        model=MODEL,
        max_tokens=2000,
        output_config={"effort": "low"},
        system="Translate the user's question about Indian government schemes into a short English search query. Reply with the English query only.",
        messages=[{"role": "user", "content": query}],
    )
    return _text(response).strip()


def answer(question: str, lang: str, passages: list[dict], history: list[dict]) -> dict:
    blocks = "\n\n".join(
        f'<passage chunk_id="{p["chunk_id"]}" scheme="{p["title"]}" section="{p["section"]}">\n{p["text"]}\n</passage>'
        for p in passages
    )
    convo = ""
    if history:
        lines = [f'{"User" if h["role"] == "user" else "Assistant"}: {h["content"][:400]}' for h in history[-6:]]
        convo = "Conversation so far (for context only):\n" + "\n".join(lines) + "\n\n"
    language = "Hindi (Devanagari script)" if lang == "hi" else "English"
    user_msg = f"{convo}Passages:\n{blocks}\n\nQuestion: {question}\n\nAnswer language: {language}"

    response = client().beta.messages.create(
        model=MODEL,
        max_tokens=8000,
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        output_config={"effort": "low", "format": {"type": "json_schema", "schema": ANSWER_SCHEMA}},
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_msg}],
    )
    if response.stop_reason == "refusal":
        raise RuntimeError("model declined the request")
    return json.loads(_text(response))
