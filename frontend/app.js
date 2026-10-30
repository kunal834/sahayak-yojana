const I18N = {
  en: {
    title: "Yojana Sahayak", tabChat: "Ask", tabElig: "Eligibility", tabDocs: "Schemes",
    placeholder: "Ask about any scheme…", connecting: "connecting…",
    statusLLM: (n) => `AI · answers from ${n} official documents`,
    statusOffline: (n) => `Offline mode · ${n} documents`,
    welcomeTitle: "Namaste 🙏",
    welcomeBody: "Ask who can get a government scheme, which documents you need, or how to apply. Every answer shows the official document it comes from.",
    suggestions: [
      ["Farmers", "Am I eligible for PM-KISAN?"],
      ["Health", "What documents do I need for Ayushman Bharat?"],
      ["Business", "I am a 25 year old street vendor. Which loan can I get?"],
      ["Savings", "How much can I deposit in Sukanya Samriddhi?"],
    ],
    chips: ["How do I apply?", "What documents are needed?", "How much money will I get?", "What is the capital of France?"],
    sources: "Sources",
    verified: (v, t) => `${v}/${t} quotes verified`,
    unverified: (v, t) => `Only ${v}/${t} verified — check source`,
    notFound: "Not in documents", offline: "Document extract", clarify: "Need more detail",
    eligTitle: "Find schemes for you",
    eligIntro: "Answer what you can. Leave anything you're unsure about blank.",
    aboutYou: "About you", quickQs: "Quick questions",
    age: "Age", gender: "Gender", female: "Female", male: "Male", other: "Other",
    income: "Annual family income (₹)", occupation: "Occupation", state: "State", area: "Area",
    rural: "Rural", urban: "Urban", category: "Social category",
    occ_farmer: "Farmer", occ_student: "Student", occ_vendor: "Street vendor", occ_business: "Small business owner",
    occ_worker: "Daily wage worker", occ_private: "Private job", occ_govt: "Government employee",
    occ_home: "Homemaker", occ_unemp: "Unemployed",
    findSchemes: "Find my schemes", yes: "Yes", no: "No",
    flags: {
      owns_land: "Own farmland in your name?", has_bank_account: "Have a bank or post office account?",
      income_tax_payer: "Anyone in family pays income tax?", has_pucca_house: "Family owns a pucca house?",
      has_lpg: "Household already has LPG gas?", has_daughter_under_10: "Have a daughter under 10?",
      pregnant_or_lactating: "Pregnant or a new mother?", class12_top20: "Top 20% in Class 12 exams?",
    },
    eligible: "Eligible", maybe: "Maybe", not_eligible: "Not eligible",
    statEligible: "likely eligible", statMaybe: "need more detail", statNot: "not eligible",
    others: (n) => `${n} schemes you don't qualify for`,
    ask: "Ask about this", view: "Read document",
    askTpl: (t) => `Am I eligible for ${t} and what documents do I need?`,
    docsTitle: "Scheme library", docsIntro: "Every answer comes only from these public documents.",
    source: "Official source", error: "Something went wrong. Please try again.",
    voiceUnsupported: "Voice input works in Chrome or Edge.",
  },
  hi: {
    title: "योजना सहायक", tabChat: "पूछें", tabElig: "पात्रता", tabDocs: "योजनाएँ",
    placeholder: "किसी भी योजना के बारे में पूछें…", connecting: "जुड़ रहा है…",
    statusLLM: (n) => `AI · ${n} आधिकारिक दस्तावेज़ों से उत्तर`,
    statusOffline: (n) => `ऑफ़लाइन मोड · ${n} दस्तावेज़`,
    welcomeTitle: "नमस्ते 🙏",
    welcomeBody: "पूछें कि किसी सरकारी योजना का लाभ कौन ले सकता है, कौन से दस्तावेज़ चाहिए या आवेदन कैसे करें। हर उत्तर के साथ उसका आधिकारिक दस्तावेज़ दिखाया जाता है।",
    suggestions: [
      ["किसान", "क्या मैं पीएम किसान योजना के लिए पात्र हूँ?"],
      ["स्वास्थ्य", "आयुष्मान भारत के लिए कौन से दस्तावेज़ चाहिए?"],
      ["पेंशन", "मेरी उम्र 30 है, क्या मैं अटल पेंशन ले सकता हूँ?"],
      ["महिला", "गर्भवती महिला को कितना पैसा मिलता है?"],
    ],
    chips: ["आवेदन कैसे करें?", "कौन से दस्तावेज़ चाहिए?", "कितना पैसा मिलेगा?", "भारत की राजधानी क्या है?"],
    sources: "स्रोत",
    verified: (v, t) => `${v}/${t} उद्धरण सत्यापित`,
    unverified: (v, t) => `केवल ${v}/${t} सत्यापित — स्रोत देखें`,
    notFound: "दस्तावेज़ों में नहीं", offline: "दस्तावेज़ का अंश", clarify: "और जानकारी चाहिए",
    eligTitle: "आपके लिए योजनाएँ खोजें",
    eligIntro: "जितना जानते हैं उतना भरें। जिसके बारे में पक्का न हों, उसे खाली छोड़ दें।",
    aboutYou: "आपके बारे में", quickQs: "छोटे सवाल",
    age: "उम्र", gender: "लिंग", female: "महिला", male: "पुरुष", other: "अन्य",
    income: "परिवार की वार्षिक आय (₹)", occupation: "व्यवसाय", state: "राज्य", area: "क्षेत्र",
    rural: "ग्रामीण", urban: "शहरी", category: "सामाजिक वर्ग",
    occ_farmer: "किसान", occ_student: "छात्र", occ_vendor: "रेहड़ी-पटरी विक्रेता", occ_business: "छोटा व्यवसायी",
    occ_worker: "दिहाड़ी मज़दूर", occ_private: "प्राइवेट नौकरी", occ_govt: "सरकारी कर्मचारी",
    occ_home: "गृहिणी", occ_unemp: "बेरोज़गार",
    findSchemes: "मेरी योजनाएँ खोजें", yes: "हाँ", no: "नहीं",
    flags: {
      owns_land: "क्या आपके नाम पर खेती की ज़मीन है?", has_bank_account: "क्या बैंक या डाकघर खाता है?",
      income_tax_payer: "क्या परिवार में कोई आयकर भरता है?", has_pucca_house: "क्या परिवार के पास पक्का मकान है?",
      has_lpg: "क्या घर में पहले से LPG गैस है?", has_daughter_under_10: "क्या 10 साल से कम उम्र की बेटी है?",
      pregnant_or_lactating: "क्या आप गर्भवती हैं या नई माँ हैं?", class12_top20: "कक्षा 12 में शीर्ष 20% में आए?",
    },
    eligible: "पात्र", maybe: "शायद", not_eligible: "पात्र नहीं",
    statEligible: "संभवतः पात्र", statMaybe: "और जानकारी चाहिए", statNot: "पात्र नहीं",
    others: (n) => `${n} योजनाएँ जिनके लिए आप पात्र नहीं हैं`,
    ask: "इसके बारे में पूछें", view: "दस्तावेज़ पढ़ें",
    askTpl: (t) => `क्या मैं ${t} के लिए पात्र हूँ और कौन से दस्तावेज़ चाहिए?`,
    docsTitle: "योजना पुस्तकालय", docsIntro: "हर उत्तर केवल इन सार्वजनिक दस्तावेज़ों से आता है।",
    source: "आधिकारिक स्रोत", error: "कुछ गड़बड़ हुई। कृपया फिर से कोशिश करें।",
    voiceUnsupported: "आवाज़ इनपुट Chrome या Edge में काम करता है।",
  },
};

