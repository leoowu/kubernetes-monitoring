#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path

p = Path("/workspace/build_tracker.py")
text = p.read_text(encoding="utf-8")

EVENT_META = {
    "binance_20261029": ("2026-10-29", "2026-10-29"),
    "mercado_20261102": ("2026-11-02", "2026-11-02"),
    "bitmart_20261102": ("2026-11-02", "2026-11-02"),
    "coindcx_202610": ("2026-10-21", "2026-10-21"),
    "bitget_20260924": ("2026-09-24", "2026-09-24"),
    "afx_20260722": ("2026-07-22", "2026-07-22"),
    "triplea_20260725": ("2026-07-25", "2026-07"),
    "phemex_202501": ("2025-01-15", "2025-01"),
}

for cid, (ed, el) in EVENT_META.items():
    needle = f'"id": "{cid}",\n    "name":'
    repl = f'"id": "{cid}",\n    "eventDate": "{ed}",\n    "eventLabel": "{el}",\n    "name":'
    if needle not in text:
        raise SystemExit(f"missing case id block: {cid}")
    text = text.replace(needle, repl, 1)

old_banner_css = '  .banner { background: #fff8ec; border: 1px solid #e3d2a8; border-radius: 12px; padding: 10px 14px; margin-bottom: 14px; font-size: .9rem; }\n</style>'
new_banner_css = r'''  .banner { background: #fff8ec; border: 1px solid #e3d2a8; border-radius: 12px; padding: 10px 14px; margin-bottom: 14px; font-size: .9rem; }
  .topnav {
    position: sticky; top: 0; z-index: 40; margin: 0 0 14px;
    background: rgba(20,47,56,.94); backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,.12); border-radius: 14px;
    padding: 8px 10px; display: flex; flex-wrap: wrap; gap: 6px; align-items: center;
  }
  .topnav a, .topnav button.navbtn {
    appearance: none; border: 0; cursor: pointer; font: inherit;
    color: #f3efe6; text-decoration: none; background: transparent;
    padding: 7px 11px; border-radius: 10px; font-size: .84rem; white-space: nowrap;
  }
  .topnav a:hover, .topnav button.navbtn:hover, .topnav a.active, .topnav button.navbtn.active {
    background: rgba(255,255,255,.14);
  }
  .topnav .sep { width: 1px; height: 18px; background: rgba(255,255,255,.18); margin: 0 2px; }
  .case-nav { display: flex; flex-wrap: wrap; gap: 8px; margin: 0 0 14px; }
  .case-nav button {
    font: inherit; cursor: pointer; border: 1px solid var(--line); background: var(--card);
    color: var(--ink); border-radius: 999px; padding: 7px 12px; font-size: .82rem;
  }
  .case-nav button.active { background: var(--teal); color: #fff; border-color: var(--teal); }
  .secure-rail { display: grid; gap: 10px; }
  .secure-item {
    display: grid; grid-template-columns: 108px 1fr auto; gap: 12px; align-items: start;
    border: 1px solid var(--line); border-radius: 14px; padding: 12px 14px; background: #fff;
    cursor: pointer; text-align: left; width: 100%; font: inherit; color: inherit;
  }
  .secure-item:hover { border-color: #b7c9c8; background: var(--teal-soft); }
  .secure-item .when { font-weight: 750; color: var(--teal); font-size: .92rem; }
  .secure-item .title { font-weight: 700; margin-bottom: 2px; }
  .secure-item .meta { color: var(--muted); font-size: .84rem; }
  .secure-item .amt { font-weight: 700; color: var(--red); font-size: .9rem; white-space: nowrap; }
  #viewOverview, #viewCase { scroll-margin-top: 72px; }
  #sec-summary, #sec-status, #sec-timeline, #sec-funds, #sec-links, #sec-fetch { scroll-margin-top: 72px; }
  @media (max-width: 720px) {
    .secure-item { grid-template-columns: 1fr; }
    .secure-item .amt { justify-self: start; }
  }
</style>'''
if old_banner_css not in text:
    raise SystemExit("banner css not found")
text = text.replace(old_banner_css, new_banner_css, 1)

