"""Document loading, chunking and BM25 retrieval with Hindi / Hinglish query expansion."""
import math
import re
import unicodedata
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "schemes"

TOKEN_RE = re.compile(r"[a-z0-9ऀ-ॿ]+")

STOPWORDS = {
    "a", "an", "the", "and", "or", "of", "to", "in", "on", "for", "is", "are", "be", "by", "with",
    "as", "at", "from", "this", "that", "it", "its", "i", "me", "my", "we", "our", "you", "your",
    "can", "do", "does", "what", "which", "who", "how", "under", "any", "all", "will", "should",
    "am", "was", "were", "has", "have", "if", "not", "no", "per", "up", "than", "into", "their",
    "there", "these", "those", "also", "get", "about", "tell", "please", "scheme", "yojana",
    "क्या", "है", "हैं", "मैं", "मुझे", "के", "की", "का", "को", "में", "से", "और", "लिए", "कि",
    "यह", "वह", "हो", "कर", "करें", "तो", "भी", "पर", "एक", "योजना", "बताइए", "बताओ", "बताएं",
    "kya", "hai", "hain", "main", "mujhe", "ke", "ki", "ka", "ko", "me", "mein", "se", "aur", "liye",
}

# Hindi / Hinglish words -> English retrieval terms. Lets Hindi questions hit English documents
# even when no LLM is configured.
GLOSSARY = {
    "पात्र": "eligible eligibility", "पात्रता": "eligible eligibility", "योग्य": "eligible eligibility",
    "patra": "eligible eligibility", "eligible": "eligible eligibility",
    "दस्तावेज": "documents required", "दस्तावेज़": "documents required", "कागज": "documents required",
    "कागजात": "documents required", "कागज़ात": "documents required", "प्रमाण": "proof certificate",
    "dastavej": "documents required", "kagaz": "documents required", "kagzat": "documents required",
    "आवेदन": "apply application", "अप्लाई": "apply", "aavedan": "apply application", "apply": "apply",
    "लाभ": "benefits", "फायदा": "benefits", "फ़ायदा": "benefits", "labh": "benefits", "fayda": "benefits",
    "पैसा": "amount rs benefits", "पैसे": "amount rs benefits", "राशि": "amount rs benefits",
    "मिलता": "benefits", "मिलेगा": "benefits", "मिलती": "benefits", "रुपये": "rs amount", "किस्त": "instalment",
    "किसान": "farmer farmers", "kisan": "farmer farmers", "खेती": "agriculture cultivation crop",
    "फसल": "crop", "fasal": "crop", "बीमा": "insurance", "bima": "insurance", "जमीन": "land",
    "ज़मीन": "land", "zameen": "land", "jameen": "land",
    "छात्र": "student students", "छात्रा": "student girl", "छात्रवृत्ति": "scholarship",
    "scholarship": "scholarship", "पढ़ाई": "education study", "कॉलेज": "college",
    "स्वास्थ्य": "health hospitalisation", "इलाज": "treatment hospitalisation", "अस्पताल": "hospital",
    "बुजुर्ग": "senior citizens", "वरिष्ठ": "senior citizens",
    "महिला": "women woman", "महिलाओं": "women", "mahila": "women", "बेटी": "girl child daughter",
    "बच्ची": "girl child", "लड़की": "girl", "गर्भवती": "pregnant women", "मां": "mother", "माँ": "mother",
    "गैस": "lpg gas connection", "सिलेंडर": "lpg refill", "घर": "house housing", "मकान": "house housing",
    "आवास": "housing house", "पेंशन": "pension", "pension": "pension", "ऋण": "loan", "लोन": "loan",
    "कर्ज": "loan credit", "कर्ज़": "loan credit", "loan": "loan", "ब्याज": "interest",
    "व्यापार": "business enterprise", "व्यवसाय": "business enterprise", "धंधा": "business",
    "रेहड़ी": "street vendor", "ठेला": "street vendor", "फेरीवाला": "street vendor", "विक्रेता": "vendor",
    "रोजगार": "employment work", "रोज़गार": "employment work", "काम": "work", "मजदूरी": "wage",
    "मज़दूरी": "wage", "नौकरी": "employment", "ग्रामीण": "rural", "शहरी": "urban",
    "आय": "income", "आमदनी": "income", "income": "income", "उम्र": "age", "आयु": "age", "umar": "age",
    "आधार": "aadhaar", "बैंक": "bank account", "खाता": "account", "राशन": "ration card",
    "कार्ड": "card", "जाति": "caste certificate", "प्रीमियम": "premium", "दुर्घटना": "accident",
    "मृत्यु": "death", "जीवन": "life", "बचत": "savings deposit", "जमा": "deposit",
    "हेल्पलाइन": "helpline", "कैसे": "how apply", "चाहिए": "required",
    "daughter": "girl child", "daughters": "girl child", "cart": "street vendor vending",
    "hawker": "street vendor vending", "thela": "street vendor", "rehri": "street vendor",
    "kitna": "amount rs", "kitni": "amount rs", "milta": "benefits", "milega": "benefits",
    "kaise": "how apply", "chahiye": "required", "kaun": "eligible", "kagaj": "documents required",
}

