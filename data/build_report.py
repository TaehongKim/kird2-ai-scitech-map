import json, pathlib, collections, datetime

root = pathlib.Path(r"z:\CS\Common\★ 평가&자문\260521 KIRD 2\outputs")
with open(root / "data" / "case_tech_map.json", encoding="utf-8") as f:
    D = json.load(f)

cases = D["cases"]
techs = {t["id"]: t for t in D["technologies"]}

domain_cases = collections.defaultdict(list)
for c in cases:
    domain_cases[c["domain"]].append(c)

tech_usage = collections.defaultdict(int)
for c in cases:
    for t in c.get("common_techs", []) + c.get("domain_techs", []):
        tech_usage[t] += 1

common_techs = [t for t in D["technologies"] if t["type"] == "common"]
spec_techs = [t for t in D["technologies"] if t["type"] == "specialized"]

DOMAIN_META = {
    "신약개발":    {"icon":"💊","color":"#7c3aed","file":"drug_discovery.html","en":"Drug Discovery"},
    "바이오·의료": {"icon":"🧬","color":"#0891b2","file":"biomedical.html","en":"Biomedical"},
    "소재":        {"icon":"⚗️","color":"#0d9488","file":"materials.html","en":"Materials"},
    "에너지":      {"icon":"⚡","color":"#d97706","file":"energy.html","en":"Energy"},
    "기후·환경":   {"icon":"🌍","color":"#16a34a","file":"climate.html","en":"Climate"},
    "제조":        {"icon":"🏭","color":"#dc2626","file":"manufacturing.html","en":"Manufacturing"},
    "우주·항공":   {"icon":"🚀","color":"#1d4ed8","file":"space.html","en":"Space"},
    "농식품":      {"icon":"🌾","color":"#65a30d","file":"agriculture.html","en":"Agriculture"},
    "수학·기초과학":{"icon":"🔬","color":"#9333ea","file":"math_science.html","en":"Math & Science"},
    "로봇·자율화": {"icon":"🤖","color":"#e11d48","file":"robotics.html","en":"Robotics"},
}
def domain_card(domain):
    m = DOMAIN_META[domain]
    cs = domain_cases[domain]
    overseas = sum(1 for c in cs if c.get("region_type") == "overseas")
    domestic = len(cs) - overseas
    high = sum(1 for c in cs if c.get("importance") == "상")
    all_techs = []
    for c in cs:
        all_techs += c.get("common_techs",[]) + c.get("domain_techs",[])
    top3 = sorted(collections.Counter(all_techs).items(), key=lambda x:-x[1])[:3]
    top_names = ", ".join(techs[t]["name"] for t,_ in top3 if t in techs)
    return f"""
    <div class="domain-card" style="--dc:{m['color']}">
      <div class="dc-top">
        <span class="dc-icon">{m['icon']}</span>
        <div><div class="dc-name">{domain}</div><div class="dc-en">{m['en']}</div></div>
        <a href="domain/{m['file']}" class="dc-link">지식맵 →</a>
      </div>
      <div class="dc-stats">
        <div class="dc-stat"><span class="dc-num">{len(cs)}</span><span class="dc-label">사례</span></div>
        <div class="dc-stat"><span class="dc-num">{overseas}</span><span class="dc-label">해외</span></div>
        <div class="dc-stat"><span class="dc-num">{domestic}</span><span class="dc-label">국내</span></div>
        <div class="dc-stat"><span class="dc-num">{high}</span><span class="dc-label">중요도상</span></div>
      </div>
      <div class="dc-techs">주요 기술: {top_names}</div>
    </div>"""

def tech_rows(tech_list):
    rows = []
    for t in tech_list:
        u = tech_usage.get(t["id"], 0)
        pct = int(u / len(cases) * 100)
        rows.append(f'<tr><td><code>{t["id"]}</code></td><td>{t["name"]}</td>'
                    f'<td>{t.get("category","—")}</td><td>{u}</td>'
                    f'<td><div class="bar-cell"><div class="bar-fill" style="width:{pct}%"></div><span>{pct}%</span></div></td></tr>')
    return "\n".join(rows)

def case_rows():
    rows = []
    for c in cases:
        ct = ", ".join(techs[t]["name"] for t in c.get("common_techs",[]) if t in techs)
        dt = ", ".join(techs[t]["name"] for t in c.get("domain_techs",[]) if t in techs)
        flag = "🌐" if c.get("region_type") == "overseas" else "🇰🇷"
        imp_cls = {"상":"imp-high","중":"imp-mid","하":"imp-low"}.get(c.get("importance","중"),"imp-mid")
        url = c.get("url","")
        nm = f'<a href="{url}" target="_blank">{c["name_ko"]}</a>' if url else c["name_ko"]
        rows.append(f'<tr><td><code>{c["id"]}</code></td><td>{flag} {nm}</td>'
                    f'<td>{c["domain"]}</td><td>{c.get("org","—")}</td>'
                    f'<td>{c.get("year","—")}</td>'
                    f'<td><span class="imp {imp_cls}">{c.get("importance","중")}</span></td>'
                    f'<td class="tech-cell">{ct}</td><td class="tech-cell">{dt}</td></tr>')
    return "\n".join(rows)