old_body = r'''<div class="wrap">
  <header>
    <h1>交易所被盗案件进展追踪</h1>
    <p>已收录 Binance / Mercado Bitcoin / BitMart / CoinDCX / Bitget / Phemex / Triple-A / AFX。点「更新」拉公开源并对比上次快照。</p>
    <div class="toolbar">
      <select id="caseSelect" aria-label="选择案件"></select>
      <button class="primary" id="btnUpdate">更新</button>
      <button class="ghost" id="btnReset">重置本地快照</button>
      <button class="ghost" id="btnExport">导出 JSON</button>
    </div>
    <div class="status-line" id="statusLine">尚未更新 · 当前显示内置基线</div>
    <div class="err" id="errBox"></div>
  </header>

  <div class="banner">基线日期：<strong>2026-11-07</strong> · 默认显示最新大案 Binance。切换下拉可看其他案件。</div>
  <div class="delta" id="deltaBox"><h2>相对上次的最新变化</h2><div id="deltaBody"></div></div>
  <div class="grid" id="kpiGrid"></div>
  <section class="card"><h2>案件摘要</h2><div id="summary"></div></section>
  <section class="card"><h2>关键节点</h2>
    <table><thead><tr><th>维度</th><th>状态</th><th>备注</th></tr></thead><tbody id="statusTable"></tbody></table>
  </section>
  <section class="card"><h2>时间线</h2><ul class="timeline" id="timeline"></ul></section>
  <section class="card"><h2>资金停留 / 在途 / 出途</h2><div id="fundFlow"></div></section>
  <section class="card"><h2>官方与追踪链接</h2><div class="links" id="links"></div></section>
  <section class="card"><h2>本次更新抓取原文</h2>
    <p class="muted">点击更新后显示公开源文本片段。</p>
    <pre class="fetch" id="fetchDump"></pre>
  </section>
  <footer>仅供信息追踪，非投资建议。数据保存在浏览器 localStorage。</footer>
</div>
<script>
'''

new_body = r'''<div class="wrap">
  <nav class="topnav" aria-label="页面导航">
    <button type="button" class="navbtn active" data-view="overview" id="navOverview">安全时间线</button>
    <button type="button" class="navbtn" data-view="case" id="navCase">案件详情</button>
    <span class="sep" aria-hidden="true"></span>
    <a href="#sec-summary" data-case-anchor>摘要</a>
    <a href="#sec-status" data-case-anchor>关键节点</a>
    <a href="#sec-timeline" data-case-anchor>案件时间线</a>
    <a href="#sec-funds" data-case-anchor>资金流</a>
    <a href="#sec-links" data-case-anchor>链接</a>
  </nav>

  <header>
    <h1>交易所被盗案件进展追踪</h1>
    <p>顶栏可切「安全时间线」总览，或进入单案详情。点「更新」拉公开源并对比上次快照。</p>
    <div class="toolbar">
      <select id="caseSelect" aria-label="选择案件"></select>
      <button class="primary" id="btnUpdate">更新</button>
      <button class="ghost" id="btnReset">重置本地快照</button>
      <button class="ghost" id="btnExport">导出 JSON</button>
    </div>
    <div class="status-line" id="statusLine">尚未更新 · 当前显示内置基线</div>
    <div class="err" id="errBox"></div>
  </header>

  <div class="banner">基线日期：<strong>2026-11-07</strong> · 顶栏「安全时间线」按事发日排序；点任一事件进入详情。</div>

  <section class="card" id="viewOverview">
    <h2>安全时间线（全部案件）</h2>
    <p class="muted" style="margin-top:-4px">按事发日期从新到旧排列。点击条目切换到对应案件详情。</p>
    <div class="secure-rail" id="secureTimeline"></div>
  </section>

  <div id="viewCase" hidden>
    <div class="case-nav" id="caseNav" aria-label="案件快捷切换"></div>
    <div class="delta" id="deltaBox"><h2>相对上次的最新变化</h2><div id="deltaBody"></div></div>
    <div class="grid" id="kpiGrid"></div>
    <section class="card" id="sec-summary"><h2>案件摘要</h2><div id="summary"></div></section>
    <section class="card" id="sec-status"><h2>关键节点</h2>
      <table><thead><tr><th>维度</th><th>状态</th><th>备注</th></tr></thead><tbody id="statusTable"></tbody></table>
    </section>
    <section class="card" id="sec-timeline"><h2>案件时间线</h2><ul class="timeline" id="timeline"></ul></section>
    <section class="card" id="sec-funds"><h2>资金停留 / 在途 / 出途</h2><div id="fundFlow"></div></section>
    <section class="card" id="sec-links"><h2>官方与追踪链接</h2><div class="links" id="links"></div></section>
    <section class="card" id="sec-fetch"><h2>本次更新抓取原文</h2>
      <p class="muted">点击更新后显示公开源文本片段。</p>
      <pre class="fetch" id="fetchDump"></pre>
    </section>
  </div>

  <footer>仅供信息追踪，非投资建议。数据保存在浏览器 localStorage。</footer>
</div>
<script>
'''

