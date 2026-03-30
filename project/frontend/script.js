"use strict";
const API_BASE = "http://localhost:5000";
let currentLang = "en";
let selectedFile = null;

//i18n
const T = {
  en: {
    badge: "AI-Powered Disease Diagnosis",
    title: "Identify Crop Disease<br /><span class='headline-accent'>Before It Spreads</span>",
    desc: "Convolutional neural network trained on thousands of leaf specimens. One upload — instant diagnosis, confidence score, and treatment protocol.",
    stat1: "Disease Classes",
    stat2: "Bilingual Output",
    uploadTitle: "Upload Leaf Image",
    dropText: "Drop your leaf image here",
    dropOr: "or click to browse files",
    browseLabel: "Choose File",
    analyseText: "Analyse Leaf",
    loadLabel: "Running CNN inference…",
    resultTitle: "Diagnosis Report",
    lblDisease: "Disease Detected",
    lblConf: "Model Confidence",
    lblCause: "Root Cause",
    lblTreatment: "Treatment Protocol",
    historyTitle: "Scan History",
    placeholder: "Awaiting leaf image",
    histEmpty: "No scans yet",
    footerText: "TensorFlow CNN · MySQL · Flask · Built for Indian Farmers",
    errNoFile: "Please select an image first.",
    errServer: "Server error — is Flask running?",
    successMsg: "Analysis complete ✓",
    stepCount: (n) => `${n} steps`,
    healthy: "Healthy",
    disease: "Disease Detected",
  },
  hi: {
    badge: "AI-आधारित रोग निदान",
    title: "फसल रोग पहचानें<br /><span class='headline-accent'>फैलने से पहले</span>",
    desc: "हजारों पत्ती नमूनों पर प्रशिक्षित CNN मॉडल। एक बार अपलोड करें — तुरंत निदान, विश्वास स्कोर और उपचार प्रोटोकॉल।",
    stat1: "रोग वर्ग",
    stat2: "द्विभाषी आउटपुट",
    uploadTitle: "पत्ती की छवि अपलोड करें",
    dropText: "यहाँ पत्ती की छवि छोड़ें",
    dropOr: "या फ़ाइल चुनने के लिए क्लिक करें",
    browseLabel: "फ़ाइल चुनें",
    analyseText: "पत्ती विश्लेषण करें",
    loadLabel: "CNN अनुमान चल रहा है…",
    resultTitle: "निदान रिपोर्ट",
    lblDisease: "पहचाना गया रोग",
    lblConf: "मॉडल विश्वास",
    lblCause: "मूल कारण",
    lblTreatment: "उपचार प्रोटोकॉल",
    historyTitle: "स्कैन इतिहास",
    placeholder: "पत्ती की छवि की प्रतीक्षा",
    histEmpty: "अभी कोई स्कैन नहीं",
    footerText: "TensorFlow CNN · MySQL · Flask · भारतीय किसानों के लिए",
    errNoFile: "कृपया पहले एक छवि चुनें।",
    errServer: "सर्वर त्रुटि — क्या Flask चल रहा है?",
    successMsg: "विश्लेषण पूर्ण ✓",
    stepCount: (n) => `${n} चरण`,
    healthy: "स्वस्थ",
    disease: "रोग पाया गया",
  },
};