domain_cards_html = "\n".join(domain_card(d) for d in DOMAIN_META)
common_chart_data = json.dumps([{"id":t["id"],"name":t["name"],"count":tech_usage.get(t["id"],0)} for t in sorted(common_techs, key=lambda x:-tech_usage.get(x["id"],0))[:10]])
spec_chart_data   = json.dumps([{"id":t["id"],"name":t["name"],"count":tech_usage.get(t["id"],0)} for t in sorted(spec_techs, key=lambda x:-tech_usage.get(x["id"],0))[:10]])
domain_chart_data = json.dumps([{"domain":d,"count":len(cs),"overseas":sum(1 for c in cs if c.get("region_type")=="overseas")} for d,cs in domain_cases.items()])
CSS = """
:root{--bg:#f8fafc;--paper:#fff;--ink:#1e293b;--muted:#64748b;--line:#e2e8f0;--brand:#0f766e;--brand2:#7c3aed;--shadow:0 4px 24px rgba(15,23,42,.08);--r:12px}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{font-family:"Noto Sans KR",system-ui,sans-serif;color:var(--ink);background:var(--bg);line-height:1.8;font-size:15px}
.page-wrap{display:grid;grid-template-columns:240px 1fr;min-height:100vh;max-width:1400px;margin:0 auto}
.sidebar{position:sticky;top:0;height:100vh;overflow-y:auto;padding:24px 16px;background:#fff;border-right:1px solid var(--line);font-size:13px}
.sidebar-logo{font-weight:700;color:var(--brand);font-size:14px;margin-bottom:20px;padding-bottom:12px;border-bottom:1px solid var(--line)}
.toc-section-title{font-weight:700;padding:6px 8px;font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted)}
.toc a{display:block;padding:5px 8px 5px 16px;color:var(--muted);text-decoration:none;border-radius:6px;line-height:1.4;transition:.15s}
.toc a:hover,.toc a.active{background:#f0fdf4;color:var(--brand)}
.toc a.l2{padding-left:28px;font-size:12px}
main{padding:48px 56px 80px;max-width:960px}
.cover{background:linear-gradient(135deg,#0f172a 0%,#1e3a5f 50%,#0f766e 100%);color:#fff;padding:64px 56px;margin:-48px -56px 60px;position:relative;overflow:hidden}
.cover-kird{font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;opacity:.6;margin-bottom:16px}
.cover h1{font-size:2.4rem;font-weight:700;line-height:1.25;margin-bottom:16px}
.cover h1 span{color:#5eead4}.cover-sub{font-size:1.05rem;opacity:.75;margin-bottom:32px;max-width:600px}
.cover-badges{display:flex;flex-wrap:wrap;gap:10px}
.cover-badge{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);border-radius:999px;padding:6px 16px;font-size:13px;font-weight:500}
h2{font-size:1.6rem;font-weight:700;color:#0f172a;margin:56px 0 20px;padding-bottom:12px;border-bottom:2px solid var(--brand);display:flex;align-items:center;gap:10px}
h2 .sec-num{font-size:.85rem;background:var(--brand);color:#fff;border-radius:6px;padding:2px 10px;font-weight:700}
h3{font-size:1.1rem;font-weight:700;color:#0f172a;margin:32px 0 14px}
h3::before{content:'';display:inline-block;width:4px;height:1em;background:var(--brand);border-radius:2px;margin-right:10px;vertical-align:middle}
p{margin-bottom:14px}
.stats-row{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin:24px 0}
.stat-card{background:var(--paper);border-radius:var(--r);padding:20px 22px;box-shadow:var(--shadow);border-top:4px solid var(--brand)}
.stat-card.s2{border-top-color:var(--brand2)}.stat-card.s3{border-top-color:#d97706}.stat-card.s4{border-top-color:#dc2626}
.stat-num{font-size:2.2rem;font-weight:700;color:#0f172a;line-height:1}.stat-label{font-size:12px;color:var(--muted);margin-top:4px}
.domain-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:16px;margin:24px 0}
.domain-card{background:var(--paper);border-radius:var(--r);padding:18px 20px;box-shadow:var(--shadow);border-left:4px solid var(--dc)}
.dc-top{display:flex;align-items:center;gap:12px;margin-bottom:12px}
.dc-icon{font-size:1.8rem;line-height:1}.dc-name{font-weight:700;color:#0f172a;font-size:.95rem}.dc-en{font-size:11px;color:var(--muted)}
.dc-link{margin-left:auto;font-size:12px;color:var(--dc);text-decoration:none;white-space:nowrap;font-weight:600}
.dc-link:hover{text-decoration:underline}
.dc-stats{display:flex;gap:16px;margin-bottom:10px}
.dc-stat{text-align:center}.dc-num{display:block;font-size:1.3rem;font-weight:700;color:var(--dc)}.dc-label{font-size:10px;color:var(--muted)}
.dc-techs{font-size:11px;color:var(--muted);border-top:1px solid var(--line);padding-top:8px}
.chart-wrap{background:var(--paper);border-radius:var(--r);padding:24px;box-shadow:var(--shadow);margin:20px 0}
.chart-title{font-size:.85rem;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;margin-bottom:16px}
.table-wrap{overflow-x:auto;margin:20px 0;border-radius:var(--r);box-shadow:var(--shadow)}
table{width:100%;border-collapse:collapse;background:var(--paper);font-size:13px}
th{background:#f1f5f9;padding:10px 14px;text-align:left;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);white-space:nowrap}
td{padding:9px 14px;border-top:1px solid var(--line);vertical-align:top}
tr:hover td{background:#f8fafc}
code{font-family:"JetBrains Mono",monospace;font-size:11px;background:#f1f5f9;padding:1px 5px;border-radius:3px;color:var(--brand)}
a{color:var(--brand);text-decoration:none}a:hover{text-decoration:underline}
.imp{display:inline-block;padding:2px 8px;border-radius:999px;font-size:11px;font-weight:700}
.imp-high{background:#fef3c7;color:#92400e}.imp-mid{background:#ede9fe;color:#5b21b6}.imp-low{background:#f0fdf4;color:#166534}
.tech-cell{font-size:11px;color:var(--muted);max-width:200px}
.bar-cell{display:flex;align-items:center;gap:8px}
.bar-fill{height:6px;border-radius:3px;background:var(--brand);min-width:2px}
.bar-cell span{font-size:11px;color:var(--muted);white-space:nowrap}
.callout{background:#f0fdf4;border-left:4px solid var(--brand);border-radius:0 var(--r) var(--r) 0;padding:14px 18px;margin:20px 0;font-size:14px}
.callout.warning{background:#fffbeb;border-color:#d97706}.callout.info{background:#eff6ff;border-color:#3b82f6}
.filter-bar{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:14px}
.filter-bar select,.filter-bar input{border:1px solid var(--line);border-radius:8px;padding:6px 12px;font-size:13px;background:#fff;color:var(--ink);font-family:inherit}
.filter-bar input{min-width:220px}
footer{margin-top:80px;padding:32px 0;border-top:1px solid var(--line);text-align:center;font-size:12px;color:var(--muted)}
@media(max-width:900px){.page-wrap{display:block}.sidebar{display:none}main{padding:28px 20px 60px}.stats-row{grid-template-columns:repeat(2,1fr)}.domain-grid{grid-template-columns:1fr}}
"""
SIDEBAR = """
<nav class="sidebar">
  <div class="sidebar-logo">📊 KIRD 2026 보고서</div>
  <div class="toc">
    <div class="toc-section-title">Contents</div>
    <a href="#overview">1. 분석 개요</a>
    <a href="#methodology" class="l2">1.1 목적 및 방법</a>
    <a href="#scope" class="l2">1.2 수집 범위</a>
    <a href="#taxonomy">2. 기술군 분류 체계</a>
    <a href="#common-tech" class="l2">2.1 공통 기술 (IT 범용)</a>
    <a href="#spec-tech" class="l2">2.2 분야 특화 기술</a>
    <a href="#domains">3. 분야별 사례 분석</a>
    <a href="#domain-drug" class="l2">3.1 신약개발</a>
    <a href="#domain-bio" class="l2">3.2 바이오·의료</a>
    <a href="#domain-mat" class="l2">3.3 소재</a>
    <a href="#domain-energy" class="l2">3.4 에너지</a>
    <a href="#domain-climate" class="l2">3.5 기후·환경</a>
    <a href="#domain-mfg" class="l2">3.6 제조</a>
    <a href="#domain-space" class="l2">3.7 우주·항공</a>
    <a href="#domain-agri" class="l2">3.8 농식품</a>
    <a href="#domain-math" class="l2">3.9 수학·기초과학</a>
    <a href="#domain-robot" class="l2">3.10 로봇·자율화</a>
    <a href="#tech-analysis">4. 기술군 활용 분석</a>
    <a href="#global-compare">5. 국내외 비교</a>
    <a href="#visualization">6. 시각화 안내</a>
    <a href="#insights">7. 시사점 및 결론</a>
    <a href="#cases-appendix">부록. 전체 사례 목록</a>
  </div>
</nav>"""