if old_body not in text:
    raise SystemExit("body block not found")
text = text.replace(old_body, new_body, 1)

old_js_start = '''const STORAGE_KEY = "cex_hack_tracker_v2";
function $(id){return document.getElementById(id);}
function loadStore(){try{return JSON.parse(localStorage.getItem(STORAGE_KEY)||"{}");}catch(e){return {};}}
function saveStore(s){localStorage.setItem(STORAGE_KEY, JSON.stringify(s));}
function currentCaseId(){return $("caseSelect").value || "binance_20261029";}
function tagLabel(t){return ({ok:"闭环/正常",warn:"关注",bad:"风险/未闭环",info:"信息"})[t]||t;}
function escapeHtml(s){return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");}

function renderCase(caseId){
  const c=CASES[caseId]; if(!c) return;
  $("kpiGrid").innerHTML=c.kpis.map(k=>`<div class="kpi"><div class="n">${k.n}</div><div class="l">${k.l}</div></div>`).join("");
  $("summary").innerHTML=`<p>${c.summary}</p><p class="muted">内置基线：${c.baselineUpdated} · ${c.exchange} · ${c.lossLabel}</p>`;
  $("statusTable").innerHTML=c.statuses.map(([a,b,note,tag])=>`<tr><td>${a}</td><td><span class="tag ${tag}">${tagLabel(tag)}</span>${b}</td><td class="muted">${note}</td></tr>`).join("");
  $("timeline").innerHTML=c.timeline.map(x=>`<li><div class="t">${x.t}</div><div class="d">${x.d}</div></li>`).join("");
  $("fundFlow").innerHTML=`<table><thead><tr><th>状态</th><th>内容</th><th>备注</th></tr></thead><tbody>`+
    c.fundFlow.map(r=>`<tr><td><strong>${r[0]}</strong></td><td>${r[1]}</td><td class="muted">${r[2]}</td></tr>`).join("")+`</tbody></table>`;
  $("links").innerHTML=c.links.map(([n,u])=>`<div style="margin:6px 0"><a href="${u}" target="_blank" rel="noopener">${n}</a></div>`).join("");
  const snap=loadStore()[caseId];
  if(snap&&snap.lastCheckAt){
    $("statusLine").textContent=`上次更新：${snap.lastCheckAt} · 内置基线：${c.baselineUpdated}`;
    if(snap.lastDeltaHtml){$("deltaBox").classList.add("show");$("deltaBody").innerHTML=snap.lastDeltaHtml;}
  }else{
    $("statusLine").textContent=`尚未在本机点过更新 · 显示内置基线（${c.baselineUpdated}）`;
  }
}
'''