const $ = (id) => document.getElementById(id);
function esc(str) {
  return String(str)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
function fmt(iso) {
  try {
    return new Date(iso).toLocaleString(currentLang === "hi" ? "hi-IN" : "en-IN",
      { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
  } catch { return ""; }
}

function setLanguage(lang) {
  currentLang = lang;
  const t = T[lang];
  $("btn-en").classList.toggle("active", lang === "en");
  $("btn-hi").classList.toggle("active", lang === "hi");
  $("hero-badge").textContent = t.badge;
  $("hero-title").innerHTML = t.title;
  $("hero-desc").textContent = t.desc;
  $("stat1").textContent = t.stat1;
  $("stat2").textContent = t.stat2;
  $("upload-title").textContent = t.uploadTitle;
  $("drop-text").textContent = t.dropText;
  $("drop-or").textContent = t.dropOr;
  $("browse-text").textContent = t.browseLabel;
  $("analyse-text").textContent = t.analyseText;
  $("loader-label").textContent = t.loadLabel;
  $("result-title").textContent = t.resultTitle;
  $("lbl-disease").textContent = t.lblDisease;
  $("lbl-confidence").textContent = t.lblConf;
  $("lbl-cause").innerHTML = `<svg width="12" height="12" viewBox="0 0 12 12" fill="none"><circle cx="6" cy="6" r="5" stroke="var(--amber)" stroke-width="1.2"/><path d="M6 3.5v3M6 8.5v.2" stroke="var(--amber)" stroke-width="1.3" stroke-linecap="round"/></svg> ${t.lblCause}`;
  $("lbl-treatment").textContent = t.lblTreatment;
  $("history-title").textContent = t.historyTitle;
  $("placeholder-text").textContent = t.placeholder;
  $("history-empty").querySelector("span").textContent = t.histEmpty;
  $("footer-text").textContent = t.footerText;
}

function handleFile(file) {
  if (!file) return;
  if (!file.type.startsWith("image/")) {
    showToast(T[currentLang].errNoFile, "error"); return;
  }
  selectedFile = file;
  const reader = new FileReader();
  reader.onload = (e) => {
    $("preview-img").src = e.target.result;
    $("dz-filename").textContent = file.name;
    $("dz-preview").style.display = "block";
    $("dz-idle").style.display = "none";
    $("analyse-btn").disabled = false;
  };
  reader.readAsDataURL(file);
}

function removeFile() {
  selectedFile = null;
  $("file-input").value = "";
  $("preview-img").src = "";
  $("dz-preview").style.display = "none";
  $("dz-idle").style.display = "flex";
  $("analyse-btn").disabled = true;
}

const dz = $("drop-zone");
dz.addEventListener("dragover", (e) => { e.preventDefault(); dz.classList.add("dragover"); });
dz.addEventListener("dragleave", () => dz.classList.remove("dragover"));
dz.addEventListener("drop", (e) => {
  e.preventDefault(); dz.classList.remove("dragover");
  handleFile(e.dataTransfer.files[0]);
});
$("file-input").addEventListener("change", (e) => handleFile(e.target.files[0]));
$("remove-btn").addEventListener("click", removeFile);

async function submitPrediction() {
  if (!selectedFile) { showToast(T[currentLang].errNoFile, "error"); return; }

  // UI: loading
  $("analyse-btn").disabled = true;
  $("loader-row").style.display = "flex";
  $("result-panel").style.display = "none";
  $("result-placeholder").style.display = "";
  animateLoader();

  const fd = new FormData();
  fd.append("file", selectedFile);
  fd.append("lang", currentLang);

  try {
    const res = await fetch(`${API_BASE}/predict`, { method: "POST", body: fd });
    if (!res.ok) {
      const e = await res.json().catch(() => ({}));
      throw new Error(e.error || `HTTP ${res.status}`);
    }
    const data = await res.json();
    if (!data.success) throw new Error(data.error || "Unknown error");

    renderResult(data);
    showToast(T[currentLang].successMsg, "success");
    loadHistory();

  } catch (err) {
    console.error(err);
    showToast(`${T[currentLang].errServer} (${err.message})`, "error");
  } finally {
    $("loader-row").style.display = "none";
    $("analyse-btn").disabled = false;
    stopLoader();
  }
}

let loaderRAF = null;
function animateLoader() {
  const fill = $("loader-fill");
  let w = 0;
  function step() {
    w = Math.min(w + (100 - w) * 0.012, 92);
    fill.style.width = w + "%";
    loaderRAF = requestAnimationFrame(step);
  }
  loaderRAF = requestAnimationFrame(step);
}
function stopLoader() {
  cancelAnimationFrame(loaderRAF);
  const fill = $("loader-fill");
  fill.style.width = "100%";
  setTimeout(() => { fill.style.width = "0%"; }, 400);
}

// Render result 
function renderResult(data) {
  const isHealthy = data.disease.toLowerCase().includes("healthy");
  const t = T[currentLang];

  // Show/hide panels
  $("result-placeholder").style.display = "none";
  $("result-panel").style.display = "block";
  $("result-panel").style.animation = "fadeUp .45s ease both";

  // Thumb
  $("result-img").src = `${API_BASE}${data.image_url}`;

  // Status chip
  const ts = $("thumb-status");
  if (isHealthy) {
    ts.textContent = "✓ OK";
    ts.style.cssText = "background:rgba(74,222,144,.2);color:var(--accent);font-size:.6rem;padding:.15rem .4rem;border-radius:4px;font-weight:700;font-family:var(--font-display);letter-spacing:.06em;text-transform:uppercase;position:absolute;top:.4rem;right:.4rem;";
  } else {
    ts.textContent = "⚠";
    ts.style.cssText = "background:rgba(255,77,77,.2);color:#ff7070;font-size:.7rem;padding:.15rem .45rem;border-radius:4px;font-weight:700;position:absolute;top:.4rem;right:.4rem;";
  }

  // Verdict
  $("lbl-disease").textContent = t.lblDisease;
  $("disease-name").textContent = data.name;

  const tag = $("verdict-tag");
  const vdot = $("vtag-dot");
  const vtxt = $("vtag-text");
  if (isHealthy) {
    tag.style.cssText = "display:inline-flex;align-items:center;gap:.4rem;font-size:.72rem;font-weight:600;padding:.25rem .7rem;border-radius:50px;background:rgba(74,222,144,.12);border:1px solid rgba(74,222,144,.25);color:var(--accent);font-family:var(--font-display);";
    vdot.style.color = "var(--accent)";
    vtxt.textContent = t.healthy;
  } else {
    tag.style.cssText = "display:inline-flex;align-items:center;gap:.4rem;font-size:.72rem;font-weight:600;padding:.25rem .7rem;border-radius:50px;background:rgba(255,77,77,.1);border:1px solid rgba(255,77,77,.25);color:#ff7070;font-family:var(--font-display);";
    vdot.style.color = "#ff7070";
    vtxt.textContent = t.disease;
  }

  // Confidence
  const pct = Math.min(Math.round(data.confidence), 100);
  $("confidence-pct").textContent = `${pct}%`;
  setTimeout(() => {
    let color;
    if (pct >= 75) color = "#4ade90";
    else if (pct >= 50) color = "#f5a623";
    else color = "#ff6b6b";
    $("conf-bar").style.width = `${pct}%`;
    $("conf-bar").style.background = color;
    $("conf-glow").style.width = `${pct}%`;
    $("conf-glow").style.background = color;
  }, 120);

  // Cause
  $("cause-text").textContent = data.cause;

  // Treatment
  const list = $("treatment-list");
  list.innerHTML = "";
  (data.treatment || []).forEach((step, i) => {
    const li = document.createElement("li");
    li.textContent = step;
    li.style.animationDelay = `${i * 70}ms`;
    list.appendChild(li);
  });
  $("step-count").textContent = t.stepCount(data.treatment?.length || 0);

  // Sim notice
  $("sim-notice").style.display = data.mode === "simulation" ? "flex" : "none";

  // Scroll into view on mobile
  if (window.innerWidth < 900) {
    $("result-panel").scrollIntoView({ behavior: "smooth", block: "start" });
  }
}

function resetAll() {
  removeFile();
  $("result-panel").style.display = "none";
  $("result-placeholder").style.display = "";
  $("conf-bar").style.width = "0%";
  $("conf-glow").style.width = "0%";
  if (window.innerWidth < 900) {
    $("upload-panel").scrollIntoView({ behavior: "smooth" });
  }
}

async function loadHistory() {
  const feed = $("history-list");
  const empty = $("history-empty");

  try {
    const res = await fetch(`${API_BASE}/history`);
    const data = await res.json();

    if (!data.success || !data.history.length) {
      feed.innerHTML = "";
      feed.appendChild(buildEmpty());
      return;
    }

    feed.innerHTML = "";
    data.history.forEach((row, i) => {
      const item = document.createElement("div");
      item.className = "feed-item";
      item.style.animationDelay = `${i * 40}ms`;

      const img = document.createElement("img");
      img.src = `${API_BASE}${row.image_path}`;
      img.alt = row.disease;
      img.className = "feed-thumb";
      img.onerror = () => {
        img.style.cssText = "width:42px;height:42px;border-radius:6px;background:var(--bg-overlay);border:1px solid var(--border);display:flex;align-items:center;justify-content:center;font-size:1.1rem;flex-shrink:0;";
        img.outerHTML = `<div class="feed-thumb" style="display:flex;align-items:center;justify-content:center;font-size:1.2rem;">🍃</div>`;
      };

      const info = document.createElement("div");
      info.className = "feed-info";

      const name = document.createElement("div");
      name.className = "feed-disease";
      name.textContent = row.disease;

      const meta = document.createElement("div");
      meta.className = "feed-meta";

      const conf = document.createElement("span");
      conf.className = "feed-conf";
      conf.textContent = `${Math.round(row.confidence)}%`;

      const time = document.createElement("span");
      time.className = "feed-time";
      time.textContent = fmt(row.created_at);

      meta.append(conf, time);
      info.append(name, meta);
      item.append(img, info);
      feed.appendChild(item);
    });
  } catch {
    feed.innerHTML = "";
    feed.appendChild(buildEmpty());
  }
}

function buildEmpty() {
  const d = document.createElement("div");
  d.className = "feed-empty";
  d.innerHTML = `<div class="empty-glyph">◎</div><span>${T[currentLang].histEmpty}</span>`;
  return d;
}

async function checkHealth() {
  const dot = document.querySelector(".status-dot-pulse");
  const label = $("status-label");
  try {
    const res = await fetch(`${API_BASE}/health`, { signal: AbortSignal.timeout(3000) });
    const data = await res.json();
    dot.style.background = "var(--accent)";
    label.textContent = data.mode === "simulation" ? "Demo" : "Live";
    label.style.color = "var(--accent)";
  } catch {
    dot.style.background = "var(--red)";
    dot.style.boxShadow = "0 0 0 0 rgba(255,77,77,.5)";
    label.textContent = "Offline";
    label.style.color = "var(--red)";
    dot.style.animation = "none";
  }
}

function showToast(msg, type = "info") {
  const t = $("toast");
  t.textContent = msg;
  t.className = `toast ${type} show`;
  clearTimeout(t._timer);
  t._timer = setTimeout(() => t.classList.remove("show"), 3500);
}

(function init() {
  setLanguage("en");
  loadHistory();
  checkHealth();
})();
