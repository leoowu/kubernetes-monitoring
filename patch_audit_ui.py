#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path

p = Path("/workspace/build_tracker.py")
text = p.read_text(encoding="utf-8")

# 1) Import AUDIT and merge in main()
if "from case_audit_data import AUDIT" not in text:
    text = text.replace(
        "from pathlib import Path\nimport json\n",
        "from pathlib import Path\nimport json\nfrom case_audit_data import AUDIT\n",
        1,
    )

# Match the actual file content (backslash-n inside quotes)
old_main = (
    "def main():\n"
    "    cases_json = json.dumps(CASES, ensure_ascii=False, indent=2)\n"
    '    full = HEAD + "\\nconst CASES = " + cases_json + ";\\n" + TAIL\n'
)

new_main = (
    "def main():\n"
    "    for cid, extra in AUDIT.items():\n"
    "        if cid not in CASES:\n"
    '            raise SystemExit(f"AUDIT key missing in CASES: {cid}")\n'
    "        CASES[cid].update(extra)\n"
    "    cases_json = json.dumps(CASES, ensure_ascii=False, indent=2)\n"
    '    full = HEAD + "\\nconst CASES = " + cases_json + ";\\n" + TAIL\n'
)

if old_main not in text:
    raise SystemExit("main() block not found")
text = text.replace(old_main, new_main, 1)

# 2) CSS additions before </style> in HEAD (the last .secure-item media query block ends with </style>)
css_anchor = "  @media (max-width: 720px) {\n    .secure-item { grid-template-columns: 1fr; }\n    .secure-item .amt { justify-self: start; }\n  }\n</style>"
css_extra = '''  @media (max-width: 720px) {
    .secure-item { grid-template-columns: 1fr; }
    .secure-item .amt { justify-self: start; }
  }
  .prose p { margin: 0 0 10px; }
  .prose ul { margin: 6px 0 12px; padding-left: 18px; }
  .prose li { margin: 4px 0; }
  .grade {
    display: inline-flex; align-items: center; gap: 8px; margin: 0 0 10px;
    padding: 8px 12px; border-radius: 12px; background: var(--teal-soft); color: var(--teal); font-weight: 700;
  }
  .subh { margin: 14px 0 6px; font-size: .95rem; color: var(--header); font-weight: 750; }
  .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
  @media (max-width: 800px) { .two-col { grid-template-columns: 1fr; } }
  .mini-card { border: 1px solid var(--line); border-radius: 12px; padding: 12px; background: #fff; }
  .mini-card h3 { margin: 0 0 8px; font-size: .9rem; }
  #sec-audit, #sec-funds-deep, #sec-biz, #sec-industry { scroll-margin-top: 72px; }
</style>'''
if css_anchor not in text:
    raise SystemExit("css anchor not found")
text = text.replace(css_anchor, css_extra, 1)

# 3) Nav links
old_nav = '''    <a href="#sec-summary" data-case-anchor>摘要</a>
    <a href="#sec-status" data-case-anchor>关键节点</a>
    <a href="#sec-timeline" data-case-anchor>案件时间线</a>
    <a href="#sec-funds" data-case-anchor>资金流</a>
    <a href="#sec-links" data-case-anchor>链接</a>'''
new_nav = '''    <a href="#sec-summary" data-case-anchor>摘要</a>
    <a href="#sec-audit" data-case-anchor>调查审计</a>
    <a href="#sec-funds-deep" data-case-anchor>资金追踪</a>
    <a href="#sec-biz" data-case-anchor>业务分析</a>
    <a href="#sec-industry" data-case-anchor>行业市场</a>
    <a href="#sec-timeline" data-case-anchor>案件时间线</a>
    <a href="#sec-links" data-case-anchor>链接</a>'''
if old_nav not in text:
    raise SystemExit("nav not found")
text = text.replace(old_nav, new_nav, 1)

# 4) Insert new sections after status card / before case timeline
old_sections = '''    <section class="card" id="sec-status"><h2>关键节点</h2>
      <table><thead><tr><th>维度</th><th>状态</th><th>备注</th></tr></thead><tbody id="statusTable"></tbody></table>
    </section>
    <section class="card" id="sec-timeline"><h2>案件时间线</h2><ul class="timeline" id="timeline"></ul></section>
    <section class="card" id="sec-funds"><h2>资金停留 / 在途 / 出途</h2><div id="fundFlow"></div></section>
    <section class="card" id="sec-links"><h2>官方与追踪链接</h2><div class="links" id="links"></div></section>'''

new_sections = '''    <section class="card" id="sec-status"><h2>关键节点</h2>
      <table><thead><tr><th>维度</th><th>状态</th><th>备注</th></tr></thead><tbody id="statusTable"></tbody></table>
    </section>
    <section class="card" id="sec-audit"><h2>安全调查审计</h2><div id="auditPanel" class="prose"></div></section>
    <section class="card" id="sec-funds-deep"><h2>资金追踪专章</h2><div id="fundDeepPanel" class="prose"></div></section>
    <section class="card" id="sec-biz"><h2>业务影响分析</h2><div id="bizPanel" class="prose"></div></section>
    <section class="card" id="sec-industry"><h2>市场 / 行业分析</h2><div id="industryPanel" class="prose"></div></section>
    <section class="card" id="sec-timeline"><h2>案件时间线</h2><ul class="timeline" id="timeline"></ul></section>
    <section class="card" id="sec-funds"><h2>资金停留 / 在途 / 出途（简表）</h2><div id="fundFlow"></div></section>
    <section class="card" id="sec-links"><h2>官方与追踪链接</h2><div id="links" class="links"></div></section>'''