const ICON = {
  check: '<svg viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>',
  cross: '<svg viewBox="0 0 24 24"><path d="M7 7l10 10M17 7L7 17"/></svg>',
  help: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .8-1 1.5v.4M12 17h.01"/></svg>',
  shield: '<svg viewBox="0 0 24 24"><path d="M12 3l8 3v6c0 4.5-3.4 8.3-8 9-4.6-.7-8-4.5-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/></svg>',
  alert: '<svg viewBox="0 0 24 24"><path d="M12 3l9.5 17h-19z"/><path d="M12 10v4M12 17h.01"/></svg>',
  info: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/></svg>',
  speaker: '<svg viewBox="0 0 24 24"><path d="M4 10v4h4l5 4V6L8 10z"/><path d="M16.5 9a4 4 0 0 1 0 6M19 6.5a8 8 0 0 1 0 11"/></svg>',
  chat: '<svg viewBox="0 0 24 24"><path d="M4 5h16v11H8l-4 4z"/></svg>',
  doc: '<svg viewBox="0 0 24 24"><path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4"/></svg>',
};

const CATEGORY_COLOR = {
  agriculture: "#3f9a4f", health: "#d0574a", education: "#3b7bd4", "women-child": "#c4569a",
  business: "#d88a2c", housing: "#7a62c9", welfare: "#2c9a9a", savings: "#5c8a3a",
  pension: "#8a6d3b", insurance: "#5a6fbf", employment: "#b0703a",
};