new_js_start = r'''const STORAGE_KEY = "cex_hack_tracker_v2";
const CASE_ORDER = ["binance_20261029","mercado_20261102","bitmart_20261102","coindcx_202610","bitget_20260924","afx_20260722","triplea_20260725","phemex_202501"];
function $(id){return document.getElementById(id);}
function loadStore(){try{return JSON.parse(localStorage.getItem(STORAGE_KEY)||"{}");}catch(e){return {};}}
function saveStore(s){localStorage.setItem(STORAGE_KEY, JSON.stringify(s));}
function currentCaseId(){return $("caseSelect").value || "binance_20261029";}
function tagLabel(t){return ({ok:"闭环/正常",warn:"关注",bad:"风险/未闭环",info:"信息"})[t]||t;}
function escapeHtml(s){return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");}

function setView(view){
  const overview = view === "overview";
  $("viewOverview").hidden = !overview;
  $("viewCase").hidden = overview;
  $("navOverview").classList.toggle("active", overview);
  $("navCase").classList.toggle("active", !overview);
  document.querySelectorAll("[data-case-anchor]").forEach(a=>{
    a.style.opacity = overview ? ".45" : "1";
    a.style.pointerEvents = overview ? "none" : "auto";
  });
}

function renderSecureTimeline(){
  const items = CASE_ORDER.filter(id=>CASES[id]).map(id=>({id, ...CASES[id]}))
    .sort((a,b)=> (b.eventDate||"").localeCompare(a.eventDate||""));
  $("secureTimeline").innerHTML = items.map(c=>{
    const shortName = (c.name||"").includes("·") ? (c.name.split("·").slice(1).join("·").trim()) : c.name;
    return `<button type="button" class="secure-item" data-case="${c.id}">
      <div class="when">${escapeHtml(c.eventLabel||c.eventDate||"")}</div>
      <div>
        <div class="title">${escapeHtml(c.exchange)} · ${escapeHtml(shortName)}</div>
        <div class="meta">${escapeHtml((c.summary||"").slice(0,88))}…</div>
      </div>
      <div class="amt">${escapeHtml(c.lossLabel||"")}</div>
    </button>`;
  }).join("");
  $("secureTimeline").querySelectorAll("[data-case]").forEach(btn=>{
    btn.addEventListener("click",()=>openCase(btn.getAttribute("data-case"), true));
  });
}

function renderCaseNav(activeId){
  $("caseNav").innerHTML = CASE_ORDER.filter(id=>CASES[id]).map(id=>{
    const c=CASES[id];
    return `<button type="button" data-case="${id}" class="${id===activeId?"active":""}">${escapeHtml(c.exchange)}</button>`;
  }).join("");
  $("caseNav").querySelectorAll("[data-case]").forEach(btn=>{
    btn.addEventListener("click",()=>openCase(btn.getAttribute("data-case"), false));
  });
}

function openCase(caseId, jumpSummary){
  if(!CASES[caseId]) return;
  $("caseSelect").value = caseId;
  $("deltaBox").classList.remove("show");
  $("fetchDump").classList.remove("show");
  setView("case");
  renderCase(caseId);
  if(jumpSummary){
    requestAnimationFrame(()=>{$("sec-summary").scrollIntoView({behavior:"smooth", block:"start"});});
  }
}

function renderCase(caseId){
  const c=CASES[caseId]; if(!c) return;
  renderCaseNav(caseId);
  $("kpiGrid").innerHTML=c.kpis.map(k=>`<div class="kpi"><div class="n">${k.n}</div><div class="l">${k.l}</div></div>`).join("");
  $("summary").innerHTML=`<p>${c.summary}</p><p class="muted">事发：${c.eventLabel||c.eventDate||"—"} · 内置基线：${c.baselineUpdated} · ${c.exchange} · ${c.lossLabel}</p>`;
  $("statusTable").innerHTML=c.statuses.map(([a,b,note,tag])=>`<tr><td>${a}</td><td><span class="tag ${tag}">${tagLabel(tag)}</span>${b}</td><td class="muted">${note}</td></tr>`).join("");
  $("timeline").innerHTML=c.timeline.map(x=>`<li><div class="t">${x.t}</div><div class="d">${x.d}</div></li>`).join("");
  $("fundFlow").innerHTML=`<table><thead><tr><th>状态</th><th>内容</th><th>备注</th></tr></thead><tbody>`+
    c.fundFlow.map(r=>`<tr><td><strong>${r[0]}</strong></td><td>${r[1]}</td><td class="muted">${r[2]}</td></tr>`).join("")+`</tbody></table>`;
  $("links").innerHTML=c.links.map(([n,u])=>`<div style="margin:6px 0"><a href="${u}" target="_blank" rel="noopener">${n}</a></div>`).join("");
  const snap=loadStore()[caseId];
  if(snap&&snap.lastCheckAt){
    $("statusLine").textContent=`上次更新：${snap.lastCheckAt} · 内置基线：${c.baselineUpdated}`;
    if(snap.lastDeltaHtml){$("deltaBox").classList.add("show");$("deltaBody").innerHTML=snap.lastDeltaHtml;}
  }else{
    $("statusLine").textContent=`尚未在本机点过更新 · 显示内置基线（${c.baselineUpdated}）`;
  }
}
'''

