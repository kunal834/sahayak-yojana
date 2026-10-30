"""Rule-based eligibility engine. Every rule is written from the matching scheme document,
so a recommendation can always be traced back to its source."""
from dataclasses import dataclass
from typing import Callable


@dataclass
class Rule:
    en: str
    hi: str
    test: Callable[[dict], bool | None]  # None = cannot decide from the answers given


@dataclass
class Scheme:
    id: str
    rules: list[Rule]


def _age(lo=None, hi=None):
    def t(p):
        a = p.get("age")
        if a is None:
            return None
        return (lo is None or a >= lo) and (hi is None or a <= hi)
    return t


def _income_max(limit):
    def t(p):
        inc = p.get("income")
        return None if inc is None else inc <= limit
    return t


def _flag(name, expected=True):
    def t(p):
        v = p.get(name)
        return None if v is None else v == expected
    return t


def _in(name, allowed):
    def t(p):
        v = p.get(name)
        return None if not v else v in allowed
    return t


def _not_govt_employee(p):
    occ = p.get("occupation")
    return None if not occ else occ != "govt_employee"


def _pmjay(p):
    # SECC 2011 listing can't be derived from a questionnaire, so below 70 the best answer is "maybe".
    if p.get("age") is not None and p["age"] >= 70:
        return True
    if p.get("income") is not None and p["income"] > 500000 and p.get("category") not in {"sc", "st"}:
        return False
    return None


def _ujjwala_poor(p):
    if p.get("category") in {"sc", "st"}:
        return True
    inc = p.get("income")
    if inc is None:
        return None
    if inc <= 200000:
        return True
    return False if inc > 500000 else None


