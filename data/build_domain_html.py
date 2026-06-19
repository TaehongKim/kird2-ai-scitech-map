import json, pathlib, html as H

BASE = pathlib.Path(r"z:\CS\Common\★ 평가&자문\260521 KIRD 2\outputs")
with open(BASE/"data"/"case_tech_map.json", encoding="utf-8") as f:
    DATA = json.load(f)
TM = {t["id"]:t for t in DATA["technologies"]}

META = {
"신약개발":{"file":"drug_discovery.html","icon":"💊","color":"#6c63ff","en":"Drug Discovery","desc":"단백질 구조 예측·de novo 약물 설계·약물-표적 상호작용 예측으로 신약 개발 기간과 비용을 획기적으로 단축","key":"AlphaFold2, 생성형 AI, GNN"},
"바이오·의료":{"file":"biomedical.html","icon":"🏥","color":"#00c6ff","en":"Biomedical","desc":"의료영상 AI 진단·유전체 분석·임상 의사결정 지원으로 의료 정확도와 접근성 향상","key":"컴퓨터 비전, LLM, 파운데이션 모델"},
"소재":{"file":"materials.html","icon":"⚗️","color":"#f7971e","en":"Materials","desc":"GNN·머신러닝으로 배터리 소재·초전도체·촉매를 발굴하고 자율 합성 실험 로봇으로 탐색 가속","key":"GNoME, GNN, 자율실험 AI"},
"에너지":{"file":"energy.html","icon":"⚡","color":"#4dd0e1","en":"Energy","desc":"핵융합 플라즈마 제어·재생에너지 발전량 예측·차세대 배터리·촉매 소재 발굴로 에너지 전환 가속","key":"강화학습, 시계열 예측, GNN"},
"기후·환경":{"file":"climate.html","icon":"🌍","color":"#81c784","en":"Climate","desc":"AI 기상 예측·홍수·산불 조기경보·탄소 포집 소재 발굴·해양 탄소 모니터링으로 기후위기 대응","key":"GraphCast, Flood Hub, NeuralGCM"},
"제조":{"file":"manufacturing.html","icon":"🏭","color":"#ffb74d","en":"Manufacturing","desc":"디지털 트윈·AI 칩 설계 자동화·반도체 결함 탐지·예측 정비로 스마트 팩토리 구현","key":"AlphaChip, 디지털 트윈, 컴퓨터 비전"},
"우주·항공":{"file":"space.html","icon":"🚀","color":"#f06292","en":"Space","desc":"화성 자율 탐사·AI 탑재 위성·우주 잔해물 추적·자율 충돌 회피로 항공우주 AI 자율화","key":"자율 탐사, 위성 영상 AI, SpaceX"},
"농식품":{"file":"agriculture.html","icon":"🌾","color":"#4fc3f7","en":"Agriculture","desc":"AI 병해충 탐지·정밀 제초·수확량 예측·토양 분석으로 식량 안보와 지속가능 농업 실현","key":"See&Spray, 드론 AI, ML 예측"},
"수학·기초과학":{"file":"math_science.html","icon":"🔢","color":"#e57373","en":"Math & Science","desc":"AI 수학 정리 증명·알고리즘 발견·입자물리 데이터 분석·천문 이미지 분석으로 기초과학 패러다임 전환","key":"AlphaProof, FunSearch, AlphaTensor"},
"로봇·자율화":{"file":"robotics.html","icon":"🤖","color":"#ba68c8","en":"Robotics","desc":"LLM 기반 자율 실험 로봇·산업용 휴머노이드·자율주행 판단 AI·이기종 로봇 통합으로 자율화 최전선","key":"Coscientist, Atlas, KAIST KAIROS"},
}

domain_dir = BASE/"domain"
domain_dir.mkdir(exist_ok=True)

