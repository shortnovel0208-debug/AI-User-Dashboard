// AI 心智监测看板 - 前端逻辑
let META = { stance_labels: {}, author_labels: {} };
const STANCE_COLORS = {
  anxious: "#ff6b6b", optimistic: "#4ecb71", balanced: "#5c7cff", dismissive: "#9a8cff",
  still_code: "#4ecb71", ai_literacy: "#5c7cff",
  humanities_critical: "#ffbc5c", fundamentals_math: "#4ecbe8",
  no_code_needed: "#ff6b6b",
};
let trendChart, cmpEnChart, cmpCnChart;

async function fetchJSON(u) { const r = await fetch(u); return r.json(); }

function stanceLabel(topic, st) {
  return (META.stance_labels[topic] || {})[st] || st;
}
function authorLabel(a) { return META.author_labels[a] || a; }

// ---------- Tabs ----------
document.querySelectorAll(".tab").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    const tab = btn.dataset.tab;
    document.querySelectorAll(".panel").forEach(p => p.classList.add("hidden"));
    document.getElementById("tab-" + tab).classList.remove("hidden");
    if (tab === "trends") loadTrends();
    if (tab === "compare") loadCompare();
    if (tab === "quotes") loadQuotes();
    if (tab === "review") loadReview();
  });
});

// ---------- Trends ----------
async function loadTrends() {
  const topic = document.getElementById("trend-topic").value;
  const region = document.getElementById("trend-region").value;
  const author = document.getElementById("trend-author").value;
  const qs = new URLSearchParams({ topic });
  if (region) qs.set("region", region);
  if (author) qs.set("author_type", author);
  const data = await fetchJSON("/api/trends?" + qs);

  const datasets = Object.entries(data.stances).map(([st, arr]) => ({
    label: stanceLabel(topic, st),
    data: arr,
    borderColor: STANCE_COLORS[st] || "#888",
    backgroundColor: (STANCE_COLORS[st] || "#888") + "33",
    tension: 0.3, fill: false,
  }));
  const cfg = {
    type: "line",
    data: { labels: data.months, datasets },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { labels: { color: "#e8ebff" } } },
      scales: {
        x: { ticks: { color: "#9aa3d1" }, grid: { color: "#2a2f55" } },
        y: { ticks: { color: "#9aa3d1" }, grid: { color: "#2a2f55" }, beginAtZero: true },
      },
    },
  };
  if (trendChart) trendChart.destroy();
  trendChart = new Chart(document.getElementById("trend-chart"), cfg);
}
["trend-topic", "trend-region", "trend-author"].forEach(id =>
  document.getElementById(id).addEventListener("change", loadTrends));

// ---------- Compare ----------
async function loadCompare() {
  const topic = document.getElementById("cmp-topic").value;
  const data = await fetchJSON("/api/compare?topic=" + topic);
  const mk = (region, canvasId) => {
    const stances = data.regions[region] || {};
    const datasets = Object.entries(stances).map(([st, arr]) => ({
      label: stanceLabel(topic, st),
      data: arr,
      backgroundColor: STANCE_COLORS[st] || "#888",
    }));
    return {
      type: "bar",
      data: { labels: data.months, datasets },
      options: {
        responsive: true, maintainAspectRatio: false,
        plugins: { legend: { labels: { color: "#e8ebff", font: { size: 10 } } } },
        scales: {
          x: { stacked: true, ticks: { color: "#9aa3d1" }, grid: { color: "#2a2f55" } },
          y: { stacked: true, max: 100, ticks: { color: "#9aa3d1" }, grid: { color: "#2a2f55" } },
        },
      },
    };
  };
  if (cmpEnChart) cmpEnChart.destroy();
  if (cmpCnChart) cmpCnChart.destroy();
  cmpEnChart = new Chart(document.getElementById("cmp-en"), mk("EN"));
  cmpCnChart = new Chart(document.getElementById("cmp-cn"), mk("CN"));
}
document.getElementById("cmp-topic").addEventListener("change", loadCompare);

// ---------- Quotes ----------
async function loadQuotes() {
  const topic = document.getElementById("q-topic").value;
  const region = document.getElementById("q-region").value;
  const qs = new URLSearchParams({ topic });
  if (region) qs.set("region", region);
  const posts = await fetchJSON("/api/posts?" + qs);

  // 按 stance 分组
  const groups = {};
  posts.forEach(p => { (groups[p.stance] = groups[p.stance] || []).push(p); });
  const container = document.getElementById("quotes-list");
  container.innerHTML = "";
  Object.entries(groups).forEach(([st, list]) => {
    const h = document.createElement("h3");
    h.textContent = `${stanceLabel(topic, st)} · ${list.length} 条`;
    h.style.margin = "18px 0 6px";
    h.style.color = "#b4bbe4";
    container.appendChild(h);
    list.slice(0, 4).forEach(p => container.appendChild(renderQuote(p)));
  });
}
["q-topic", "q-region"].forEach(id =>
  document.getElementById(id).addEventListener("change", loadQuotes));