let lang = "en";
let status = null;
let schemes = [];
const history = [];
const flagState = {};
let lastEligibility = null;
const t = (k) => I18N[lang][k];
const $ = (s) => document.querySelector(s);

function esc(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

function renderMarkdown(text) {
  let html = "", inList = false;
  for (const raw of esc(text).split("\n")) {
    const line = raw.replace(/\*\*(.+?)\*\*/g, "<b>$1</b>");
    const m = line.match(/^\s*[-*•]\s+(.*)/);
    if (m) {
      if (!inList) { html += "<ul>"; inList = true; }
      html += `<li>${m[1]}</li>`;
    } else {
      if (inList) { html += "</ul>"; inList = false; }
      if (line.trim()) html += `<p>${line}</p>`;
    }
  }
  return html + (inList ? "</ul>" : "");
}

const schemeTitle = (s) => (lang === "hi" && s.title_hi ? s.title_hi : s.title);
const now = () => new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

/* ---------- language ---------- */
function applyLang() {
  document.documentElement.lang = lang;
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const v = I18N[lang][el.dataset.i18n];
    if (typeof v === "string") el.textContent = v;
  });
  document.querySelectorAll("[data-i18n-ph]").forEach((el) => (el.placeholder = t(el.dataset.i18nPh)));
  document.querySelectorAll(".seg-toggle button").forEach((b) => b.classList.toggle("active", b.dataset.lang === lang));
  renderStatus();
  renderChips();
  renderFlags();
  renderDocs();
  renderEligibility();
  if (!history.length) renderWelcome();
}
document.querySelectorAll(".seg-toggle button").forEach((b) =>
  b.addEventListener("click", () => { lang = b.dataset.lang; applyLang(); }));

function renderStatus() {
  if (!status) return;
  $("#status").textContent = status.llm ? t("statusLLM")(status.documents) : t("statusOffline")(status.documents);
  $("#status-dot").className = `dot ${status.llm ? "on" : "off"}`;
}

/* ---------- tabs ---------- */
function showTab(name) {
  document.querySelectorAll(".tab").forEach((b) => b.classList.toggle("active", b.dataset.tab === name));
  document.querySelectorAll(".panel").forEach((p) => p.classList.toggle("active", p.id === `tab-${name}`));
}
document.querySelectorAll(".tab").forEach((b) => b.addEventListener("click", () => showTab(b.dataset.tab)));

