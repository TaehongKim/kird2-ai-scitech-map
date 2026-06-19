import json, pathlib

path = pathlib.Path(r"z:\CS\Common\★ 평가&자문\260521 KIRD 2\outputs\data\case_tech_map.json")
with open(path, encoding="utf-8") as f:
    DATA = json.load(f)

# 5 new cases C096-C100
new_cases = [
    {
        "id": "C096",
        "name_ko": "Google DeepMind 데이터센터 AI 냉각 자율 제어",
        "name_en": "DeepMind Data Centre Cooling AI",
        "org": "Google DeepMind",
        "country": "미국/영국",
        "region_type": "overseas",
        "domain": "에너지",
        "problem": "데이터센터 냉각 시스템 에너지 최적화 한계 — 전문가 수동 제어로 과도한 에너지 소비",
        "outcome": "냉각 에너지 40% 절감, 전체 PUE 15% 개선, 2022년 완전 자율 제어 전환(인간 감독 없이)",
        "common_techs": ["T03", "T16", "T01"],
        "domain_techs": ["T43"],
        "url": "https://deepmind.google/blog/deepmind-ai-reduces-google-data-centre-cooling-bill-by-40/",
        "year": 2022,
        "importance": "상"
    },
    {
        "id": "C097",
        "name_ko": "Meta FAIR Lean Copilot LLM 수학 증명 보조",
        "name_en": "Meta FAIR Lean Copilot",
        "org": "Meta FAIR / CMU",
        "country": "미국",
        "region_type": "overseas",
        "domain": "수학·기초과학",
        "problem": "수학 형식 증명 시스템(Lean4) 사용 시 인간이 모든 증명 전술을 수동 입력해야 하는 높은 진입 장벽",
        "outcome": "LLM 기반 증명 전술 자동 제안으로 증명 시간 대폭 단축, 비전문가도 형식 증명 가능, ICLR 2024",
        "common_techs": ["T11", "T07", "T04"],
        "domain_techs": ["T64"],
        "url": "https://arxiv.org/abs/2404.12534",
        "year": 2024,
        "importance": "중"
    },
    {
        "id": "C098",
        "name_ko": "Bayer Xarvio 디지털 작물 관리 AI 플랫폼",
        "name_en": "Bayer Xarvio FIELD MANAGER",
        "org": "Bayer Crop Science",
        "country": "독일",
        "region_type": "overseas",
        "domain": "농식품",
        "problem": "소규모 농가의 병해·잡초 관리 전문 지식 부족 및 과도한 농약 사용으로 비용·환경 부담",
        "outcome": "130개국 서비스, 5천만 헥타르+ 적용, 농약 사용 최대 20% 절감, 작물 수확량 손실 감소",
        "common_techs": ["T02", "T01", "T15"],
        "domain_techs": ["T60", "T61"],
        "url": "https://www.xarvio.com/content/xarvio/xarvio-international/en/products/field-manager.html",
        "year": 2023,
        "importance": "중"
    },
    {
        "id": "C099",
        "name_ko": "Microsoft MatterGen 생성형 AI 신소재 역설계",
        "name_en": "Microsoft MatterGen",
        "org": "Microsoft Research",
        "country": "미국",
        "region_type": "overseas",
        "domain": "소재",
        "problem": "원하는 화학·기계·전자적 특성을 가진 소재를 체계적으로 역설계하는 방법 부재",
        "outcome": "확산 모델 기반 신소재 역설계 최초 구현, 조건부 생성 정확도 기존 대비 3배 향상, Nature(2025)",
        "common_techs": ["T09", "T08", "T01"],
        "domain_techs": ["T35", "T38"],
        "url": "https://www.microsoft.com/en-us/research/project/mattergen/",
        "year": 2024,
        "importance": "상"
    },
    {
        "id": "C100",
        "name_ko": "Google DeepMind RT-2 비전-언어-행동 로봇 모델",
        "name_en": "Google DeepMind RT-2",
        "org": "Google DeepMind",
        "country": "미국/영국",
        "region_type": "overseas",
        "domain": "로봇·자율화",
        "problem": "기존 로봇은 특정 훈련 작업만 수행 가능, 새로운 언어 지시에 의한 범용 조작 어려움",
        "outcome": "웹 데이터로 학습한 VLA 모델, 새 지시에 범용 대응(훈련 외 작업 62% 성공), Science Robotics(2023)",
        "common_techs": ["T10", "T20", "T04"],
        "domain_techs": ["T70"],
        "url": "https://deepmind.google/blog/rt-2-new-model-translates-vision-and-language-into-robot-actions/",
        "year": 2023,
        "importance": "상"
    }
]

DATA["cases"].extend(new_cases)
DATA["metadata"]["total_cases"] = 100
DATA["metadata"]["overseas_cases"] = 80
DATA["metadata"]["domestic_cases"] = 20

with open(path, "w", encoding="utf-8") as f:
    json.dump(DATA, f, ensure_ascii=False, indent=2)

domain_cnt = {}
for c in DATA["cases"]:
    domain_cnt[c["domain"]] = domain_cnt.get(c["domain"], 0) + 1
print(f"Total: {len(DATA['cases'])} cases")
for d, n in domain_cnt.items():
    print(f"  {d}: {n}")