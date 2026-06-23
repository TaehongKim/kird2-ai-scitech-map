import pathlib

root = pathlib.Path(r"z:\CS\Common\★ 평가&자문\260521 KIRD 2\outputs")

# ── 1. index.html: 헤더에 "분석 보고서" 버튼 추가 ────────────
idx = root / "index.html"
txt = idx.read_text(encoding="utf-8")

# CSS: nav-btn 스타일 추가
btn_css = """  .nav-btn { display:inline-flex; align-items:center; gap:6px; background:var(--accent1); color:#fff; border:none; border-radius:20px; padding:7px 18px; font-size:0.82rem; font-weight:600; cursor:pointer; text-decoration:none; transition:opacity .15s; white-space:nowrap; }
  .nav-btn:hover { opacity:.85; }
"""
txt = txt.replace("  @media (max-width: 768px)", btn_css + "  @media (max-width: 768px)", 1)

# 헤더에 버튼 삽입 (meta-badges 닫힘 태그 + </header> 사이)
old_hdr = "  </div>\n</header>"
new_hdr = '  </div>\n  <a href="report.html" class="nav-btn">📄 분석 보고서</a>\n</header>'
txt = txt.replace(old_hdr, new_hdr, 1)

idx.write_text(txt, encoding="utf-8")

# 검증
assert 'href="report.html"' in idx.read_text(encoding="utf-8"), "index.html link missing!"
print("index.html: nav-btn link added OK")

# ── 2. report.html: 사이드바 + 커버 + 푸터에 지식맵 링크 ─────
rpt = root / "report.html"
txt = rpt.read_text(encoding="utf-8")

# CSS: sidebar-nav-btn, cover-link-btn
link_css = """.sidebar-nav-btn { display:block; background:var(--brand); color:#fff; text-decoration:none; text-align:center; padding:9px 12px; border-radius:8px; font-size:13px; font-weight:700; margin-bottom:16px; transition:opacity .15s; }
.sidebar-nav-btn:hover { opacity:.85; }
.cover-link-btn { display:inline-flex; align-items:center; gap:8px; background:rgba(255,255,255,.18); border:1px solid rgba(255,255,255,.35); border-radius:999px; padding:8px 20px; font-size:13px; font-weight:600; color:#fff; text-decoration:none; transition:background .2s; }
.cover-link-btn:hover { background:rgba(255,255,255,.28); }
"""
txt = txt.replace("</style>", link_css + "</style>", 1)

# 사이드바 로고 다음에 버튼
old_logo = '  <div class="sidebar-logo">📊 KIRD 2026 보고서</div>'
new_logo = ('  <div class="sidebar-logo">📊 KIRD 2026 보고서</div>\n'
            '  <a href="index.html" class="sidebar-nav-btn">🗺️ 종합 지식맵 바로가기</a>')
txt = txt.replace(old_logo, new_logo, 1)

# 커버 배지 마지막에 링크 배지
old_badge = '    <span class="cover-badge">⚙️ 70종 기술군</span>'
new_badge = ('    <span class="cover-badge">⚙️ 70종 기술군</span>\n'
             '    <a href="index.html" class="cover-link-btn">🗺️ 인터랙티브 지식맵 →</a>')
txt = txt.replace(old_badge, new_badge, 1)

# 푸터 링크 강조
old_foot = 'Generated with Claude AI (Anthropic) — <a href="index.html">종합 지식맵 보기</a>'
new_foot = ('Generated with Claude AI (Anthropic) &nbsp;|&nbsp; '
            '<a href="index.html" style="font-weight:700;color:var(--brand)">🗺️ 종합 인터랙티브 지식맵 →</a>')
txt = txt.replace(old_foot, new_foot, 1)

rpt.write_text(txt, encoding="utf-8")

# 검증
v = rpt.read_text(encoding="utf-8")
assert 'sidebar-nav-btn' in v, "sidebar-nav-btn missing"
assert 'cover-link-btn' in v, "cover-link-btn missing"
assert '종합 지식맵 바로가기' in v, "sidebar link missing"
assert '인터랙티브 지식맵' in v, "cover link missing"
print(f"report.html: all links added OK ({len(v):,} chars)")