JS = """
<script src="https://d3js.org/d3.v7.min.js"></script>
<script>
const BRAND="#0f766e",BRAND2="#7c3aed";
function barChart(id,data,color){
  const el=document.getElementById(id);
  const W=el.parentElement.clientWidth-48,H=280;
  const m={top:10,right:180,bottom:10,left:10};
  const w=W-m.left-m.right,h=H-m.top-m.bottom;
  const svg=d3.select("#"+id).attr("width",W).attr("height",H)
    .append("g").attr("transform",`translate(${m.left},${m.top})`);
  const x=d3.scaleLinear().domain([0,d3.max(data,d=>d.count)]).range([0,w]);
  const y=d3.scaleBand().domain(data.map(d=>d.name)).range([0,h]).padding(.25);
  svg.selectAll("rect").data(data).join("rect")
    .attr("y",d=>y(d.name)).attr("height",y.bandwidth())
    .attr("x",0).attr("width",d=>x(d.count))
    .attr("rx",3).attr("fill",color).attr("opacity",.85);
  svg.selectAll(".lbl").data(data).join("text").attr("class","lbl")
    .attr("y",d=>y(d.name)+y.bandwidth()/2+4)
    .attr("x",d=>x(d.count)+8)
    .attr("fill","#334155").attr("font-size","12px")
    .attr("font-family","'Noto Sans KR',sans-serif")
    .text(d=>d.name+" ("+d.count+")");
}
barChart("chart-common",COMMON_DATA,BRAND);
barChart("chart-spec",SPEC_DATA,BRAND2);
(function(){
  const data=DOMAIN_DATA;
  const el=document.getElementById("chart-domain");
  const W=el.parentElement.clientWidth-48,H=320;
  const m={top:20,right:20,bottom:65,left:30};
  const w=W-m.left-m.right,h=H-m.top-m.bottom;
  const svg=d3.select("#chart-domain").attr("width",W).attr("height",H)
    .append("g").attr("transform",`translate(${m.left},${m.top})`);
  const x0=d3.scaleBand().domain(data.map(d=>d.domain)).range([0,w]).padding(.2);
  const x1=d3.scaleBand().domain(["해외","국내"]).range([0,x0.bandwidth()]).padding(.05);
  const y=d3.scaleLinear().domain([0,d3.max(data,d=>d.count)+2]).range([h,0]);
  svg.append("g").call(d3.axisLeft(y).ticks(5).tickSize(-w))
    .call(g=>g.selectAll(".tick line").attr("stroke","#e2e8f0"))
    .call(g=>g.select(".domain").remove());
  const grp=svg.selectAll(".grp").data(data).join("g").attr("class","grp")
    .attr("transform",d=>`translate(${x0(d.domain)},0)`);
  grp.append("rect").attr("x",x1("해외")).attr("y",d=>y(d.overseas))
    .attr("width",x1.bandwidth()).attr("height",d=>h-y(d.overseas))
    .attr("fill",BRAND).attr("rx",2);
  grp.append("rect").attr("x",x1("국내")).attr("y",d=>y(d.count-d.overseas))
    .attr("width",x1.bandwidth()).attr("height",d=>h-y(d.count-d.overseas))
    .attr("fill",BRAND2).attr("rx",2);
  grp.append("text").attr("x",x0.bandwidth()/2).attr("y",d=>y(d.count)-5)
    .attr("text-anchor","middle").attr("font-size","11px")
    .attr("fill","#64748b").attr("font-family","'Noto Sans KR',sans-serif")
    .text(d=>d.count);
  svg.append("g").attr("transform",`translate(0,${h})`)
    .call(d3.axisBottom(x0).tickSize(0))
    .call(g=>g.select(".domain").remove())
    .selectAll("text").attr("transform","rotate(-30)").attr("text-anchor","end")
    .attr("font-size","11px").attr("font-family","'Noto Sans KR',sans-serif");
  const leg=svg.append("g").attr("transform",`translate(${w-110},-10)`);
  [["해외",BRAND],["국내",BRAND2]].forEach(([l,c],i)=>{
    leg.append("rect").attr("x",i*56).attr("width",10).attr("height",10).attr("fill",c).attr("rx",2);
    leg.append("text").attr("x",i*56+14).attr("y",9).attr("font-size","11px")
      .attr("fill","#64748b").attr("font-family","'Noto Sans KR',sans-serif").text(l);
  });
})();
function filterTable(){
  const q=document.getElementById("si").value.toLowerCase();
  const dom=document.getElementById("df").value;
  const reg=document.getElementById("rf").value;
  const imp=document.getElementById("if").value;
  document.querySelectorAll("#case-tbody tr").forEach(tr=>{
    const txt=tr.textContent.toLowerCase();
    const cells=tr.querySelectorAll("td");
    const d=cells[2]?.textContent.trim()||"";
    const r=tr.querySelector("td:nth-child(2)")?.textContent.includes("🌐")?"overseas":"domestic";
    const im=tr.querySelector(".imp")?.textContent||"";
    tr.style.display=(!q||txt.includes(q))&&(!dom||d===dom)&&(!reg||r===reg)&&(!imp||im===imp)?"":"none";
  });
}
["si","df","rf","if"].forEach(id=>{
  const el=document.getElementById(id);
  if(el)el.addEventListener(id==="si"?"input":"change",filterTable);
});
const secs=document.querySelectorAll("h2[id],h3[id]");
const lnks=document.querySelectorAll(".toc a");
new IntersectionObserver(es=>{
  es.forEach(e=>{if(e.isIntersecting)lnks.forEach(l=>l.classList.toggle("active",l.getAttribute("href")==="#"+e.target.id));});
},{rootMargin:"-20% 0px -70% 0px"}).observe;
secs.forEach(s=>new IntersectionObserver(es=>{
  es.forEach(e=>{if(e.isIntersecting)lnks.forEach(l=>l.classList.toggle("active",l.getAttribute("href")==="#"+e.target.id));});
},{rootMargin:"-20% 0px -70% 0px"}).observe(s));
</script>"""
def domain_summary(did, domain, text, highlight):
    cnt = len(domain_cases[domain])
    return f"""
<h3 id="{did}">{DOMAIN_META[domain]['icon']} 3.{list(DOMAIN_META.keys()).index(domain)+1} {domain} ({cnt}건)</h3>
<p>{text}</p>
<div class="callout"><strong>대표 성과:</strong> {highlight}</div>"""