SCHEMES: list[Scheme] = [
    Scheme("pm-kisan", [
        Rule("Is a farmer", "किसान हों", _in("occupation", {"farmer"})),
        Rule("Owns cultivable land in own name", "अपने नाम पर खेती योग्य ज़मीन हो", _flag("owns_land")),
        Rule("Did not pay income tax last year", "पिछले वर्ष आयकर नहीं भरा हो", _flag("income_tax_payer", False)),
        Rule("Not a government employee", "सरकारी कर्मचारी न हों", _not_govt_employee),
    ]),
    Scheme("pm-fasal-bima", [
        Rule("Is a farmer (owner, tenant or sharecropper)", "किसान हों (मालिक, किरायेदार या बटाईदार)", _in("occupation", {"farmer"})),
    ]),
    Scheme("kisan-credit-card", [
        Rule("Is a farmer / animal husbandry / fisheries worker", "किसान / पशुपालक / मछुआरे हों", _in("occupation", {"farmer"})),
        Rule("Age 18 or above", "उम्र 18 या अधिक", _age(18)),
    ]),
    Scheme("ayushman-bharat-pmjay", [
        Rule("Aged 70+ (any income), or a family listed in SECC 2011 (verify on beneficiary.nha.gov.in)",
             "70+ आयु (किसी भी आय पर), या SECC 2011 सूची में शामिल परिवार (beneficiary.nha.gov.in पर जाँचें)",
             _pmjay),
    ]),
    Scheme("pm-ujjwala", [
        Rule("Woman aged 18+", "18+ आयु की महिला", lambda p: None if p.get("gender") is None or p.get("age") is None
             else p["gender"] == "female" and p["age"] >= 18),
        Rule("No LPG connection in household", "घर में कोई LPG कनेक्शन न हो", _flag("has_lpg", False)),
        Rule("Poor household (SC/ST, BPL or low income)", "गरीब परिवार (SC/ST, BPL या कम आय)", _ujjwala_poor),
    ]),
    Scheme("pmay-urban", [
        Rule("Lives in an urban area", "शहरी क्षेत्र में रहते हों", _in("area", {"urban"})),
        Rule("Annual family income up to Rs 9 lakh", "पारिवारिक वार्षिक आय 9 लाख रुपये तक", _income_max(900000)),
        Rule("Family does not own a pucca house", "परिवार के पास पक्का मकान न हो", _flag("has_pucca_house", False)),
    ]),
    Scheme("sukanya-samriddhi", [
        Rule("Has a daughter below 10 years", "10 वर्ष से कम उम्र की बेटी हो", _flag("has_daughter_under_10")),
    ]),
    Scheme("atal-pension", [
        Rule("Age between 18 and 40", "उम्र 18 से 40 वर्ष के बीच", _age(18, 40)),
        Rule("Has a bank / post office account", "बैंक / डाकघर खाता हो", _flag("has_bank_account")),
        Rule("Not an income-tax payer", "आयकरदाता न हों", _flag("income_tax_payer", False)),
    ]),
    Scheme("pmjjby", [
        Rule("Age between 18 and 50", "उम्र 18 से 50 वर्ष के बीच", _age(18, 50)),
        Rule("Has a bank / post office account", "बैंक / डाकघर खाता हो", _flag("has_bank_account")),
    ]),
    Scheme("pmsby", [
        Rule("Age between 18 and 70", "उम्र 18 से 70 वर्ष के बीच", _age(18, 70)),
        Rule("Has a bank / post office account", "बैंक / डाकघर खाता हो", _flag("has_bank_account")),
    ]),
    Scheme("post-matric-scholarship-sc", [
        Rule("Is a student (Class 11 or above)", "छात्र हों (कक्षा 11 या ऊपर)", _in("occupation", {"student"})),
        Rule("Belongs to Scheduled Caste", "अनुसूचित जाति से हों", _in("category", {"sc"})),
        Rule("Parents' income up to Rs 2.5 lakh", "माता-पिता की आय 2.5 लाख रुपये तक", _income_max(250000)),
    ]),
    Scheme("central-sector-scholarship", [
        Rule("Is a college / university student", "कॉलेज / विश्वविद्यालय के छात्र हों", _in("occupation", {"student"})),
        Rule("Above 80th percentile in Class 12", "कक्षा 12 में 80 पर्सेंटाइल से ऊपर", _flag("class12_top20")),
        Rule("Family income up to Rs 4.5 lakh", "पारिवारिक आय 4.5 लाख रुपये तक", _income_max(450000)),
    ]),
    Scheme("pm-mudra", [
        Rule("Runs or plans a small non-farm business", "छोटा गैर-कृषि व्यवसाय चलाते / शुरू करना चाहते हों",
             _in("occupation", {"business", "street_vendor"})),
        Rule("Age 18 or above", "उम्र 18 या अधिक", _age(18)),
    ]),
    Scheme("pm-svanidhi", [
        Rule("Is a street vendor", "रेहड़ी-पटरी विक्रेता हों", _in("occupation", {"street_vendor"})),
    ]),
    Scheme("pmmvy", [
        Rule("Pregnant woman or lactating mother", "गर्भवती महिला या स्तनपान कराने वाली माँ", _flag("pregnant_or_lactating")),
        Rule("Not in regular government / PSU employment", "सरकारी / PSU में नियमित नौकरी न हो", _not_govt_employee),
        Rule("Family income below Rs 8 lakh (or SC/ST)", "पारिवारिक आय 8 लाख से कम (या SC/ST)",
             lambda p: True if p.get("category") in {"sc", "st"} else (None if p.get("income") is None else p["income"] < 800000)),
    ]),
    Scheme("mgnrega", [
        Rule("Lives in a rural area", "ग्रामीण क्षेत्र में रहते हों", _in("area", {"rural"})),
        Rule("Age 18 or above", "उम्र 18 या अधिक", _age(18)),
    ]),
    Scheme("majhi-ladki-bahin-maharashtra", [
        Rule("Woman resident of Maharashtra", "महाराष्ट्र की निवासी महिला",
             lambda p: None if not p.get("gender") or not p.get("state") else p["gender"] == "female" and p["state"] == "maharashtra"),
        Rule("Age between 21 and 65", "उम्र 21 से 65 वर्ष के बीच", _age(21, 65)),
        Rule("Family income up to Rs 2.5 lakh", "पारिवारिक आय 2.5 लाख रुपये तक", _income_max(250000)),
        Rule("No income-tax payer in family", "परिवार में कोई आयकरदाता न हो", _flag("income_tax_payer", False)),
    ]),
]


def evaluate(profile: dict) -> list[dict]:
    results = []
    for scheme in SCHEMES:
        checks = []
        for r in scheme.rules:
            outcome = r.test(profile)
            checks.append({"en": r.en, "hi": r.hi, "result": outcome})
        outcomes = [c["result"] for c in checks]
        if any(o is False for o in outcomes):
            status = "not_eligible"
        elif all(o is True for o in outcomes):
            status = "eligible"
        else:
            status = "maybe"
        results.append({"scheme_id": scheme.id, "status": status, "checks": checks})
    order = {"eligible": 0, "maybe": 1, "not_eligible": 2}
    results.sort(key=lambda r: order[r["status"]])
    return results