function renderQuote(p) {
  const el = document.createElement("div");
  el.className = "quote";
  const regionCls = p.region === "CN" ? "cn" : "en";
  el.innerHTML = `
    <div class="meta">
      <span class="pill ${regionCls}">${p.region}</span>
      <span class="pill">${p.source}</span>
      <span class="pill">${authorLabel(p.author_type)}</span>
      <span>${p.posted_at}</span>
      ${p.human_verified ? '<span class="pill" style="background:#2a5a3a;color:#b4f5c8">✓已审</span>' : ''}
      <a href="${p.url}" target="_blank" style="color:#5c7cff;margin-left:auto">source</a>
    </div>
    <p>${escapeHtml(p.original_text)}</p>
    ${p.translation ? `<p class="t">↳ ${escapeHtml(p.translation)}</p>` : ''}
  `;
  return el;
}
function escapeHtml(s) {
  return (s || "").replace(/[&<>"']/g, c => ({ "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;" }[c]));
}

// ---------- Review ----------
async function loadReview() {
  const verified = document.getElementById("r-filter").value;
  const qs = new URLSearchParams();
  if (verified !== "") qs.set("verified", verified);
  const [posts, stats] = await Promise.all([
    fetchJSON("/api/posts?" + qs),
    fetchJSON("/api/stats"),
  ]);
  document.getElementById("r-stats").textContent =
    `共 ${stats.total} 条 · 已审 ${stats.verified} · 未审 ${stats.unverified} · 人工覆写 stance ${stats.stance_overrides} 次`;
  document.getElementById("review-badge").textContent = stats.unverified || "";

  const box = document.getElementById("review-list");
  box.innerHTML = "";
  posts.forEach(p => box.appendChild(renderReviewCard(p)));
}
document.getElementById("r-filter").addEventListener("change", loadReview);

function renderReviewCard(p) {
  const ai = p.ai_labels_json ? JSON.parse(p.ai_labels_json) : {};
  const el = document.createElement("div");
  el.className = "rcard" + (p.human_verified ? " verified" : "");

  const topicOpts = ["anxiety","kids_learn"].map(v =>
    `<option value="${v}" ${p.topic===v?"selected":""}>${v==="anxiety"?"AI焦虑":"孩子学什么"}</option>`
  ).join("");
  const stanceOpts = Object.entries(META.stance_labels[p.topic] || {}).map(
    ([v,l]) => `<option value="${v}" ${p.stance===v?"selected":""}>${l}</option>`
  ).join("");
  const authorOpts = Object.entries(META.author_labels).map(
    ([v,l]) => `<option value="${v}" ${p.author_type===v?"selected":""}>${l}</option>`
  ).join("");
  const regionOpts = ["EN","CN"].map(v =>
    `<option value="${v}" ${p.region===v?"selected":""}>${v}</option>`
  ).join("");

  el.innerHTML = `
    <div class="meta" style="font-size:12px;color:#7a83b4">
      #${p.id} · ${p.source} · ${p.posted_at}
      ${p.human_verified ? '· <span style="color:#4ecb71">✓ 已审核</span>' : ''}
    </div>
    <div class="orig">${escapeHtml(p.original_text)}${p.translation?`<div class="t" style="color:#7a83b4;font-size:12px;margin-top:4px">↳ ${escapeHtml(p.translation)}</div>`:""}</div>
    <div class="fields">
      <div><label>议题 (AI: ${ai.topic||"?"})</label><select data-f="topic">${topicOpts}</select></div>
      <div><label>立场 (AI: ${ai.stance||"?"})</label><select data-f="stance">${stanceOpts}</select></div>
      <div><label>用户分层 (AI: ${ai.author_type||"?"})</label><select data-f="author_type">${authorOpts}</select></div>
      <div><label>地区 (AI: ${ai.region||"?"})</label><select data-f="region">${regionOpts}</select></div>
    </div>
    <label style="font-size:11px;color:#7a83b4">审核备注</label>
    <textarea data-f="human_notes" rows="2">${escapeHtml(p.human_notes||"")}</textarea>
    <div class="row-act" style="margin-top:8px">
      <button data-act="save">保存并标记已审核</button>
      <span class="changed"></span>
    </div>
  `;

  // 切换 topic 时 stance 候选也要跟着改
  el.querySelector('[data-f="topic"]').addEventListener("change", (e) => {
    const newTopic = e.target.value;
    const sel = el.querySelector('[data-f="stance"]');
    sel.innerHTML = Object.entries(META.stance_labels[newTopic] || {})
      .map(([v,l]) => `<option value="${v}">${l}</option>`).join("");
  });

  el.querySelector('[data-act="save"]').addEventListener("click", async () => {
    const payload = { id: p.id };
    el.querySelectorAll("[data-f]").forEach(n => payload[n.dataset.f] = n.value);
    const res = await fetch("/api/review", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (res.ok) {
      el.querySelector(".changed").textContent = "✓ 已写回";
      setTimeout(loadReview, 600);
    }
  });
  return el;
}

// ---------- Boot ----------
(async () => {
  META = await fetchJSON("/api/meta");
  loadTrends();
  // 顺便刷一下未审角标
  fetchJSON("/api/stats").then(s => {
    document.getElementById("review-badge").textContent = s.unverified || "";
  });
})();