DOMAIN_SUMMARIES = [
("domain-drug","신약개발",
 "AlphaFold2를 기점으로 단백질 구조 예측 문제가 사실상 해결되면서 de novo 약물 설계·약물-표적 상호작용 예측 AI가 폭발적으로 성장하였다. 2023년에는 생성형 AI가 설계한 약물(Insilico Medicine)이 세계 최초로 임상 2상에 진입하였고, RFdiffusion은 확산 모델 기반 단백질 설계를 실현하였다.",
 "AlphaFold2 — CASP14 1위·2억개+ 구조 공개 / Insilico Medicine — 생성형 AI 신약 세계 최초 임상 2상 / MIT Halicin — 항생제 내성균 치료제 발굴"),
("domain-bio","바이오·의료",
 "의료영상 AI 진단이 FDA 승인을 받으며 임상 현장에 본격 진입하였다. Med-PaLM 2가 MedQA 86.5% 정확도로 전문의 수준을 최초 달성하였고, CONCH·UNI 등 계산 병리학 파운데이션 모델이 등장하였다.",
 "IDx-DR — 세계 최초 자율 AI 진단 FDA 승인 / Paige Prostate — 병리의사 오류 70% 감소 / Med-PaLM 2 — 전문의 수준(MedQA 86.5%)"),
("domain-mat","소재",
 "GNN 기반 소재 발굴이 DFT 대비 수천~수백만 배 빠른 탐색을 가능하게 하였다. GNoME(DeepMind)은 38만 1천 개 안정 소재를 단번에 발굴하였고, A-Lab이 17일 자율 합성 실험실 가능성을 입증하였다. Microsoft MatterGen은 확산 모델로 원하는 특성의 소재를 역설계하는 최초 사례를 제시하였다.",
 "GNoME — 38만 1천개 안정 소재(Nature) / A-Lab — 17일 자율 합성 63% 성공 / MatterGen — 생성형 AI 신소재 역설계(Nature 2025)"),
("domain-energy","에너지",
 "DeepMind 토카막 플라즈마 자기 제어(Nature 2022)가 핵융합 상용화 핵심 장벽을 돌파하였다. 구글 데이터센터 냉각 AI가 완전 자율 제어로 냉각 에너지 40%를 절감하였고, 재생에너지 발전량 예측 AI가 전력망 안정성을 향상시켰다.",
 "DeepMind TCV — 토카막 플라즈마 안정 유지(Nature) / DC 냉각 자율 제어 — 냉각 에너지 40% 절감 / 한국중부발전 — 태양광 99% 정확도(국내 최초)"),
("domain-climate","기후·환경",
 "AI 기상 예측 모델(GraphCast·FourCastNet·Pangu-Weather)이 기존 수치예보 슈퍼컴퓨터를 수만~수십만 배 앞서는 추론 속도를 달성하였다. 자연재해 조기경보 AI가 80개국 이상에 배포되었다.",
 "GraphCast — 10일 예측 45초(Science) / FourCastNet — NWP 대비 80,000배 빠른 추론 / Google Flood Hub — 80개국+ 460만 명 최대 7일 전 홍수 예측"),
("domain-mfg","제조",
 "AI가 반도체 플로어플래닝·웨이퍼 결함 탐지·디지털 트윈 기반 공장 설계에 실용화 단계로 진입하였다. DeepMind AlphaChip은 Trillium TPU 설계에 적용되었고, BMW×NVIDIA는 세계 최초 완전 가상 검증 후 공장 건설을 실현하였다.",
 "AlphaChip — 반도체 플로어플래닝 자동화 / BMW×NVIDIA — 완전 가상 검증 공장 / SK하이닉스 Panoptes VM — 처리 시간 50%+ 단축"),
("domain-space","우주·항공",
 "NASA 퍼서비어런스 로버가 AI 자율 계획으로 화성 자율 주행을 완료하였고, ESA는 세계 최초 AI 탑재 지구관측위성(PhiSat)을 발사하였다. SpaceX Starlink는 25,000회 이상 자율 충돌 회피를 수행하였다.",
 "NASA Perseverance — 화성 자율 주행 완료 / ESA PhiSat — 세계 최초 AI 탑재 위성 / SpaceX Starlink — 25,000회+ 자율 충돌 회피"),
("domain-agri","농식품",
 "정밀 AI 제초 로봇(See &amp; Spray)이 농약 사용을 대폭 절감하였고, 국내 농촌진흥청 AI 병해충 진단이 31개 작물 182개 병해충을 99.4% 정확도로 진단한다. Bayer Xarvio는 130개국 5천만 헥타르에 디지털 작물 관리 AI를 제공하고 있다.",
 "John Deere See &amp; Spray — 정밀 AI 제초 / Xarvio — 130개국 5천만 헥타르 / 농촌진흥청 — 31작물 99.4% 정확도"),
("domain-math","수학·기초과학",
 "DeepMind AlphaProof가 2024년 IMO에서 은메달 수준(28/42점)을 달성하였다. AlphaTensor는 50년 이상 불변이던 행렬 곱셈 알고리즘을 경신하고, FunSearch는 수학 미해결 문제의 20년 기록을 경신하였다.",
 "AlphaProof — IMO 은메달급(2024) / AlphaTensor — 행렬 곱셈 알고리즘 50년 기록 경신 / Meta Lean Copilot — LLM 기반 형식 증명 보조"),
("domain-robot","로봇·자율화",
 "CMU Coscientist가 LLM 기반 자율 화학 실험 로봇을 구현(Nature 2023)하였고, Google DeepMind RT-2가 웹 데이터로 학습한 범용 비전-언어-행동 모델로 새 지시에 62% 성공률을 달성하였다. Boston Dynamics Atlas는 코딩 없이 새 기능 추가 가능한 범용 휴머노이드로 발전하였다.",
 "CMU Coscientist — 자율 화학 실험(Nature 2023) / RT-2 — VLA 모델 새 지시 62% 성공(Science Robotics 2023) / KAIST KAIROS — 통합 무인공장"),
]
domain_summaries_html = "\n".join(domain_summary(*args) for args in DOMAIN_SUMMARIES)
def build_html():
    n_drug=len(domain_cases["신약개발"])
    n_bio=len(domain_cases["바이오·의료"])
    n_mat=len(domain_cases["소재"])
    n_ene=len(domain_cases["에너지"])
    n_cli=len(domain_cases["기후·환경"])
    n_mfg=len(domain_cases["제조"])
    n_spc=len(domain_cases["우주·항공"])
    n_agr=len(domain_cases["농식품"])
    n_mth=len(domain_cases["수학·기초과학"])
    n_rob=len(domain_cases["로봇·자율화"])
    js2 = JS.replace("COMMON_DATA", common_chart_data).replace("SPEC_DATA", spec_chart_data).replace("DOMAIN_DATA", domain_chart_data)
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI 과학기술 혁신 사례 기술군 매핑 분석 보고서 — KIRD 2026</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<div class="page-wrap">
{SIDEBAR}
<main>
<div class="cover">
  <div class="cover-kird">KIRD · AI 과학기술 혁신 사례 분석</div>
  <h1>AI 과학기술 혁신 사례<br><span>기술군 매핑 분석 보고서</span></h1>
  <div class="cover-sub">AI 활용 과학기술 혁신 사례 100건의 체계적 수집·분석 및 공통·분야특화 기술군 매핑 결과</div>
  <div class="cover-badges">
    <span class="cover-badge">📅 2026년 6월</span>
    <span class="cover-badge">📋 총 100건 사례</span>
    <span class="cover-badge">🌐 해외 80건 · 국내 20건</span>
    <span class="cover-badge">🔬 10개 과학기술 분야</span>
    <span class="cover-badge">⚙️ 70종 기술군</span>
  </div>
