# 방치형 게임 리서치 — 카테고리 JSON 스키마 (공통 규칙)

이 리서치는 **실제 상용 서비스할 방치형(idle) 게임을 기획**하기 위한 근거 자료다.
기준일: **2026-10-14 (KST)**. 모든 서술 텍스트는 **한국어**로 작성한다(게임 원제·고유명사는 원문 병기 가능).

## 절대 규칙
1. **숫자·사실을 지어내지 않는다.** 출처 URL로 확인한 것만 쓴다. 확인 못 하면 해당 키를 생략하거나 "미확인"이라고 쓴다.
2. 추정치(센서타워·AppMagic·모바일인덱스 등)는 **"추정"과 출처·시점**을 함께 쓴다. 다운로드/매출/동접/누적 방문은 서로 다른 지표이므로 섞어 비교하지 않는다.
3. 해석(인기 요인 등)은 문장 끝에 "(해석)"을 붙인다. 사실과 해석을 구분한다.
4. 모든 게임은 `url`(공식 사이트 또는 공식 스토어 페이지)을 갖고, 같은 URL이 `evidence` 배열에도 반드시 1개 들어간다.
5. 과금은 **실제 확인한 상품명·가격**(App Store 페이지의 '앱 내 구입' 목록, 공식 확률 공시, 공식 상점/공지, Steam 상점, Roblox API 등)만 `products`/`verified`에 넣는다. 게임 내 재화로 사는 것을 현금 과금의 증거로 쓰지 않는다. 확인 못 한 범위는 `unverified`에 반드시 적는다.
6. 출처 우선순위: 공식(개발사/퍼블리셔/스토어/확률 공시/IR) > 데이터 기업 보도(센서타워·AppMagic·모바일인덱스) > 주요 매체(인벤·게임메카·디스이즈게임·아이뉴스24·전자신문·pocketgamer.biz·mobilegamer.biz·gamesindustry.biz 등) > 위키/커뮤니티(표시하고 보조로만).
7. `accessed`는 실제 확인한 날짜(보통 "2026-10-14").
8. 파일은 UTF-8 JSON. 작성 후 반드시 `python -c "import json;json.load(open(r'<경로>',encoding='utf-8'))"`로 문법 검증.

## 카테고리 파일 구조 (research/idle/<id>.json)
```json
{
  "id": "카테고리 id (지정값)",
  "region": "국내 | 해외 | 글로벌",
  "platformGroup": "모바일 | PC/Steam | PC·웹·모바일 | 로블록스 | 멀티",
  "name": "카테고리 이름 (지정값)",
  "asOf": "2026-10-14",
  "scope": "다루는 범위 1~2문장",
  "selectionBasis": "선정 기준과 목록 순서의 기준(예: 2026년 국내 매출 순위 근거 순). 공식 전체 순위가 아니라 연구자 선정 목록임을 명시",
  "methodology": ["조사 방법·한계 3~6개"],
  "overview": "이 하위 장르의 시장 개요 4~7문장. 최근 1~2년 흐름·대표 지표·변화(근거 기반, 숫자에는 출처 시점).",
  "commonalities": ["공통점 4~6개"],
  "designPatterns": [{"name":"패턴명","detail":"작동 방식","examples":["게임명"]}],
  "monetizationPatterns": [{"name":"과금 패턴","detail":"설명","examples":["게임명"]}],
  "risks": ["이 하위 장르로 신작을 낼 때의 위험·실패 요인 3~6개"],
  "pipeline": [{"name":"출시 예정/준비작","note":"상태·출처 한 줄"}],
  "games": [GAME × 10],
  "deepDive": DEEPDIVE,
  "recommendations": [REC × 3],
  "sources": [SOURCE ...]
}
```
`pipeline`은 해당 없으면 `[]`. `designPatterns` 5~8개, `monetizationPatterns` 4~6개.

