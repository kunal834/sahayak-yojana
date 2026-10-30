"""Full self-check for Yojana Sahayak against every requirement of Problem Statement 03.

Start the server first, then run:   python check.py          (add -v to see every check)
"""
import json
import sys
import urllib.request

BASE = "http://127.0.0.1:8000"
VERBOSE = "-v" in sys.argv
results = {}  # requirement -> [passed, failed, failures]


def call(path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data, {"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=180))


def ask(message, history=None, lang=None):
    return call("/api/chat", {"message": message, "history": history or [], "lang": lang})


def check(req, name, ok, detail=""):
    r = results.setdefault(req, [0, 0, []])
    r[0 if ok else 1] += 1
    if not ok:
        r[2].append(f"{name}  ({detail})" if detail else name)
    if VERBOSE or not ok:
        print(f"  {'PASS' if ok else 'FAIL'}  [{req}] {name}" + (f"  ({detail})" if detail and not ok else ""))


def is_hindi(text):
    return sum("ऀ" <= ch <= "ॿ" for ch in text) > 10


try:
    status = call("/api/status")
except Exception as e:
    sys.exit(f"Server not reachable at {BASE} - start it first ({e})")
schemes = call("/api/schemes")
ai = status["llm"]
print(f"\nMode: {'AI (' + status['model'] + ')' if ai else 'OFFLINE (no API key) - AI-only checks are skipped'}")
print(f"{status['documents']} documents, {status['chunks']} passages\n")

# ---------------------------------------------------------------- 1. Document collection
R1 = "1 Documents"
check(R1, "10 to 20 scheme documents", 10 <= len(schemes) <= 20, len(schemes))
for s in schemes:
    check(R1, f"{s['id']}: has official source URL", s["source"].startswith("http"), s["source"])
    check(R1, f"{s['id']}: has Hindi title", bool(s["title_hi"]))
    body = call(f"/api/schemes/{s['id']}")["body"].lower()
    for section in ("eligib", "document", "apply"):
        check(R1, f"{s['id']}: covers '{section}'", section in body)
cats = {s["category"] for s in schemes}
for needed in ("agriculture", "education", "health"):
    check(R1, f"includes {needed} schemes (PS asks for PM-KISAN, scholarships, Ayushman)", needed in cats)
check(R1, "includes a state scheme", any("maharashtra" in s["id"] for s in schemes))

# ---------------------------------------------------------------- 2. RAG chatbot, every scheme, both languages
R2 = "2 RAG Q&A"
for s in schemes:
    for q, lang in [(f"Who is eligible for {s['title']}?", "en"),
                    (f"What documents do I need for {s['title']}?", "en"),
                    (f"{s['title_hi']} के लिए कौन से दस्तावेज़ चाहिए?", "hi")]:
        r = ask(q)
        cited = [c["doc_id"] for c in r["citations"]]
        check(R2, f"{s['id']} / {lang}: '{q[:50]}' cites the right scheme", r["found"] and cited and cited[0] == s["id"],
              f"cited {cited}")

natural = [
    ("I am a farmer, how do I get Rs 6000 per year?", "pm-kisan"),
    ("mudra loan kitna milta hai", "pm-mudra"),
    ("How can I get a free LPG gas connection?", "pm-ujjwala"),
    ("I sell vegetables on a cart, can I get a loan?", "pm-svanidhi"),
    ("my crop was destroyed by flood, what insurance can help?", "pm-fasal-bima"),
    ("pension scheme for unorganised workers", "atal-pension"),
    ("savings account for my daughter", "sukanya-samriddhi"),
    ("100 days of work guarantee in village", "mgnrega"),
    ("गर्भवती महिला को कितना पैसा मिलता है?", "pmmvy"),
    ("किसान को फसल बीमा कैसे मिलेगा?", "pm-fasal-bima"),
    ("मनरेगा में कितने दिन का काम मिलता है?", "mgnrega"),
    ("लाडकी बहीण योजना में हर महीने कितने रुपये मिलते हैं?", "majhi-ladki-bahin-maharashtra"),
]
for q, doc in natural:
    r = ask(q)
    cited = [c["doc_id"] for c in r["citations"]]
    check(R2, f"natural question '{q}' -> {doc}", r["found"] and doc in cited, f"cited {cited}")

r = ask("What documents are required?", history=[{"role": "user", "content": "Tell me about Mudra loan"},
                                                 {"role": "assistant", "content": "..."}])
check(R2, "follow-up question keeps the earlier scheme", any(c["doc_id"] == "pm-mudra" for c in r["citations"]))

# ---------------------------------------------------------------- 3. Hindi and English answers
R3 = "3 Languages"
r = ask("Who is eligible for Atal Pension Yojana?")
check(R3, "English question -> English answer", r["lang"] == "en" and not is_hindi(r["answer"]))
r = ask("अटल पेंशन योजना के लिए उम्र क्या होनी चाहिए?")
check(R3, "Hindi question auto-detected", r["lang"] == "hi")
r = ask("Who is eligible for Atal Pension Yojana?", lang="hi")
check(R3, "Hindi toggle -> Hindi reply even for English question", r["lang"] == "hi")
if ai:
    for q in ["अटल पेंशन योजना के लिए उम्र क्या होनी चाहिए?", "आयुष्मान भारत में कितने का इलाज मुफ्त है?"]:
        r = ask(q)
        check(R3, f"AI writes the answer in Hindi: '{q[:30]}'", is_hindi(r["answer"].split("\n", 1)[-1]), r["answer"][:80])

# ---------------------------------------------------------------- 4. Cite every answer
R4 = "4 Citations"
for q in ["Am I eligible for PM-KISAN?", "How do I apply for Kisan Credit Card?", "पीएम स्वनिधि में कितना लोन मिलता है?",
          "What is the premium for PMSBY?", "Benefits of Central Sector Scholarship"]:
    r = ask(q)
    check(R4, f"'{q[:40]}' has at least one citation", r["found"] and len(r["citations"]) > 0)
    check(R4, f"'{q[:40]}' citations have title, section and quote",
          all(c["title"] and c["section"] and c["quote"] for c in r["citations"]))
    if ai:
        g = r.get("grounding") or {}
        check(R4, f"'{q[:40]}' every quote verified in source", g.get("total") and g["verified"] == g["total"], g)

# ---------------------------------------------------------------- 5. No guessing
R5 = "5 No guessing"
for q in ["What is the capital of France?", "Who won the cricket world cup?", "How do I make biryani?",
          "What is the share price of Reliance?", "भारत की राजधानी क्या है?", "आज मौसम कैसा है?",
          "Tell me a joke"]:
    r = ask(q)
    check(R5, f"off-topic '{q}' -> says not found", not r["found"] and not r["citations"], r["answer"][:60])
for q in ["What documents are required?", "कौन से दस्तावेज़ चाहिए?"]:
    r = ask(q)
    check(R5, f"'{q}' (no scheme named) -> asks which scheme", r.get("mode") == "clarify")
if ai:
    for q in ["What is the PM-KISAN helpline email address?", "How many people got Ujjwala connections in Bihar in 2023?"]:
        r = ask(q)
        check(R5, f"in-topic but not in documents '{q[:45]}' -> not found", not r["found"], r["answer"][:80])

# ---------------------------------------------------------------- 6. Eligibility questionnaire
R6 = "6 Eligibility"
base = {"has_bank_account": True, "income_tax_payer": False}
personas = {
    "pm-kisan": {"age": 40, "occupation": "farmer", "owns_land": True},
    "pm-fasal-bima": {"age": 40, "occupation": "farmer"},
    "kisan-credit-card": {"age": 40, "occupation": "farmer"},
    "ayushman-bharat-pmjay": {"age": 72},
    "pm-ujjwala": {"age": 30, "gender": "female", "category": "sc", "has_lpg": False},
    "pmay-urban": {"age": 35, "area": "urban", "income": 400000, "has_pucca_house": False},
    "sukanya-samriddhi": {"age": 30, "has_daughter_under_10": True},
    "atal-pension": {"age": 30},
    "pmjjby": {"age": 30},
    "pmsby": {"age": 65},
    "post-matric-scholarship-sc": {"age": 18, "occupation": "student", "category": "sc", "income": 200000},
    "central-sector-scholarship": {"age": 18, "occupation": "student", "class12_top20": True, "income": 300000},
    "pm-mudra": {"age": 30, "occupation": "business"},
    "pm-svanidhi": {"age": 30, "occupation": "street_vendor"},
    "pmmvy": {"age": 26, "gender": "female", "occupation": "homemaker", "pregnant_or_lactating": True, "income": 300000},
    "mgnrega": {"age": 30, "area": "rural"},
    "majhi-ladki-bahin-maharashtra": {"age": 30, "gender": "female", "state": "maharashtra", "income": 200000},
}
for sid, p in personas.items():
    res = {r["scheme_id"]: r["status"] for r in call("/api/eligibility", {**base, **p})["results"]}
    check(R6, f"{sid}: matching person -> eligible", res.get(sid) == "eligible", res.get(sid))
check(R6, "every scheme has an eligibility persona", set(personas) == {s["id"] for s in schemes})

negatives = [
    ("pm-kisan", {"age": 45, "occupation": "farmer", "owns_land": True, "income_tax_payer": True}, "income-tax payer"),
    ("pm-kisan", {"age": 45, "occupation": "govt_employee"}, "government employee"),
    ("atal-pension", {"age": 45, "has_bank_account": True}, "age 45 (limit 18-40)"),
    ("pmjjby", {"age": 55, "has_bank_account": True}, "age 55 (limit 18-50)"),
    ("pmay-urban", {"area": "urban", "income": 1200000}, "income 12 lakh (limit 9 lakh)"),
    ("pmay-urban", {"area": "urban", "income": 300000, "has_pucca_house": True}, "already owns pucca house"),
    ("post-matric-scholarship-sc", {"occupation": "student", "category": "general"}, "not SC"),
    ("central-sector-scholarship", {"occupation": "student", "class12_top20": True, "income": 600000}, "income 6 lakh (limit 4.5 lakh)"),
    ("majhi-ladki-bahin-maharashtra", {"gender": "female", "state": "bihar", "age": 30}, "not Maharashtra"),
    ("majhi-ladki-bahin-maharashtra", {"gender": "female", "state": "maharashtra", "age": 70}, "age 70 (limit 21-65)"),
    ("mgnrega", {"area": "urban", "age": 30}, "urban resident"),
    ("pm-ujjwala", {"gender": "male", "age": 30}, "male applicant"),
    ("pm-ujjwala", {"gender": "female", "age": 30, "has_lpg": True}, "already has LPG"),
]
for sid, p, why in negatives:
    res = {r["scheme_id"]: r["status"] for r in call("/api/eligibility", p)["results"]}
    check(R6, f"{sid}: {why} -> not eligible", res.get(sid) == "not_eligible", res.get(sid))

res = call("/api/eligibility", {})["results"]
check(R6, "empty form -> nothing marked eligible", all(r["status"] != "eligible" for r in res))
res = call("/api/eligibility", {"age": 30})["results"]
check(R6, "every result has a checklist in English and Hindi", all(c["en"] and c["hi"] for r in res for c in r["checks"]))
check(R6, "results link back to source document", all(r["source"].startswith("http") for r in res))

# ---------------------------------------------------------------- 7. Frontend served
R7 = "7 Web app"
for path in ["/", "/static/app.js", "/static/style.css"]:
    try:
        urllib.request.urlopen(BASE + path, timeout=10)
        check(R7, f"{path} loads", True)
    except Exception as e:
        check(R7, f"{path} loads", False, e)

# ---------------------------------------------------------------- summary
print("\n" + "-" * 58)
print(f"{'Requirement':<22}{'Passed':>8}{'Failed':>8}")
print("-" * 58)
tp = tf = 0
for req, (p, f, _) in results.items():
    print(f"{req:<22}{p:>8}{f:>8}")
    tp, tf = tp + p, tf + f
print("-" * 58)
print(f"{'TOTAL':<22}{tp:>8}{tf:>8}")
if not ai:
    print("\nNote: add ANTHROPIC_API_KEY to .env and rerun to also test AI answers, Hindi generation and quote verification.")
sys.exit(1 if tf else 0)