</div>

<h2 id="overview"><span class="sec-num">1</span> 분석 개요</h2>
<h3 id="methodology">1.1 목적 및 방법론</h3>
<p>본 분석은 AI 기술을 활용하여 과학기술을 혁신한 국내외 사례를 체계적으로 수집·분류하고, 각 사례에 필요한 기술군을 <strong>공통 기술(IT 범용)</strong>과 <strong>분야 특화 기술(도메인 의존)</strong>로 분류한 후 D3.js 기반 인터랙티브 시각화 지식맵을 구축하는 것을 목표로 한다.</p>
<div class="callout"><strong>수집 방법:</strong> Claude AI 다중 에이전트가 10개 과학기술 분야를 병렬 탐색하여 국내외 사례를 자동 수집. 각 사례에 출처 URL·성과 수치·활용 기술을 명시하고, 중복 제거 후 최종 100건을 확정하였다.</div>

<h3 id="scope">1.2 분석 범위</h3>
<div class="stats-row">
  <div class="stat-card"><div class="stat-num">100</div><div class="stat-label">총 수집 사례</div></div>
  <div class="stat-card s2"><div class="stat-num">80</div><div class="stat-label">해외 사례</div></div>
  <div class="stat-card s3"><div class="stat-num">20</div><div class="stat-label">국내 사례</div></div>
  <div class="stat-card s4"><div class="stat-num">70</div><div class="stat-label">기술군 (공통20+특화50)</div></div>