def make_html(domain, meta, cases):
    col = meta["color"]; icon = meta["icon"]; en = meta["en"]
    uc,us = {},{}
    for c in cases:
        for t in (c.get("common_techs") or []):
            uc[t] = uc.get(t,{"name":TM[t]["name"],"n":0}); uc[t]["n"]+=1
        for t in (c.get("domain_techs") or []):
            if t in TM: us[t] = us.get(t,{"name":TM[t]["name"],"n":0}); us[t]["n"]+=1
    cs_ = sorted(uc.items(),key=lambda x:-x[1]["n"]); ss_ = sorted(us.items(),key=lambda x:-x[1]["n"])
    top6 = sorted(cases,key=lambda c:{"상":0,"중":1,"하":2}.get(c.get("importance","중"),1))[:6]
    
    def bar(items, col2):
        mx = items[0][1]["n"] if items else 1
        return "".join(f'<div class="br"><div class="bl">{H.escape(v["name"])}</div><div class="bt"><div class="bf" style="width:{int(v["n"]/mx*100)}%;background:{col2}"></div></div><span class="bv">{v["n"]}</span></div>' for _,v in items[:8])

    def cards():
        out=""
        for c in top6:
            ic = {"상":"#ff7043","중":"#f7971e","하":"#9fa8da"}.get(c.get("importance","중"),"#9fa8da")
            out+=f'<div class="cc"><div class="ch"><span style="background:{ic}22;color:{ic};border:1px solid {ic}55;border-radius:4px;padding:2px 7px;font-size:0.7rem;font-weight:700">{c.get("importance","중")}</span><span style="font-size:0.7rem;color:var(--t2)">{c.get("year","")}</span></div><div style="font-size:0.82rem;font-weight:600;margin:4px 0"><a href="{c.get("url","#")}" target="_blank" style="color:var(--txt);text-decoration:none">{H.escape(c.get("name_ko",""))}</a></div><div style="font-size:0.75rem;color:var(--t2);margin-bottom:4px">{H.escape(c.get("org",""))}</div><div style="font-size:0.74rem;color:var(--t2);line-height:1.4">{H.escape(c.get("outcome","")[:90])}{"…" if len(c.get("outcome",""))>90 else ""}</div></div>'
        return out

    def rows():
        out=""
        for c in sorted(cases,key=lambda x:{"상":0,"중":1,"하":2}.get(x.get("importance","중"),1)):
            cmn="".join(f'<span class="tc">{H.escape(TM[t]["name"])}</span>' for t in (c.get("common_techs") or []) if t in TM)
            spc="".join(f'<span class="ts">{H.escape(TM[t]["name"])}</span>' for t in (c.get("domain_techs") or []) if t in TM)
            ic={"상":"#ff7043","중":"#f7971e","하":"#9fa8da"}.get(c.get("importance","중"),"#9fa8da")
            rt="해외" if c.get("region_type")=="overseas" else "국내"
            out+=f'<tr><td><a href="{c.get("url","#")}" target="_blank" style="color:#00c6ff;text-decoration:none">{H.escape(c.get("name_ko",""))}</a></td><td style="font-size:0.78rem">{H.escape(c.get("org",""))}</td><td style="font-size:0.78rem;color:{"#00c6ff" if c.get("region_type")=="overseas" else "#81c784"}">{rt}</td><td>{cmn}</td><td>{spc}</td><td style="font-size:0.78rem">{c.get("year","")}</td><td style="color:{ic};font-weight:700">{c.get("importance","중")}</td></tr>'
        return out

    nj = json.dumps([{"id":c["id"],"name":c["name_ko"][:18],"type":"case","region":c.get("region_type","overseas")} for c in cases]+[{"id":t,"name":TM[t]["name"],"type":"tech","tt":TM[t]["type"]} for t in set(tid for c in cases for tid in [*(c.get("common_techs") or []),*(c.get("domain_techs") or [])]) if t in TM], ensure_ascii=False)
    lj = json.dumps([{"source":c["id"],"target":tid,"tt":TM[tid]["type"]} for c in cases for tid in [*(c.get("common_techs") or []),*(c.get("domain_techs") or [])] if tid in TM], ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI 지식맵 - {domain}</title>
<script src="https://d3js.org/d3.v7.min.js"></script>
<style>
:root{{--bg:#0f1117;--sf:#1a1d2e;--sf2:#252840;--ac:{col};--cm:#4dd0e1;--sp:#f06292;--txt:#e8eaf6;--t2:#9fa8da;--bd:#2d3154}}
*{{box-sizing:border-box;margin:0;padding:0}}body{{background:var(--bg);color:var(--txt);font-family:'Segoe UI','Malgun Gothic',sans-serif}}
.nav{{background:var(--sf);border-bottom:1px solid var(--bd);padding:10px 24px;display:flex;align-items:center;gap:10px}}
.nav a{{color:var(--t2);text-decoration:none;font-size:0.82rem}}.nav a:hover{{color:var(--ac)}}
.hero{{background:linear-gradient(135deg,{col}22 0%,#0f1117 60%);border-bottom:1px solid var(--bd);padding:24px 32px}}
.hero h1{{font-size:1.5rem;font-weight:700}}.hero h1 span{{color:var(--ac)}}
.hero-sub{{font-size:0.84rem;color:var(--t2);margin-top:6px;max-width:700px;line-height:1.6}}
.badges{{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}}
.badge{{background:var(--sf2);border:1px solid var(--bd);border-radius:20px;padding:3px 12px;font-size:0.76rem;color:var(--t2)}}.badge b{{color:var(--ac)}}
.layout{{display:grid;grid-template-columns:1fr 1fr;gap:0}}
.col{{padding:22px 26px}}.col-l{{border-right:1px solid var(--bd)}}
.stitle{{font-size:0.92rem;font-weight:700;color:var(--t2);margin-bottom:12px;padding-bottom:7px;border-bottom:1px solid var(--bd)}}
.case-grid{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}
.cc{{background:var(--sf);border:1px solid var(--bd);border-radius:8px;padding:11px;transition:border-color 0.2s}}.cc:hover{{border-color:var(--ac)}}
.ch{{display:flex;justify-content:space-between;margin-bottom:5px}}
.br{{display:flex;align-items:center;gap:7px;margin-bottom:5px}}
.bl{{font-size:0.76rem;color:var(--txt);min-width:90px;text-align:right}}
.bt{{flex:1;background:var(--sf2);border-radius:4px;height:15px}}.bf{{height:100%;border-radius:4px}}
.bv{{font-size:0.7rem;color:var(--t2);min-width:22px}}
#dn{{width:100%;height:340px;background:var(--sf2);border-radius:10px;border:1px solid var(--bd);display:block}}
.legend{{display:flex;gap:12px;flex-wrap:wrap;margin:8px 0;font-size:0.76rem}}
.li{{display:flex;align-items:center;gap:5px}}.ld{{width:10px;height:10px;border-radius:50%}}
.full{{padding:22px 26px;border-top:1px solid var(--bd)}}
table{{width:100%;border-collapse:collapse;font-size:0.79rem}}
thead tr{{background:var(--sf2)}}th{{padding:8px 10px;text-align:left;color:var(--t2);font-weight:600;border-bottom:1px solid var(--bd);white-space:nowrap}}
td{{padding:7px 10px;border-bottom:1px solid var(--bd);vertical-align:top}}tr:hover td{{background:var(--sf2)}}
.tc{{display:inline-block;border-radius:4px;padding:1px 6px;font-size:0.68rem;margin:1px;font-weight:600;background:rgba(77,208,225,0.15);color:var(--cm);border:1px solid rgba(77,208,225,0.3)}}
.ts{{display:inline-block;border-radius:4px;padding:1px 6px;font-size:0.68rem;margin:1px;font-weight:600;background:rgba(240,98,146,0.15);color:var(--sp);border:1px solid rgba(240,98,146,0.3)}}
.tp{{position:fixed;background:var(--sf2);border:1px solid var(--bd);border-radius:8px;padding:8px 12px;font-size:0.77rem;max-width:240px;pointer-events:none;opacity:0;transition:opacity 0.15s;z-index:999;line-height:1.5}}.tp.show{{opacity:1}}.tp b{{color:var(--ac)}}
@media(max-width:900px){{.layout{{grid-template-columns:1fr}}.col-l{{border-right:none;border-bottom:1px solid var(--bd)}}.case-grid{{grid-template-columns:1fr}}}}
</style></head><body>
<div class="nav"><a href="../index.html">← 전체 지식맵</a><span style="color:var(--bd)">|</span><span style="color:var(--ac);font-weight:700">{icon} {domain}</span></div>
<div class="hero">
  <h1>{icon} AI 혁신 역량 지식맵 — <span>{domain}</span></h1>
  <div class="hero-sub">{H.escape(meta["desc"])}</div>
  <div class="badges">
    <div class="badge">사례 <b>{len(cases)}</b>건</div>
    <div class="badge">공통기술 <b>{len(uc)}</b>종</div>
    <div class="badge">특화기술 <b>{len(us)}</b>종</div>
    <div class="badge">분야: <b>{en}</b></div>
    <div class="badge">핵심기술: <b>{H.escape(meta.get("key",""))}</b></div>
  </div>
</div>
<div class="layout">
  <div class="col col-l">
    <div class="stitle">① 분야 개요 및 대표 사례</div>
    <div class="case-grid">{cards()}</div>
  </div>
  <div class="col">
    <div class="stitle">② 필요 역량 체계 (D3.js)</div>
    <div class="legend">
      <div class="li"><div class="ld" style="background:#6c63ff"></div>사례(해외)</div>
      <div class="li"><div class="ld" style="background:#81c784"></div>사례(국내)</div>
      <div class="li"><div class="ld" style="background:var(--cm)"></div>공통기술</div>
      <div class="li"><div class="ld" style="background:var(--sp)"></div>특화기술</div>
    </div>
    <svg id="dn"></svg>
    <div class="stitle" style="margin-top:18px">③ 기술군 분류</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">
      <div><div style="font-size:0.8rem;font-weight:700;color:var(--cm);margin-bottom:8px">공통 기술 (IT 범용)</div>{bar(cs_,"var(--cm)")}</div>
      <div><div style="font-size:0.8rem;font-weight:700;color:var(--sp);margin-bottom:8px">분야 특화 기술</div>{bar(ss_,"var(--sp)")}</div>
    </div>
  </div>
</div>
<div class="full">
  <div class="stitle">④ {domain} 전체 사례 ({len(cases)}건)</div>
  <div style="overflow-x:auto">
  <table><thead><tr><th>사례명</th><th>기관</th><th>지역</th><th>공통기술</th><th>특화기술</th><th>연도</th><th>중요도</th></tr></thead>
  <tbody>{rows()}</tbody></table></div>
</div>
<div class="tp" id="tp"></div>
<script>
const NJ={nj};const LJ={lj};
function st(e,h){{const t=document.getElementById("tp");t.innerHTML=h;t.classList.add("show");t.style.left=(e.clientX+12)+"px";t.style.top=(e.clientY-8)+"px"}}
function ht(){{document.getElementById("tp").classList.remove("show")}}
(function(){{
const sv=d3.select("#dn"),W=document.getElementById("dn").clientWidth||460,H2=340;
sv.attr("viewBox",`0 0 ${{W}} ${{H2}}`);
const zoom=d3.zoom().scaleExtent([0.2,5]).on("zoom",e=>g.attr("transform",e.transform));
sv.call(zoom);const g=sv.append("g");
const sim=d3.forceSimulation(NJ).force("link",d3.forceLink(LJ).id(d=>d.id).distance(60)).force("charge",d3.forceManyBody().strength(-100)).force("center",d3.forceCenter(W/2,H2/2)).force("collision",d3.forceCollide(15));
const lk=g.append("g").selectAll("line").data(LJ).join("line").attr("stroke",d=>d.tt==="common"?"rgba(77,208,225,0.5)":"rgba(240,98,146,0.4)").attr("stroke-width",1.2).attr("stroke-opacity",0.5);
const ng=g.append("g").selectAll("g").data(NJ).join("g").call(d3.drag().on("start",(e,d)=>{{if(!e.active)sim.alphaTarget(0.3).restart();d.fx=d.x;d.fy=d.y;}}).on("drag",(e,d)=>{{d.fx=e.x;d.fy=e.y;}}).on("end",(e,d)=>{{if(!e.active)sim.alphaTarget(0);d.fx=null;d.fy=null;}}));
ng.append("circle").attr("r",d=>d.type==="case"?7:5).attr("fill",d=>d.type==="case"?(d.region==="overseas"?"#6c63ff":"#81c784"):(d.tt==="common"?"var(--cm)":"var(--sp)")).attr("stroke","rgba(255,255,255,0.3)").attr("stroke-width",1).on("mouseover",(e,d)=>st(e,d.type==="case"?`<b>${{d.name}}</b>`:`<b>${{d.name}}</b><br>${{d.tt==="common"?"공통기술":"특화기술"}}`)).on("mouseout",ht);
ng.append("text").attr("dy",-9).attr("text-anchor","middle").attr("font-size",8).attr("fill","var(--txt)").attr("pointer-events","none").text(d=>d.type==="tech"?(d.name.length>7?d.name.substring(0,7)+"…":d.name):"");
sim.on("tick",()=>{{lk.attr("x1",d=>d.source.x).attr("y1",d=>d.source.y).attr("x2",d=>d.target.x).attr("y2",d=>d.target.y);ng.attr("transform",d=>`translate(${{d.x}},${{d.y}})`)}});
}})();
</script></body></html>"""

for domain in DATA["metadata"]["domains"]:
    meta = META.get(domain)
    if not meta: continue
    cases = [c for c in DATA["cases"] if c["domain"] == domain]
    content = make_html(domain, meta, cases)
    out = domain_dir / meta["file"]
    with open(out, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"OK: {meta['file']} ({len(cases)} cases)")
print("All done!")