/* ---------- chat ---------- */
function renderWelcome() {
  const cards = t("suggestions").map(([tag, q]) =>
    `<button data-q="${esc(q)}"><span class="tag">${esc(tag)}</span>${esc(q)}</button>`).join("");
  $("#messages").innerHTML = `<div class="welcome">
    <div class="mark">यो</div>
    <h1>${esc(t("welcomeTitle"))}</h1>
    <p>${esc(t("welcomeBody"))}</p>
    <div class="suggest">${cards}</div></div>`;
  $("#messages").querySelectorAll("[data-q]").forEach((b) => (b.onclick = () => send(b.dataset.q)));
}

function renderChips() {
  $("#chips").innerHTML = t("chips").map((q) => `<button class="chip">${esc(q)}</button>`).join("");
  $("#chips").querySelectorAll(".chip").forEach((b) => (b.onclick = () => send(b.textContent)));
}

function addRow(role, inner) {
  const row = document.createElement("div");
  row.className = `row ${role}`;
  row.innerHTML = role === "bot"
    ? `<div class="avatar">यो</div><div class="msg bot">${inner}</div>`
    : `<div class="msg user">${inner}</div>`;
  $("#messages").appendChild(row);
  $("#messages").scrollTop = $("#messages").scrollHeight;
  return row.querySelector(".msg");
}

function botHtml(res) {
  const L = I18N[res.lang] || I18N[lang];
  let html = renderMarkdown(res.answer);

  if (res.citations && res.citations.length) {
    html += `<div class="sources"><div class="sources-label">${esc(L.sources)}</div>`;
    res.citations.forEach((c, i) => {
      const title = res.lang === "hi" && c.title_hi ? c.title_hi : c.title;
      html += `<button class="cite" data-i="${i}">
        <span class="cite-num">${i + 1}</span>
        <span class="cite-body"><span class="cite-title">${esc(title)} <em>· ${esc(c.section)}</em></span>
        <span class="cite-quote">“${esc(c.quote)}”</span></span>
        <span class="cite-check ${c.verified ? "ok" : "no"}">${c.verified ? ICON.check : ICON.alert}</span></button>`;
    });
    html += `</div>`;
  }

  let badge = "";
  if (res.grounding) {
    const g = res.grounding;
    const ok = g.total > 0 && g.verified === g.total;
    badge = `<span class="badge ${ok ? "ok" : "warn"}">${ok ? ICON.shield : ICON.alert}${esc(ok ? L.verified(g.verified, g.total) : L.unverified(g.verified, g.total))}</span>`;
  } else if (res.mode === "clarify") {
    badge = `<span class="badge nf">${ICON.help}${esc(L.clarify)}</span>`;
  } else if (!res.found) {
    badge = `<span class="badge nf">${ICON.info}${esc(L.notFound)}</span>`;
  } else if (res.mode === "offline") {
    badge = `<span class="badge nf">${ICON.doc}${esc(L.offline)}</span>`;
  }
  html += `<div class="msg-foot">${badge}<span class="foot-actions">
    <button class="speak" title="Listen" aria-label="Listen">${ICON.speaker}</button>${now()}</span></div>`;
  return html;
}

async function send(text) {
  text = text.trim();
  if (!text) return;
  if (!history.length) $("#messages").innerHTML = "";
  $("#input").value = "";
  $("#chips").classList.remove("hidden");
  addRow("user", `${esc(text)}<div class="time">${now()}</div>`);
  const bubble = addRow("bot", `<div class="typing"><span></span><span></span><span></span></div>`);
  try {
    const r = await fetch("/api/chat", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text, lang, history: history.slice(-8) }),
    });
    if (!r.ok) throw new Error(await r.text());
    const res = await r.json();
    bubble.innerHTML = botHtml(res);
    bubble.querySelectorAll(".cite").forEach((b) =>
      (b.onclick = () => { const c = res.citations[+b.dataset.i]; if (c.doc_id) openDoc(c.doc_id, c.quote); }));
    bubble.querySelector(".speak").onclick = () => speak(res.answer, res.lang);
    history.push({ role: "user", content: text }, { role: "assistant", content: res.answer });
    console.debug("retrieval", res.search_query, res.retrieved);
  } catch (e) {
    bubble.innerHTML = `<p>${esc(t("error"))}</p>`;
    console.error(e);
  }
  $("#messages").scrollTop = $("#messages").scrollHeight;
}