</div>

<h2 id="taxonomy"><span class="sec-num">2</span> 기술군 분류 체계</h2>
<p>기술군 분류는 <strong>도메인 지식 의존성</strong>을 핵심 기준으로 한다. 특정 과학기술 도메인 지식 없이 여러 분야에 활용 가능한 IT 기반 AI 기술은 <em>공통 기술</em>로, 해당 도메인 지식과 결합해야만 의미 있는 결과를 낼 수 있는 기술은 <em>분야 특화 기술</em>로 분류한다.</p>
<div class="callout info"><strong>예외 규칙:</strong> 특정 분야에만 최적화된 IT 기술도 특화 기술로 분류. 예: 단백질 구조 예측 GNN(신약개발 특화), 기후 수치 모델링(기후·환경 특화)</div>

<h3 id="common-tech">2.1 공통 기술군 (IT 범용, T01–T20)</h3>
<div class="chart-wrap"><div class="chart-title">공통 기술 활용 빈도 Top 10 (전체 100건 대비)</div><svg id="chart-common" height="280"></svg></div>
<div class="table-wrap"><table><thead><tr><th>ID</th><th>기술명</th><th>분류</th><th>활용</th><th>활용률</th></tr></thead><tbody>
{tech_rows(common_techs)}
</tbody></table></div>

<h3 id="spec-tech">2.2 분야 특화 기술군 (T21–T70)</h3>
<div class="chart-wrap"><div class="chart-title">분야 특화 기술 활용 빈도 Top 10</div><svg id="chart-spec" height="280"></svg></div>
<div class="table-wrap"><table><thead><tr><th>ID</th><th>기술명</th><th>분류</th><th>활용</th><th>활용률</th></tr></thead><tbody>
{tech_rows(spec_techs)}
</tbody></table></div>

<h2 id="domains"><span class="sec-num">3</span> 분야별 사례 분석</h2>
<div class="chart-wrap"><div class="chart-title">분야별 수집 사례 수 (해외/국내 구분)</div><svg id="chart-domain" height="320"></svg></div>
<div class="domain-grid">
{domain_cards_html}
</div>
{domain_summaries_html}