# Phrases that identify a specific scheme -> doc id. Used for boosting and for follow-up questions.
SCHEME_ALIASES = {
    "pm-kisan": ["pm kisan", "pm-kisan", "kisan samman", "samman nidhi", "पीएम किसान", "पीएम-किसान", "किसान सम्मान", "सम्मान निधि"],
    "ayushman-bharat-pmjay": ["ayushman", "pmjay", "pm-jay", "jan arogya", "आयुष्मान", "जन आरोग्य", "vay vandana"],
    "pm-ujjwala": ["ujjwala", "pmuy", "उज्ज्वला", "उज्जवला"],
    "pmay-urban": ["awas", "pmay", "आवास योजना", "प्रधानमंत्री आवास", "housing scheme"],
    "sukanya-samriddhi": ["sukanya", "ssy", "सुकन्या"],
    "atal-pension": ["atal pension", "apy", "अटल पेंशन", "अटल"],
    "pmjjby": ["jeevan jyoti", "pmjjby", "जीवन ज्योति", "life insurance"],
    "pmsby": ["suraksha bima", "pmsby", "सुरक्षा बीमा", "accident insurance"],
    "pm-fasal-bima": ["fasal bima", "pmfby", "crop insurance", "फसल बीमा"],
    "kisan-credit-card": ["kisan credit", "kcc", "किसान क्रेडिट", "क्रेडिट कार्ड"],
    "post-matric-scholarship-sc": ["post matric", "post-matric", "पोस्ट मैट्रिक", "sc scholarship"],
    "central-sector-scholarship": ["central sector", "csss", "केंद्रीय क्षेत्र", "merit scholarship"],
    "pm-mudra": ["mudra", "मुद्रा", "shishu", "kishore", "tarun"],
    "pm-svanidhi": ["svanidhi", "swanidhi", "स्वनिधि", "street vendor"],
    "pmmvy": ["matru vandana", "pmmvy", "मातृ वंदना", "maternity", "pregnan", "गर्भवती", "garbhvati"],
    "mgnrega": ["mgnrega", "nrega", "manrega", "मनरेगा", "नरेगा", "job card", "जॉब कार्ड"],
    "majhi-ladki-bahin-maharashtra": ["ladki bahin", "ladli behna", "लाडकी बहीण", "लाडकी बहिन", "लाडली बहना", "majhi ladki"],
}


def _nfc(text: str) -> str:
    # Precomposed nukta letters (e.g. U+095B ज़) decompose under NFC, so both spellings match.
    # Digit-group commas are dropped so "Rs 6,000" and "Rs 6000" become the same token.
    return re.sub(r"(?<=\d),(?=\d)", "", unicodedata.normalize("NFC", text))


def _stem(tok: str) -> str:
    if tok.isascii() and len(tok) > 3 and tok.endswith("s") and not tok.endswith("ss"):
        return tok[:-1]
    return tok


def tokenize(text: str) -> list[str]:
    return [_stem(t) for t in TOKEN_RE.findall(_nfc(text).lower()) if t not in STOPWORDS]


GLOSSARY = {_nfc(k): v for k, v in GLOSSARY.items()}


def has_devanagari(text: str) -> bool:
    return any("ऀ" <= ch <= "ॿ" for ch in text)


def expand_query(query: str) -> list[str]:
    raw = [t for t in TOKEN_RE.findall(_nfc(query).lower()) if t not in STOPWORDS]
    expanded = [_stem(t) for t in raw]
    for tok in raw:
        if tok in GLOSSARY:
            expanded.extend(tokenize(GLOSSARY[tok]))
    return expanded


GENERIC_TERMS = {"document", "required", "eligible", "eligibility", "apply", "application", "benefit",
                 "amount", "rs", "how", "need", "needed", "require", "proof", "certificate", "instalment",
                 "कौन", "चाहिए", "दस्तावेज़", "दस्तावेज", "कागज", "कागजात", "पात्र", "पात्रता", "लाभ", "आवेदन",
                 "कैसे", "कितना", "मिलता", "मिलेगा", "kaun", "chahiye", "kitna", "kaise", "milta"}