$("#composer").addEventListener("submit", (e) => { e.preventDefault(); send($("#input").value); });

/* ---------- voice ---------- */
const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
let rec = null;
$("#mic").addEventListener("click", () => {
  if (!SR) { $("#input").placeholder = t("voiceUnsupported"); return; }
  if (rec) { rec.stop(); return; }
  rec = new SR();
  rec.lang = lang === "hi" ? "hi-IN" : "en-IN";
  rec.interimResults = true;
  $("#mic").classList.add("rec");
  rec.onresult = (e) => {
    const r = e.results[e.results.length - 1];
    $("#input").value = r[0].transcript;
    if (r.isFinal) send(r[0].transcript);
  };
  rec.onend = () => { $("#mic").classList.remove("rec"); rec = null; };
  rec.start();
});

function speak(text, l) {
  if (!window.speechSynthesis) return;
  speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text.replace(/[*#•-]/g, " "));
  u.lang = l === "hi" ? "hi-IN" : "en-IN";
  const voices = speechSynthesis.getVoices();
  const v = voices.find((v) => v.lang === u.lang) || voices.find((v) => v.lang.startsWith(l === "hi" ? "hi" : "en"));
  if (v) u.voice = v;
  speechSynthesis.speak(u);
}

/* ---------- eligibility ---------- */
const FLAGS = ["owns_land", "has_bank_account", "income_tax_payer", "has_pucca_house", "has_lpg",
               "has_daughter_under_10", "pregnant_or_lactating", "class12_top20"];

function renderFlags() {
  const box = $("#yesno");
  box.innerHTML = FLAGS.map((f) => `<div class="yn-row"><span>${esc(t("flags")[f])}</span>
    <div class="pill-seg" data-f="${f}">
      <button type="button" data-v="true" class="${flagState[f] === true ? "on" : ""}">${esc(t("yes"))}</button>
      <button type="button" data-v="false" class="${flagState[f] === false ? "on" : ""}">${esc(t("no"))}</button>
    </div></div>`).join("");
  box.querySelectorAll(".pill-seg button").forEach((b) => (b.onclick = () => {
    const f = b.parentElement.dataset.f;
    const v = b.dataset.v === "true";
    flagState[f] = flagState[f] === v ? undefined : v;
    renderFlags();
  }));
}

$("#elig-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const profile = {};
  for (const [k, v] of new FormData(e.target).entries()) {
    if (v !== "") profile[k] = ["age", "income"].includes(k) ? Number(v) : v;
  }
  for (const f of FLAGS) if (flagState[f] !== undefined) profile[f] = flagState[f];
  const r = await fetch("/api/eligibility", {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(profile),
  });
  lastEligibility = (await r.json()).results;
  renderEligibility();
  $("#elig-results").scrollIntoView({ behavior: "smooth", block: "start" });
});

function eligCard(s) {
  const icon = { true: ["yes", ICON.check], false: ["no", ICON.cross], null: ["unk", ICON.help] };
  const checks = s.checks.map((c) => {
    const [cls, svg] = icon[c.result];
    return `<li class="${cls}">${svg}<span>${esc(c[lang])}</span></li>`;
  }).join("");
  return `<div class="card scheme-card">
    <div class="top"><div>
      <span class="cat" style="--c:${CATEGORY_COLOR[s.category] || "var(--primary)"}"><i></i>${esc(s.category)}</span>
      <h3>${esc(schemeTitle(s))}</h3></div>
      <span class="pill ${s.status}">${esc(t(s.status))}</span></div>
    <ul class="checks">${checks}</ul>
    <div class="actions">
      <button class="link-btn solid" data-ask="${esc(s.scheme_id)}">${ICON.chat}${esc(t("ask"))}</button>
      <button class="link-btn" data-view="${esc(s.scheme_id)}">${ICON.doc}${esc(t("view"))}</button>
    </div></div>`;
}

function renderEligibility() {
  if (!lastEligibility) return;
  const by = (st) => lastEligibility.filter((s) => s.status === st);
  const [yes, maybe, no] = [by("eligible"), by("maybe"), by("not_eligible")];
  let html = `<div class="stats">
    <div class="card stat ok"><b>${yes.length}</b><span>${esc(t("statEligible"))}</span></div>
    <div class="card stat warn"><b>${maybe.length}</b><span>${esc(t("statMaybe"))}</span></div>
    <div class="card stat bad"><b>${no.length}</b><span>${esc(t("statNot"))}</span></div></div>`;
  html += [...yes, ...maybe].map(eligCard).join("");
  if (no.length) html += `<details class="others"><summary>${esc(t("others")(no.length))}</summary>${no.map(eligCard).join("")}</details>`;
  const box = $("#elig-results");
  box.innerHTML = html;
  box.querySelectorAll("[data-ask]").forEach((b) => (b.onclick = () => {
    const s = lastEligibility.find((x) => x.scheme_id === b.dataset.ask);
    showTab("chat");
    send(t("askTpl")(schemeTitle(s)));
  }));
  box.querySelectorAll("[data-view]").forEach((b) => (b.onclick = () => openDoc(b.dataset.view)));
}

/* ---------- documents ---------- */
function renderDocs() {
  const list = $("#doc-list");
  list.innerHTML = schemes.map((d) => `<button class="card doc" data-id="${esc(d.id)}">
    <span class="cat" style="--c:${CATEGORY_COLOR[d.category] || "var(--primary)"}"><i></i>${esc(d.category)}</span>
    <span class="name">${esc(schemeTitle(d))}</span>
    <span class="alt">${esc(lang === "hi" ? d.title : d.title_hi)}</span></button>`).join("");
  list.querySelectorAll(".doc").forEach((b) => (b.onclick = () => openDoc(b.dataset.id)));
}

function highlight(html, quote) {
  if (!quote) return html;
  const words = esc(quote).replace(/[.\s]+$/, "").split(/\s+/).map((w) => w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
  if (!words.length) return html;
  const re = new RegExp(words.join("[\\s\\S]{0,12}?"), "i");
  return html.replace(re, (m) => `<mark id="hl">${m}</mark>`);
}

async function openDoc(id, quote) {
  const d = await (await fetch(`/api/schemes/${encodeURIComponent(id)}`)).json();
  $("#modal-title").textContent = schemeTitle(d);
  $("#modal-sub").textContent = lang === "hi" ? d.title : d.title_hi;
  $("#modal-src").textContent = `${t("source")} ↗`;
  $("#modal-src").href = d.source.startsWith("http") ? d.source : "#";
  const body = renderMarkdown(d.body.replace(/^## (.*)$/gm, "§§$1")).replace(/<p>§§(.*?)<\/p>/g, "<h4>$1</h4>");
  $("#modal-body").innerHTML = highlight(body, quote);
  $("#modal").classList.remove("hidden");
  const hl = document.getElementById("hl");
  if (hl) hl.scrollIntoView({ block: "center" });
}
const closeModal = () => $("#modal").classList.add("hidden");
$("#modal-close").onclick = closeModal;
$("#modal").addEventListener("click", (e) => { if (e.target.id === "modal") closeModal(); });
document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeModal(); });

/* ---------- boot ---------- */
(async function init() {
  [status, schemes] = await Promise.all([
    fetch("/api/status").then((r) => r.json()),
    fetch("/api/schemes").then((r) => r.json()),
  ]);
  applyLang();
})();