<h2 id="tech-analysis"><span class="sec-num">4</span> 기술군 활용 분석</h2>
<h3>4.1 전 분야 공통 기술 Top 5</h3>
<div class="table-wrap"><table><thead><tr><th>순위</th><th>기술</th><th>활용 건수</th><th>주요 적용 분야</th></tr></thead><tbody>
<tr><td>1</td><td>딥러닝 (T01)</td><td>100건 전체</td><td>전 분야</td></tr>
<tr><td>2</td><td>머신러닝 (T02)</td><td>48건</td><td>소재·에너지·제조·농식품</td></tr>
<tr><td>3</td><td>컴퓨터 비전 (T06)</td><td>40건</td><td>바이오·의료·제조·우주·항공·농식품</td></tr>
<tr><td>4</td><td>그래프 신경망 (T05)</td><td>22건</td><td>신약개발·소재·기후·환경</td></tr>
<tr><td>5</td><td>생성형 AI (T08)</td><td>20건</td><td>신약개발·소재·로봇·자율화</td></tr>
</tbody></table></div>
<h3>4.2 주요 기술 조합 패턴</h3>
<div class="table-wrap"><table><thead><tr><th>기술 조합</th><th>주요 적용 사례</th></tr></thead><tbody>
<tr><td>딥러닝 + 컴퓨터 비전</td><td>의료영상 진단, 위성 영상 분석, 반도체 결함 탐지</td></tr>
<tr><td>강화학습 + 딥러닝</td><td>핵융합 플라즈마 제어, 자율 로봇, DC 냉각 자율 제어</td></tr>
<tr><td>그래프 신경망 + 머신러닝</td><td>소재 발굴, 약물-표적 예측, 기상 예측</td></tr>
<tr><td>LLM + 생성형 AI</td><td>신약 설계, 자율 실험 로봇, 수학 증명 보조</td></tr>
<tr><td>확산 모델 + 딥러닝</td><td>단백질 설계, 신소재 역설계, 이미지 기반 진단</td></tr>
<tr><td>파운데이션 모델 + 멀티모달 AI</td><td>범용 로봇 제어, 의료 전문 LLM, 과학 이해 AI</td></tr>
</tbody></table></div>

<h2 id="global-compare"><span class="sec-num">5</span> 국내외 비교 분석</h2>
<h3>5.1 해외 주요 기관</h3>
<div class="table-wrap"><table><thead><tr><th>기관</th><th>사례 수</th><th>주요 분야</th></tr></thead><tbody>
<tr><td>Google DeepMind</td><td>12건+</td><td>신약·소재·기후·에너지·수학·로봇</td></tr>
<tr><td>NASA / JPL</td><td>3건</td><td>우주·항공</td></tr>
<tr><td>Meta AI</td><td>3건</td><td>소재·기후·수학</td></tr>
<tr><td>Microsoft Research</td><td>3건</td><td>소재·제조·기후</td></tr>
<tr><td>NVIDIA</td><td>3건</td><td>기후·제조</td></tr>
<tr><td>ESA</td><td>3건</td><td>우주·항공</td></tr>
</tbody></table></div>
<h3>5.2 국내 현황</h3>
<div class="table-wrap"><table><thead><tr><th>기관</th><th>대표 사례</th><th>분야</th></tr></thead><tbody>
<tr><td>SK하이닉스</td><td>Panoptes VM, 자율형 팹</td><td>제조</td></tr>
<tr><td>현대자동차그룹</td><td>Atlas 휴머노이드, HMGICS</td><td>로봇·제조</td></tr>
<tr><td>KAIST</td><td>KAIROS, 신약 플랫폼</td><td>로봇·신약</td></tr>
<tr><td>농촌진흥청</td><td>AI 병해충 진단(31작물, 99.4%)</td><td>농식품</td></tr>
<tr><td>삼성전자</td><td>AI 반도체 결함 탐지</td><td>제조</td></tr>
<tr><td>한국중부발전/GS E&amp;R</td><td>재생에너지 예측(태양광 99%)</td><td>에너지</td></tr>
</tbody></table></div>

<h2 id="visualization"><span class="sec-num">6</span> 시각화 결과물 안내</h2>
<p>본 분석은 D3.js v7 기반 인터랙티브 시각화를 함께 제공한다.</p>
<div class="table-wrap"><table><thead><tr><th>파일</th><th>설명</th></tr></thead><tbody>
<tr><td><a href="index.html">index.html</a></td><td>종합 지식맵 — 개요 대시보드 · 포스 네트워크 · 매트릭스 · 사례 목록 · 분야별 링크</td></tr>
<tr><td><a href="domain/drug_discovery.html">신약개발</a></td><td>{n_drug}건 사례 · D3.js 역량 네트워크 · 기술 분류 차트</td></tr>
<tr><td><a href="domain/biomedical.html">바이오·의료</a></td><td>{n_bio}건 사례 · D3.js 역량 네트워크 · 기술 분류 차트</td></tr>
<tr><td><a href="domain/materials.html">소재</a></td><td>{n_mat}건 사례 · D3.js 역량 네트워크 · 기술 분류 차트</td></tr>
<tr><td><a href="domain/energy.html">에너지</a></td><td>{n_ene}건 사례 · D3.js 역량 네트워크 · 기술 분류 차트</td></tr>
<tr><td><a href="domain/climate.html">기후·환경</a></td><td>{n_cli}건 사례 · D3.js 역량 네트워크 · 기술 분류 차트</td></tr>
<tr><td><a href="domain/manufacturing.html">제조</a></td><td>{n_mfg}건 사례 · D3.js 역량 네트워크 · 기술 분류 차트</td></tr>
<tr><td><a href="domain/space.html">우주·항공</a></td><td>{n_spc}건 사례 · D3.js 역량 네트워크 · 기술 분류 차트</td></tr>
<tr><td><a href="domain/agriculture.html">농식품</a></td><td>{n_agr}건 사례 · D3.js 역량 네트워크 · 기술 분류 차트</td></tr>
<tr><td><a href="domain/math_science.html">수학·기초과학</a></td><td>{n_mth}건 사례 · D3.js 역량 네트워크 · 기술 분류 차트</td></tr>
<tr><td><a href="domain/robotics.html">로봇·자율화</a></td><td>{n_rob}건 사례 · D3.js 역량 네트워크 · 기술 분류 차트</td></tr>
</tbody></table></div>