if old_js_start not in text:
    raise SystemExit("js start not found")
text = text.replace(old_js_start, new_js_start, 1)

old_init = '''function init(){
  const sel=$("caseSelect");
  const order=["binance_20261029","mercado_20261102","bitmart_20261102","coindcx_202610","bitget_20260924","afx_20260722","triplea_20260725","phemex_202501"];
  sel.innerHTML=order.filter(id=>CASES[id]).map(id=>`<option value="${id}">${CASES[id].name}</option>`).join("");
  sel.addEventListener("change",()=>{$("deltaBox").classList.remove("show");$("fetchDump").classList.remove("show");renderCase(sel.value);});
  $("btnUpdate").addEventListener("click", doUpdate);
  $("btnReset").addEventListener("click",()=>{const s=loadStore();delete s[currentCaseId()];saveStore(s);$("deltaBox").classList.remove("show");$("fetchDump").classList.remove("show");renderCase(currentCaseId());$("statusLine").textContent="已清除本机快照";});
  $("btnExport").addEventListener("click",()=>{
    const payload={exportedAt:new Date().toISOString(), caseId:currentCaseId(), baseline:CASES[currentCaseId()], localSnapshot:loadStore()[currentCaseId()]||null};
    const blob=new Blob([JSON.stringify(payload,null,2)],{type:"application/json"});
    const a=document.createElement("a"); a.href=URL.createObjectURL(blob); a.download=currentCaseId()+"-tracker-export.json"; a.click(); URL.revokeObjectURL(a.href);
  });
  renderCase(currentCaseId());
}
init();'''

new_init = '''function init(){
  const sel=$("caseSelect");
  sel.innerHTML=CASE_ORDER.filter(id=>CASES[id]).map(id=>`<option value="${id}">${CASES[id].name}</option>`).join("");
  sel.addEventListener("change",()=>openCase(sel.value, false));
  $("btnUpdate").addEventListener("click", ()=>{ setView("case"); doUpdate(); });
  $("btnReset").addEventListener("click",()=>{const s=loadStore();delete s[currentCaseId()];saveStore(s);$("deltaBox").classList.remove("show");$("fetchDump").classList.remove("show");renderCase(currentCaseId());$("statusLine").textContent="已清除本机快照";});
  $("btnExport").addEventListener("click",()=>{
    const payload={exportedAt:new Date().toISOString(), caseId:currentCaseId(), baseline:CASES[currentCaseId()], localSnapshot:loadStore()[currentCaseId()]||null};
    const blob=new Blob([JSON.stringify(payload,null,2)],{type:"application/json"});
    const a=document.createElement("a"); a.href=URL.createObjectURL(blob); a.download=currentCaseId()+"-tracker-export.json"; a.click(); URL.revokeObjectURL(a.href);
  });
  $("navOverview").addEventListener("click",()=>setView("overview"));
  $("navCase").addEventListener("click",()=>{ setView("case"); renderCase(currentCaseId()); });
  document.querySelectorAll("[data-case-anchor]").forEach(a=>{
    a.addEventListener("click",(e)=>{
      e.preventDefault();
      setView("case");
      renderCase(currentCaseId());
      const id=a.getAttribute("href").slice(1);
      requestAnimationFrame(()=>{ const el=$(id); if(el) el.scrollIntoView({behavior:"smooth", block:"start"}); });
    });
  });
  renderSecureTimeline();
  renderCase(currentCaseId());
  setView("overview");
}
init();'''

if old_init not in text:
    raise SystemExit("init not found")
text = text.replace(old_init, new_init, 1)

p.write_text(text, encoding="utf-8")
print("patched ok")