def is_generic(query: str) -> bool:
    """True when the question names no topic at all, e.g. "What documents are required?"."""
    tokens = [t for t in TOKEN_RE.findall(_nfc(query).lower()) if t not in STOPWORDS]
    return bool(tokens) and all(_stem(t) in GENERIC_TERMS or t in GENERIC_TERMS for t in tokens)


def detect_schemes(text: str) -> list[str]:
    low = _nfc(text).lower()
    return [doc_id for doc_id, aliases in SCHEME_ALIASES.items() if any(_nfc(a) in low for a in aliases)]


@dataclass
class Doc:
    id: str
    title: str
    title_hi: str
    category: str
    source: str
    body: str


@dataclass
class Chunk:
    id: str
    doc_id: str
    section: str
    text: str
    tokens: list[str] = field(default_factory=list)


def _parse_doc(path: Path) -> Doc:
    raw = path.read_text(encoding="utf-8")
    meta, body = {}, raw
    if raw.startswith("---"):
        _, header, body = raw.split("---", 2)
        for line in header.strip().splitlines():
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
    return Doc(
        id=meta.get("id", path.stem),
        title=meta.get("title", path.stem),
        title_hi=meta.get("title_hi", ""),
        category=meta.get("category", "other"),
        source=meta.get("source", ""),
        body=body.strip(),
    )


def _parse_pdf(path: Path) -> Doc:
    from pypdf import PdfReader

    text = "\n".join(page.extract_text() or "" for page in PdfReader(str(path)).pages)
    return Doc(id=path.stem, title=path.stem.replace("-", " ").title(), title_hi="",
               category="other", source=path.name, body=text)


def _chunk_doc(doc: Doc, max_chars: int = 900) -> list[Chunk]:
    sections = re.split(r"^## +", doc.body, flags=re.M)
    chunks = []
    for sec in sections:
        sec = sec.strip()
        if not sec:
            continue
        heading, _, content = sec.partition("\n")
        if not content.strip():
            heading, content = "Text", sec
        paras = [p.strip() for p in content.split("\n\n") if p.strip()]
        buf, part = "", 0
        for para in paras + [None]:
            if para is None or (buf and len(buf) + len(para) > max_chars):
                if buf:
                    slug = re.sub(r"[^a-z0-9]+", "-", heading.lower()).strip("-") or "text"
                    cid = f"{doc.id}#{slug}" + (f"-{part}" if part else "")
                    chunks.append(Chunk(cid, doc.id, heading.strip(), buf.strip()))
                    part += 1
                buf = ""
            if para is not None:
                buf += para + "\n\n"
    return chunks


class Index:
    def __init__(self, data_dir: Path = DATA_DIR):
        self.docs: dict[str, Doc] = {}
        self.chunks: list[Chunk] = []
        for path in sorted(data_dir.iterdir()):
            if path.suffix in (".md", ".txt"):
                doc = _parse_doc(path)
            elif path.suffix == ".pdf":
                doc = _parse_pdf(path)
            else:
                continue
            self.docs[doc.id] = doc
            self.chunks.extend(_chunk_doc(doc))
        for ch in self.chunks:
            doc = self.docs[ch.doc_id]
            # Title and section heading are indexed with the passage so "PM-KISAN documents" matches.
            ch.tokens = tokenize(f"{doc.title} {doc.title_hi} {ch.section} {ch.section} {ch.text}")
        self.df = Counter(t for ch in self.chunks for t in set(ch.tokens))
        self.avgdl = sum(len(c.tokens) for c in self.chunks) / max(len(self.chunks), 1)

    def _bm25(self, q_tokens: list[str], chunk: Chunk, k1: float = 1.5, b: float = 0.75) -> float:
        tf = Counter(chunk.tokens)
        n = len(self.chunks)
        score = 0.0
        for t in q_tokens:
            if t not in tf:
                continue
            idf = math.log(1 + (n - self.df[t] + 0.5) / (self.df[t] + 0.5))
            score += idf * tf[t] * (k1 + 1) / (tf[t] + k1 * (1 - b + b * len(chunk.tokens) / self.avgdl))
        return score

    def search(self, query: str, k: int = 6, focus_schemes: list[str] | None = None) -> list[tuple[Chunk, float]]:
        q_tokens = expand_query(query)
        q_set = set(q_tokens)
        named = detect_schemes(query)
        focus = set(named or focus_schemes or [])
        scored = []
        for ch in self.chunks:
            s = self._bm25(q_tokens, ch)
            if s > 0:
                # Intent match: "documents" questions should land on the "Documents Required" section.
                s += 4.0 * len(q_set & set(tokenize(ch.section)))
            if ch.doc_id in focus:
                s = s * 1.5 + 8.0
            scored.append((ch, s))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [(c, s) for c, s in scored[:k] if s > 0]