<h2 id="insights"><span class="sec-num">7</span> 주요 시사점 및 결론</h2>
<h3>7.1 공통 기술의 범용성과 한계</h3>
<p>딥러닝은 100건 전체에서 활용되는 가장 범용적인 공통 기술이다. 그러나 딥러닝 단독으로 성과를 내는 사례는 드물며, 대부분 <strong>공통 기술 + 도메인 특화 알고리즘</strong>의 결합으로 최대 성과가 창출된다. 그래프 신경망(GNN)은 과학 데이터의 복잡한 관계 구조(분자·격자·기상)를 표현하는 데 특히 강력하여 '과학 AI의 핵심 엔진'으로 부상하였다.</p>
<h3>7.2 생성형 AI와 파운데이션 모델의 부상</h3>
<p>2022~2024년 사이 생성형 AI(확산 모델·LLM)가 신약 설계·소재 발굴·자율 실험 등에 본격 적용되었다. 기존 예측·분류 AI를 넘어 '창조적 AI'로 발전하면서 과학적 발견의 속도와 범위가 획기적으로 확대되었다.</p>
<h3>7.3 자율 과학 실험의 도래</h3>
<p>CMU Coscientist(화학 자율 실험)·A-Lab(자율 소재 합성)·NASA 퍼서비어런스(자율 화성 탐사)는 AI가 인간 개입 없이 실험을 설계·실행하는 '완전 자율 과학'이 현실화되고 있음을 보여준다.</p>
<h3>7.4 AI 성숙도별 분야</h3>
<div class="table-wrap"><table><thead><tr><th>성숙 단계</th><th>분야</th><th>특징</th></tr></thead><tbody>
<tr><td><strong>상용화·임상</strong></td><td>바이오·의료, 제조, 농식품</td><td>FDA 승인, 양산 팹 적용, 130개국 서비스</td></tr>
<tr><td><strong>대형 연구 성과</strong></td><td>신약개발, 소재, 기후, 수학</td><td>Nature·Science 게재, 기록 경신</td></tr>
<tr><td><strong>자율화·통합</strong></td><td>로봇·자율화, 우주·항공</td><td>VLA 모델, 자율 탐사</td></tr>
<tr><td><strong>에너지 전환 과도기</strong></td><td>에너지</td><td>핵융합·재생에너지 AI 병행 발전</td></tr>
</tbody></table></div>
<div class="callout warning"><strong>국내 강점:</strong> 반도체 제조 AI·휴머노이드 로봇·농업 AI — 상용화·산업화에서 경쟁력 보유<br><br><strong>보완 필요:</strong> 기초과학 AI(수학·물리 원천 연구)·기후·환경 AI·생성형 AI 신약 개발 — 해외 선도기관 대비 격차 존재</div>

<h2 id="cases-appendix"><span class="sec-num">부록</span> 전체 사례 목록 (100건)</h2>
<div class="filter-bar">
  <input type="text" id="si" placeholder="사례명·기관·분야 검색...">
  <select id="df"><option value="">전체 분야</option>
    <option>신약개발</option><option>바이오·의료</option><option>소재</option>
    <option>에너지</option><option>기후·환경</option><option>제조</option>
    <option>우주·항공</option><option>농식품</option><option>수학·기초과학</option><option>로봇·자율화</option>
  </select>
  <select id="rf"><option value="">전체 지역</option><option value="overseas">해외</option><option value="domestic">국내</option></select>
  <select id="if"><option value="">전체 중요도</option><option value="상">상</option><option value="중">중</option><option value="하">하</option></select>
</div>
<div class="table-wrap"><table id="case-table">
<thead><tr><th>ID</th><th>사례명</th><th>분야</th><th>기관</th><th>연도</th><th>중요도</th><th>공통 기술</th><th>특화 기술</th></tr></thead>
<tbody id="case-tbody">
{case_rows()}
</tbody></table></div>
<footer><p>AI 과학기술 혁신 사례 기술군 매핑 분석 보고서 · KIRD 한국연구인재개발원 · 2026년 6월</p>
<p style="margin-top:6px">Generated with Claude AI (Anthropic) — <a href="index.html">종합 지식맵 보기</a></p></footer>
</main></div>
{js2}
</body></html>"""

html = build_html()
out = root / "report.html"
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
sz = out.stat().st_size
print(f"Written: {out}")
print(f"Size: {sz:,} bytes ({sz//1024} KB)")