### GAME (정확히 10개, rank 1~10)
```json
{
  "rank": 1,
  "id": "kebab-case-고유값",
  "name": "국내 서비스명(있으면) 또는 원제",
  "originalName": "원제/영문명 (name과 같으면 생략)",
  "url": "https://공식 사이트 또는 공식 스토어",
  "developer": "개발사",
  "publisher": "퍼블리셔 (개발사와 같으면 같게)",
  "origin": "개발사 국가",
  "release": "YYYY-MM-DD 또는 YYYY-MM (지역 표기)",
  "platforms": ["Android","iOS","PC(Steam)","웹","Roblox" 등],
  "subgenre": "세부 장르 한 줄",
  "businessModel": "예: 부분유료(IAP 중심)+보상형 광고 / 유료 구매 $4.99 / 무료+Steam 마켓 아이템",
  "status": "서비스 중 | 얼리 액세스 | 서비스 종료(날짜) 등",
  "description": "1~2문장",
  "coreLoop": ["4~6단계 핵심 루프 (마지막은 반복 지점)"],
  "features": ["사실 위주 특징 4~6개"],
  "progression": ["성장 축/시스템 4~8개"],
  "idleMechanics": "오프라인·방치 보상 방식(최대 누적 시간, 보상, 광고/유료 가속). 모르면 '미확인'",
  "socialAndLiveOps": ["길드·랭킹·PvP·레이드·이벤트·시즌·업데이트 주기 등 3~6개"],
  "popularityFactors": ["인기 요인 3~5개 (해석이면 (해석))"],
  "monetization": {
    "model": "IAP 중심 | 광고 중심 | 혼합 | 유료 구매 | 무료(후원/코스메틱)",
    "summary": "과금 구조 2~3문장",
    "products": [{"name":"상품명","price":"₩/$/Robux 표기","contents":"구성·효과(알면)","evidence":"근거 출처 제목"}],
    "verified": ["확인된 과금 사실 2~6개"],
    "unverified": "확인하지 못한 범위 (필수)",
    "productEvidence": true
  },
  "metrics": {
    "downloads": "…(출처·시점)",
    "revenue": "…(추정 여부·출처·시점)",
    "chart": "…",
    "rating": "…",
    "ccu": "…",
    "players": "…",
    "other": "…"
  },
  "userFeedback": {"positive":["2~3개"],"negative":["2~3개"],"basis":"근거(스토어 리뷰/Steam 리뷰/커뮤니티 등)"},
  "takeaways": {"borrow":["신작에 가져올 점 2~4개"],"avoid":["피할 점 2~3개"]},
  "evidence": [SOURCE × 3~8]
}
```
`metrics`는 확인된 키만 넣는다(문자열, 출처·시점 포함). `productEvidence`는 실제 상품명·가격 근거를 확인했을 때만 true.

### SOURCE
```json
{"url":"https://…","title":"출처 제목","type":"공식 | 스토어 | 보도 | 데이터(추정) | 위키/커뮤니티 | 인터뷰","note":"이 출처에서 확인한 내용 한 줄","accessed":"2026-10-14"}
```

### DEEPDIVE (카테고리당 1개 — 가장 배울 점이 많은 대표작 해부)
```json
{
  "gameId": "games[].id 중 하나",
  "title": "해부 이유 한 줄",
  "summary": "3~5문장",
  "firstSession": ["첫 10~30분(FTUE) 경험 단계 4~8개"],
  "coreLoop": [{"step":"짧은 동사구","detail":"설명"}],
  "currencies": [{"name":"재화","earn":"획득처","spend":"사용처","paid":false}],
  "growthAxes": [{"name":"성장 축","detail":"설명","monetized":"무료 | 유료 가속 | 유료 전용"}],
  "gacha": {"pools":["뽑기 종류"],"rates":["공시 확률(출처)"],"pity":"천장/보정","source":"확률 공시 출처 제목"},
  "offline": "오프라인 보상 상세",
  "adPlacements": ["보상형 광고 위치·보상"],
  "storeStructure": ["상점 구성: 첫 결제/패스/월정액/단계 패키지/한정 판매 등 (가격 확인 시 표기)"],
  "liveOpsCadence": ["업데이트·이벤트 주기 사례(날짜)"],
  "metricsTimeline": [{"date":"YYYY-MM-DD","event":"사건","value":"수치(출처)"}],
  "strengths": ["3~5개"],
  "weaknesses": ["3~5개"],
  "lessons": ["우리 신작에 적용할 교훈 3~5개"],
  "evidence": [SOURCE ...]
}
```
뽑기가 없는 게임은 `gacha`를 `null`, 광고가 없으면 `adPlacements`를 `[]`.

### REC (카테고리당 3개 — 원작 복제가 아닌 독립 신작 아이디어)
```json
{
  "name": "가칭",
  "pitch": "한 문장",
  "target": "타깃 이용자·시장",
  "platform": "출시 플랫폼",
  "coreLoop": ["3~5단계"],
  "mvp": ["MVP 범위 3~6개"],
  "difficulty": "낮음 | 중간 | 높음",
  "effort": "예: 1인+AI 주20시간 12~16주 / 3인 팀 4~6개월",
  "monetization": "과금 설계",
  "why": "근거 (이 카테고리 사례와 연결)",
  "risks": "위험",
  "kpiGate": "소프트런칭에서 통과해야 할 지표 기준",
  "buildNext": "첫 작업"
}
```

## 최종 응답 (부모 에이전트에게)
파일 작성·검증 후 **15줄 이내**로만 답한다: ①선정 10개(이름 — 핵심 근거 지표 한 줄) ②deepDive 대상 ③확인 못 한 주요 공백·주의점. JSON 전문을 답변에 붙이지 않는다.