if old_sections not in text:
    raise SystemExit("sections not found")
text = text.replace(old_sections, new_sections, 1)

# 5) Extend renderCase JS
old_render_tail = '''  $("links").innerHTML=c.links.map(([n,u])=>`<div style="margin:6px 0"><a href="${u}" target="_blank" rel="noopener">${n}</a></div>`).join("");
  const snap=loadStore()[caseId];'''

new_render_tail = '''  $("links").innerHTML=c.links.map(([n,u])=>`<div style="margin:6px 0"><a href="${u}" target="_blank" rel="noopener">${n}</a></div>`).join("");
  renderAudit(c);
  renderFundDeep(c);
  renderBiz(c);
  renderIndustry(c);
  const snap=loadStore()[caseId];'''

if old_render_tail not in text:
    raise SystemExit("renderCase tail not found")
text = text.replace(old_render_tail, new_render_tail, 1)

# 6) Insert helper renderers before openCase or after escapeHtml
helpers = r'''
function listHtml(arr){
  if(!arr||!arr.length) return "<p class='muted'>暂无</p>";
  return "<ul>"+arr.map(x=>"<li>"+escapeHtml(x)+"</li>").join("")+"</ul>";
}
function renderAudit(c){
  const a=c.audit||{};
  $("auditPanel").innerHTML = `
    <div class="grade">遏制评级：${escapeHtml(a.containmentGrade||"—")} <span class="muted" style="font-weight:500">${escapeHtml(a.containmentNotes||"")}</span></div>
    <div class="subh">攻击叙事（审计口径）</div>
    <p>${escapeHtml(a.narrative||"—")}</p>
    <div class="subh">攻击链</div>
    ${listHtml(a.attackChain)}
    <div class="subh">控制失效 / 根因要点</div>
    ${listHtml(a.controlFailures)}
    <div class="subh">关键证据</div>
    ${listHtml(a.evidence)}
    <div class="subh">IR 评价</div>
    <p>${escapeHtml(a.irCritique||"—")}</p>
    <div class="subh">整改建议</div>
    ${listHtml(a.recommendations)}
  `;
}
function renderFundDeep(c){
  const f=c.fundTracking||{};
  const rows=(f.buckets||[]).map(r=>`<tr><td><strong>${escapeHtml(r[0])}</strong></td><td>${escapeHtml(r[1])}</td><td class="muted">${escapeHtml(r[2])}</td></tr>`).join("");
  $("fundDeepPanel").innerHTML = `
    <p><strong>总览：</strong>${escapeHtml(f.statusSummary||"—")}</p>
    <table><thead><tr><th>分桶</th><th>规模/状态</th><th>说明</th></tr></thead><tbody>${rows||"<tr><td colspan=3 class='muted'>暂无分桶</td></tr>"}</tbody></table>
    <div class="two-col" style="margin-top:12px">
      <div class="mini-card"><h3>停留</h3><p>${escapeHtml(f.stay||"—")}</p></div>
      <div class="mini-card"><h3>在途</h3><p>${escapeHtml(f.transit||"—")}</p></div>
      <div class="mini-card"><h3>出途</h3><p>${escapeHtml(f.exit||"—")}</p></div>
      <div class="mini-card"><h3>追回预期</h3><p>${escapeHtml(f.recoveryOutlook||"—")}</p></div>
    </div>
    <div class="subh">追踪备注</div>
    ${listHtml(f.notes)}
  `;
}
function renderBiz(c){
  const b=c.businessAnalysis||{};
  $("bizPanel").innerHTML = `
    <div class="two-col">
      <div class="mini-card"><h3>运营影响</h3><p>${escapeHtml(b.opsImpact||"—")}</p></div>
      <div class="mini-card"><h3>用户信任</h3><p>${escapeHtml(b.userTrust||"—")}</p></div>
      <div class="mini-card"><h3>偿付 / 覆盖</h3><p>${escapeHtml(b.solvencyCoverage||"—")}</p></div>
      <div class="mini-card"><h3>竞争格局</h3><p>${escapeHtml(b.competitive||"—")}</p></div>
    </div>
  `;
}
function renderIndustry(c){
  const m=c.marketIndustry||{};
  $("industryPanel").innerHTML = `
    <div class="subh">市场反应</div>
    <p>${escapeHtml(m.marketReaction||"—")}</p>
    <div class="subh">行业含义</div>
    ${listHtml(m.industryImplications)}
    <div class="subh">监管信号</div>
    <p>${escapeHtml(m.regulatorySignals||"—")}</p>
    <div class="subh">同业风险提示</div>
    <p>${escapeHtml(m.peerRisk||"—")}</p>
  `;
}

'''

marker = "function setView(view){"
if marker not in text:
    raise SystemExit("setView not found")
text = text.replace(marker, helpers + marker, 1)

p.write_text(text, encoding="utf-8")
print("ui patch ok")
