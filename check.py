"""Self-check for Yojana Sahayak. Start the server first, then run:  python check.py"""
import json
import sys
import urllib.request

BASE = "http://localhost:8000"
passed = failed = 0


def call(path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data, {"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=120))


def check(name, ok, detail=""):
    global passed, failed
    passed += ok
    failed += not ok
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"   ({detail})" if detail and not ok else ""))


def ask(message, history=None, lang=None):
    return call("/api/chat", {"message": message, "history": history or [], "lang": lang})


try:
    status = call("/api/status")
except Exception as e:
    sys.exit(f"Server not reachable at {BASE} - start it first ({e})")

print(f"\nMode: {'AI (' + status['model'] + ')' if status['llm'] else 'OFFLINE - no API key, answers are document extracts'}")
print(f"Documents: {status['documents']}, passages: {status['chunks']}\n")

print("1. Documents loaded")
check("10-20 scheme documents", 10 <= status["documents"] <= 20, status["documents"])

print("2. Answers cite the right scheme")
cases = [
    ("Am I eligible for PM-KISAN?", "pm-kisan"),
    ("What documents do I need for Ayushman Bharat?", "ayushman-bharat-pmjay"),
    ("How do I apply for Mudra loan?", "pm-mudra"),
    ("पीएम किसान के लिए कौन से दस्तावेज़ चाहिए?", "pm-kisan"),
    ("गर्भवती महिला को कितना पैसा मिलता है?", "pmmvy"),
    ("सुकन्या योजना में कितना जमा कर सकते हैं?", "sukanya-samriddhi"),
]
for q, doc in cases:
    r = ask(q)
    cited = {c["doc_id"] for c in r["citations"]}
    check(f"{q}  ->  {doc}", r["found"] and doc in cited, f"cited {cited or 'nothing'}")

print("3. Hindi questions get Hindi answers")
r = ask("अटल पेंशन योजना के लिए उम्र क्या होनी चाहिए?")
check("answer language is Hindi", r["lang"] == "hi" and any("ऀ" <= ch <= "ॿ" for ch in r["answer"]))

print("4. No guessing")
for q in ["What is the capital of France?", "Who won the cricket world cup?", "भारत की राजधानी क्या है?"]:
    r = ask(q)
    check(f"'{q}' -> not found", not r["found"] and not r["citations"])
r = ask("What documents are required?")
check("question without a scheme -> asks which scheme", r.get("mode") == "clarify")

print("5. Follow-up keeps context")
r = ask("What documents are required?", history=[{"role": "user", "content": "Tell me about Mudra loan"},
                                                 {"role": "assistant", "content": "..."}])
check("follow-up answered about Mudra", any(c["doc_id"] == "pm-mudra" for c in r["citations"]))

if status["llm"]:
    print("6. AI answers are grounded (hallucination check)")
    r = ask("Am I eligible for PM-KISAN if I pay income tax?")
    g = r.get("grounding") or {}
    check("quotes verified against source", g.get("total", 0) > 0 and g.get("verified") == g.get("total"), g)
    check("AI mode used (not offline fallback)", r["mode"] == "llm", r.get("error", r["mode"]))

print("7. Eligibility questionnaire")
res = {r["scheme_id"]: r["status"] for r in call("/api/eligibility", {
    "age": 34, "gender": "female", "income": 180000, "occupation": "farmer", "state": "maharashtra",
    "area": "rural", "owns_land": True, "income_tax_payer": False, "has_bank_account": True})["results"]}
check("woman farmer -> PM-KISAN eligible", res["pm-kisan"] == "eligible")
check("woman farmer, Maharashtra -> Ladki Bahin eligible", res["majhi-ladki-bahin-maharashtra"] == "eligible")
check("woman farmer -> not eligible for street-vendor loan", res["pm-svanidhi"] == "not_eligible")
res = {r["scheme_id"]: r["status"] for r in call("/api/eligibility", {
    "age": 45, "occupation": "farmer", "owns_land": True, "income_tax_payer": True})["results"]}
check("income-tax payer -> PM-KISAN not eligible", res["pm-kisan"] == "not_eligible")
check("blank answers give 'maybe', not 'eligible'", call("/api/eligibility", {})["results"][0]["status"] != "eligible")

print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
