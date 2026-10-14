# 방치형 게임 리서치 — 작업 인계 문서

- 작성: 2026-10-14 (KST), Claude Code 세션 중단 시점 기록
- 목적: 다른 AI/작업자가 이 문서만 보고 이어서 완성할 수 있게 한다.
- 관련 문서: [TASKS.md](TASKS.md)(조사 과제 13개 원문) · [SCHEMA.md](SCHEMA.md)(카테고리 JSON 스키마·규칙) · `research/idle/*.notes.md`(에이전트별 중단 시점 메모)

---

## 1. 사용자 요구 (원문)

> 국내 해외 인기 방치형 게임 리서치해서 `C:\Users\FORYOUCOM\Desktop\game-trends-research\docs\index.html` 처럼 리포트 만들어봐. 특정 어느 게임 플랫폼에 한정할 필요 없음.
> 리서치 결과를 가지고 실제 서비스하는 게임을 만들 거니까 리포트가 `docs/index.html` 보다 더 자세하게 나와야됨. 꼼꼼하게 분석해

해석해서 정한 방향:
- 기존 리포트(`docs/index.html`, 로블록스·메이플 월드·마인크래프트·유즈맵 160항목)와 같은 형식이다. 파이프라인은 JSON 데이터 → 빌드 스크립트 → 오프라인 HTML이고, 디자인 언어도 같다.
- **더 자세하게** 하기 위해 다음을 더한다.
  - 게임 카드 항목을 늘린다: 핵심 루프, 성장 시스템, 방치 메커닉, 소셜/라이브옵스, 상품·가격표, 유저 반응, 가져올 점·피할 점.
  - 장르별 대표작 해부: 재화, 성장 축, 공시 확률, 상점, 업데이트 주기, 지표 타임라인.
  - 시장·KPI 벤치마크, 경제 공식과 시뮬레이터, 한국 규제·플랫폼 수수료·기술 스택·출시 체크리스트.
  - 상용 기획안: 후보 방향 점수 비교, 기획안별 시스템·경제·과금·KPI 게이트·팀·일정, 로드맵.
- 새 파일로 만든다: `docs/idle-games.html` + `docs/idle-report-data.json`. **기존 `docs/index.html`은 수정하지 않는다.**

## 2. 현재 상태 한눈에

| 항목 | 상태 |
| --- | --- |
| 리포트 템플릿 `scripts/idle-report-template.html` | **완료** (CSS·JS·필터·정렬·툴팁·시뮬레이터·체크리스트) |
| 빌드 `scripts/build_idle_report.py` | **완료** (샘플 데이터로 빌드 성공) |
| 검증 `scripts/validate_idle_report.py` | **완료** (실데이터 완성 후 실행) |
| 설정 `research/idle/config.json` | **완료** (카테고리 10개 순서·파일·출력 경로) |
| 스키마 `research/idle/SCHEMA.md`, 과제 `TASKS.md` | **완료** |
| 레이아웃 테스트 | **완료** — 샘플 100개로 1440px·390px에서 JS 오류 0, 가로 넘침 0, 필터·검색·초기화 정상 |
| 카테고리 데이터 10개 + 가이드 3개 | **미완료** — 에이전트 13개가 조사 도중 중단됨. 아래 3절 표 참고 |
| `research/idle/overview.json` (핵심 결론·추천 기획·로드맵) | **미작성** — 7절 명세 참고 |
| 최종 빌드 `docs/idle-games.html` | **미생성** (overview·데이터 완성 후) |
| README 갱신 | **미실시** |
| git 커밋 | **안 함** (사용자 요청 시에만) |

## 3. 에이전트별 진행 상태 (중단 시점)

에이전트들에게 "추가 검색 없이 현재까지 결과를 `<id>.json`(최상위 `status:"partial"`, `completed`, `todo`) + `<id>.notes.md`로 저장하고 종료"하라고 지시했다. 실제 저장 결과는 아래 표에 기록한다(파일이 없으면 해당 과제는 처음부터 다시 수행).

<!-- STATUS_TABLE_START -->
**2026-10-14 13:40 기준: 데이터 13개 + overview 작성 완료, `docs/idle-games.html` 빌드·검증 통과.**
- 카테고리 10개 모두 게임 10개·deepDive·추천 3개를 갖추고 `tools/check_category.py`와 `scripts/validate_idle_report.py` PASS. 출처 URL 873개.
- 1차 에이전트는 중단 후 기록을 `raw/*.log.md`로 추출했고, 2차 Sonnet 에이전트가 로그로 JSON을 완성했다(새 웹 조회는 거의 없음).
- `design-guide.json`은 `status:"partial"`(todo 9건: 국내 키우기 오프라인 상한 근거 등)이지만 모든 배열이 채워져 빌드에 문제없음.
- 화면 점검: 1440·390px 가로 넘침 0, JS 오류 0, 필터·검색·초기화 정상.
<!-- STATUS_TABLE_END -->

**2차 작업(완료)**: 조사 로그로 JSON을 다시 만드는 Sonnet 에이전트 12개를 실행했다. 대상은 kr-major, kr-indie, global-rpg, hybrid, tycoon, arcade-idle, desktop, incremental, cozy, market, build-guide이고, roblox는 deepDive와 추천 3개를 마무리한다. 각 에이전트는 게임 2개마다 파일을 저장한다(`"status":"partial"`). 완료되면 status 키가 사라진다. 중단됐다면 파일의 `status`를 확인하고, 남은 부분만 같은 방식으로 로그를 보고 채우면 된다.


## 4. 파일 지도

| 경로 | 내용 |
| --- | --- |
| `research/idle/config.json` | 카테고리 순서·파일명·기대 게임 수(각 10), 가이드 파일명, 출력 경로 |
| `research/idle/<카테고리>.json` | 장르별 10개 게임 분석 (SCHEMA.md 구조). 10개: kr-major, kr-indie, global-rpg, hybrid, cozy, tycoon, arcade-idle, desktop, incremental, roblox |
| `research/idle/market.json` | 시장 지표·시계열·대표작 지표·차트 스냅샷·연표·트렌드·KPI 벤치마크 |
| `research/idle/design-guide.json` | 하위 장르 분류표·공식·프레스티지·페이싱·키우기 표준 시스템·수익화·안티패턴·밸런싱·텔레메트리 |
| `research/idle/build-guide.json` | 한국/해외 규제·스토어 수수료·광고 스택·기술 스택·출시 플레이북·체크리스트 |
| `research/idle/overview.json` | (미작성) 제목·핵심 결론·후보 방향 점수표·상용 기획안·로드맵·프롬프트·추가 차트 |
| `research/idle/*.notes.md` | 에이전트 중단 시점 메모(확인 수치·출처·남은 일) |
| `research/idle/raw/*.log.md` | 에이전트 조사 원자료 로그(검색·페치·API 결과). JSON 재구성용 |
| `research/idle/tools/extract_transcripts.py` | 에이전트 JSONL 기록 → 로그 변환기 |
| `research/idle/tools/make_sample.py` | 레이아웃 테스트용 가짜 데이터 생성기 (배포 금지) |
| `research/idle/tools/shot.cjs` | Playwright 스크린샷·가로 넘침·필터 테스트 (데스크톱 1440 / 모바일 390) |
| `research/idle/tools/check_links.py` | JSON 안의 출처 URL 실제 접속 점검(404/DNS 실패=broken, 403/429=차단·불명) |
| `scripts/idle-report-template.html` | 보고서 레이아웃·스타일·상호작용 (자리표시자 `{{...}}`) |
| `scripts/build_idle_report.py` | JSON → `docs/idle-games.html`, `docs/idle-report-data.json` |
| `scripts/validate_idle_report.py` | 개수·필수 필드·출처·id 중복·앵커·외부 자산·자리표시자 검증 |

## 5. 빌드·검증·테스트 방법

Python **3.12 이상** 필요(빌드 스크립트가 f-string 안에서 같은 따옴표를 중첩 사용 — PEP 701). 이 PC는 3.13.3.

```sh
# 실데이터 빌드 → docs/idle-games.html, docs/idle-report-data.json
python scripts/build_idle_report.py
python scripts/validate_idle_report.py

# 데이터가 덜 모였을 때 레이아웃만 보는 법 (docs/를 건드리지 않음)
python research/idle/tools/make_sample.py <샘플폴더> research/idle/config.json
IDLE_DATA_DIR=<샘플폴더> IDLE_OUT_DIR=<출력폴더> python scripts/build_idle_report.py

# 화면 점검 (Playwright·Chrome 경로는 shot.cjs 상단에 하드코딩)
node research/idle/tools/shot.cjs docs/idle-games.html <스크린샷폴더> full

# 출처 링크 점검
python -I research/idle/tools/check_links.py <결과.json> research/idle/kr-major.json research/idle/kr-indie.json ...
```

- 빌드는 `config.json`의 카테고리 10개 + 가이드 4개(overview·market·design-guide·build-guide)가 **모두 있어야** 실행된다. 부분 데이터로 미리 보려면 위 샘플 방식을 쓰거나 빈 구조의 JSON을 임시로 둔다.
- 검증 스크립트는 카테고리당 정확히 10개 게임, 필수 필드, `url`이 `evidence`에 포함, `game.id` 전체 유일, deepDive의 `gameId` 존재, 추천 3개 이상(`kpiGate` 포함), overview 필수 필드, 외부 자산 없음, 내부 앵커를 검사한다.
- 레이아웃 테스트에 쓴 Playwright: `C:/Users/FORYOUCOM/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright`, 브라우저: `C:/Program Files/Google/Chrome/Application/chrome.exe`.

## 6. 리포트 구성과 설계 결정

**섹션 순서** (상단 메뉴와 동일): 히어로(통계 5개·조사 기준) → 핵심 결론(overview.summary) → 시장(market) → 장르 지도(design.taxonomy + 수익 모델 구성 차트 + 장르 요약표) → 추천 기획(overview: 점수표·기획안·로드맵·프롬프트) → 게임 100선(장르별: 개요·공통점·위험·설계/과금 패턴·출시 예정작·카드 10개·대표작 해부·신작 아이디어 3개·조사 방법) → 비교표(100행, 정렬·검색) → 설계 가이드(design: 원칙·공식·**경제 곡선 시뮬레이터**·프레스티지·페이싱·키우기 표준 시스템·수익화·안티패턴·밸런싱·텔레메트리·큰 수) → 출시 가이드(build: 규제·수수료·광고·기술 스택·플레이북·체크리스트).

**결정 사항**
- 디자인은 `docs/index.html`과 같은 색·서체·레이아웃을 쓴다(`--bg #f5f4ee`, `--accent #195343`, `--lime #d7f08e`, Malgun Gothic). 라이트 테마만 쓰고, 외부 CDN·이미지·추적기 없이 오프라인으로 동작한다.
- 카테고리 표시 순서: kr-major → kr-indie → global-rpg → hybrid → cozy → tycoon → arcade-idle → desktop → incremental → roblox (`config.json`).
- 수익 모델 필터·차트는 `monetization.model` 문자열을 5개 버킷으로 자동 분류한다(`build_idle_report.py`의 `model_bucket`). 버킷은 `IAP 중심 / 혼합 / 광고 중심 / 유료 구매 / 무료·기타`이며, 데이터 작성 시 model 값을 SCHEMA.md 표기대로 맞춘다.
- 플랫폼 필터: `platforms` 배열의 문자열로 `모바일/PC/웹/로블록스/콘솔`을 자동 분류(`platform_buckets`).
- 차트: 반응형 HTML/CSS 막대(SVG 확대 시 글자 깨짐 문제로 교체).
  - 팔레트 `#2a78d6, #eb6834, #1baf7a, #eda100` + 기타 회색 `#b9b8b0`.
  - 보고서 표면색 `#fffefb` 기준 색각 이상 검증을 통과했다. 청록·노랑은 대비 3:1 미만이라 모든 차트에 "표로 보기"를 넣었다.
  - 차트 종류: 단일 시계열은 세로 막대(`market.series`), 동접 비교 등은 가로 막대(`overview.extraCharts`), 장르별 수익 모델은 100% 누적 막대.
- 시뮬레이터 모델:
  - 비용 = b·r^레벨
  - 초당 수익 = p·레벨·(마일스톤 배수)^⌊레벨/간격⌋·프레스티지 배수
  - 세로축은 대기 시간 로그 눈금이며, 예시 프리셋 4개(AdCap·Cookie Clicker 근사 등)를 둔다.
- 체크리스트 체크 상태는 브라우저 localStorage(`idle-report-checklist-v1`)에만 저장한다(try/catch 처리).
- 게임 카드: 공식 URL 링크, 개발/퍼블리셔/국가/출시/플랫폼/장르 칩, 지표, 핵심 루프 단계, 특징·성장 시스템·방치 메커닉·라이브옵스·인기 요인(해석)이 들어간다. 과금은 요약·상품표·확인된 정보·미확인 범위로, 유저 반응은 + / −로 나누고, 가져올 점/피할 점과 출처 목록을 단다.
- 필터를 좁히면(검색·플랫폼·모델·근거 필터) 장르 개요·해부·아이디어 블록(`.cat-extra`)은 숨기고 카드만 보여 준다.

## 7. `overview.json` 명세 (미작성 — 데이터 완성 후 작성)

```json
{
  "date": "2026-10-14",
  "title": "히어로 제목 (예: 방치형 게임, 무엇을 만들어야 하나)",
  "subtitle": "부제",
  "intro": "히어로 소개 1~2문장",
  "methodology": ["조사 기준 6~9개 (아래 초안)"],
  "summary": [{"title":"결론","body":"근거 설명","implication":"우리 게임에 주는 결론","evidence":"근거 요약(출처명·시점)"}],
  "marketHighlights": ["market.marketStats의 id 8개 — 히어로 아래 KPI 타일로 표시"],
  "extraCharts": [{"id":"ccu-steam","section":"market|genres","title":"…","subtitle":"…","unit":"명","points":[{"label":"게임","value":526572,"note":"시점"}],"source":{SOURCE},"wide":false,"highlight":null}],
  "criteria": [{"key":"market","label":"시장성","weight":1.5,"desc":"설명"}],
  "directions": [{"name":"후보 방향","example":"대표 사례","scores":{"market":4},"verdict":"판단 한 줄"}],
  "concepts": [{"rank":"01","genre":"장르","name":"가칭","pitch":"…","tags":["…"],"why":["…"],"target":"…","platform":"…","positioning":"…","coreLoop":["…"],"systems":["…"],"economy":["…"],"monetization":["…"],"products":[{"name":"…","price":"₩…","contents":"…"}],"content":["첫 90일"],"kpi":["…"],"team":["…"],"timeline":["…"],"risks":["…"],"references":["…"],"firstSteps":["…"]}],
  "roadmap": [{"phase":"0","title":"…","duration":"…","tasks":["…"],"gate":"다음 단계 조건"}],
  "starterPrompt": "AI 코딩 도구용 첫 프로토타입 요청문"
}
```
검증 필수: `date, title, subtitle, methodology, summary, criteria, directions, concepts, roadmap, starterPrompt`. concept 필수: `name, pitch, why, coreLoop, systems, economy, monetization, kpi, team, risks`.

**methodology 초안**
1. 기준일은 2026-10-14 KST다. 공식 사이트·스토어·확률 공시·IR·데이터 기업 보도·주요 매체를 대조했고, 게임을 직접 결제하거나 전수 플레이하지는 않았다.
2. 10개 하위 장르 × 10개 = 100개는 연구자 선정 목록이며 공식 전체 순위가 아니다. 장르별 선정 기준과 목록 순서는 각 장르 머리말에 적는다.
3. 국내는 한국 앱마켓 매출·인기 순위와 국내 보도를 근거로 삼았다. '국내 중소·인디'는 개발사 국적을 확인했다.
4. 해외는 센서타워·AppMagic 공개 보도, Steam(SteamDB/SteamCharts/Steam 상점), Roblox 공개 API를 근거로 삼았다.
5. 매출 추정·다운로드·동접·누적 방문·DAU는 서로 다른 지표이므로 순위로 비교하지 않는다. 데이터 기업 수치는 모델 추정치다.
6. 과금은 App Store '앱 내 구입' 목록, 확률 공시, 공식 상점·공지, Steam 상점, Roblox 게임패스 API로 확인한 상품만 '확인된 정보'로 표시한다. 인게임 재화 거래는 현금 과금 근거로 쓰지 않는다. 지역·시점에 따라 가격이 다를 수 있다.
7. 인기 요인·공통점·추천은 연구자의 해석과 가설이며 인과 검증을 거치지 않았다.
8. 규제 요약은 법률 자문이 아니다.
9. 기획안의 가격·KPI·일정은 공개 벤치마크를 바탕으로 한 초기 가정이다.

**criteria 초안** (5점, 높을수록 유리):
- 시장성 `market` (가중 1.5)
- 경쟁 강도 `competition` (가중 1, 경쟁이 약할수록 높은 점수)
- 개발·운영 부담 `devCost` (가중 1.5, 부담이 적을수록 높은 점수)
- 수익화 깊이 `monetization` (가중 1)
- 차별화 여지 `differentiation` (가중 1)
- 유입 효율·바이럴 `ua` (가중 1)

**검토 중이던 후보 방향 (데이터로 검증 전 — 점수 미부여)**
- A. 한국형 키우기 RPG(신규 IP): 국내 비중이 가장 크다. 대형 IP가 상위권을 차지하고 있고, 과거 레전드 오브 슬라임처럼 글로벌 원빌드로 성공한 중소 선례가 있다.
- B. 방치 + 로그라이트 하이브리드: Capybara Go!형. IAP가 강하고 글로벌 출시가 가능하다.
- C. 코지 컬렉션 방치: 고양이와 스프형. 광고+IAP, IP·굿즈로 확장할 수 있고 소규모 팀에 맞는다.
- D. Steam 데스크톱 방치: TBH·Bongo Cat형. 개발 범위가 작고 바이럴에 유리하다. 대신 수익화가 제한되고 봇·마켓 위험이 있다.
- E. 아케이드 아이들: 퍼블리셔와 협업해 CPI 테스트 중심으로 간다. 다운로드는 크지만 광고 중심이라 ARPU가 낮다.
- F. 클래식 인크리멘탈(Steam 유료·웹): 1인 개발에 맞는다. 매출 규모는 작지만 꾸준하다.
- G. 로블록스 방치 타이쿤: 도달 범위는 크지만 플랫폼에 종속되고 유행 주기가 짧다.

**roadmap 초안**
- 0 컨셉 검증 (2~3주)
  - 할 일: 경쟁작 10개 플레이 분석, 경제 스프레드시트, 페이퍼 프로토타입, 아트 톤 테스트, 스토어 페이지 목업.
  - 통과 조건: 내부 테스트 5인 중 4인 이상이 "다음 성장을 원한다"고 답하고, 7일 진행 곡선을 확정한다.
- 1 프로토타입 (4~6주)
  - 할 일: 핵심 루프, 오프라인 보상, 성장 3축, 30분 분량, 텔레메트리 이벤트.
  - 통과 조건: 외부 테스터 20~30명에서 첫 벽 도달률과 재접속률을 측정한다.
- 2 알파/버티컬 슬라이스 (6~8주)
  - 할 일: 아트 확정, 1주 분량 콘텐츠, 상점·광고 SDK, 서버 세이브, 확률 공시 페이지.
- 3 소프트런칭 (6~10주)
  - 할 일: 제한 국가 또는 국내 CBT, 소액 UA, CPI·D1/D7/D30·ARPDAU 측정, 2주 단위 업데이트.
- 4 정식 출시 (4주 준비)
  - 할 일: 사전예약, 마케팅, 운영툴, CS.
- 5 라이브옵스
  - 할 일: 2주 이벤트, 월 1회 콘텐츠, 시즌.
- 각 단계의 통과 기준 수치는 market.json의 KPI 벤치마크(출처 포함)로 채운다.

## 8. 사전 조사로 확인한 사실 (메인 세션 직접 확인, 출처 포함)

> 에이전트 결과와 별개로 메인 세션이 웹 검색·페이지 조회로 확인한 것. "검색 요약"은 검색 도구의 요약에서만 본 것이라 원문 재확인이 필요하다.

**한국 시장**
- 2025 대한민국 게임백서(한국콘텐츠진흥원, 2026-03 발간 보도)
  - 국내 모바일 게임 매출 중 **방치형 비중: 2020년 1.7% → 2024년 16%**.
  - 방치형 RPG 비중: 2021년 1.6% → 2024년 7.1%.
  - MMORPG 비중: 2021년 67% → 2024년 51.3%.
  - 2024 국내 게임시장 23조 8,515억 원, 기사 추정 방치형 약 3조 8,000억 원.
  - 모바일 이용자 46.0%가 '빠른 레벨업'을 위해 아이템을 구매한다.
  - 같은 기사가 전한 개별 소식:
    - 던전앤파이터 방치형 버전 발표(넥슨 CMB, 출시일 미정).
    - 애니멀 버스터즈(라인게임즈) 2026-04-07 출시.
    - 버섯커 키우기: 2024 상반기 매출 3위·다운로드 1위, 반년 만에 글로벌 3억 5,000만 달러, 한국 비중 34%.
    - 메이플 키우기: 출시 5개월 후에도 구글플레이 매출 1위.
  - 출처: 한국금융경제신문 2026-04-14 https://www.kfenews.co.kr/news/articleView.html?idxno=656841 (백서 원문은 미확인)
- 센서타워 한국 블로그(2023-10, 2023-01~08 데이터)
  - 한국 모바일 게임 매출 중 RPG 57.5%.
  - 한국 RPG 매출 중 방치형 RPG 1.7%(2019) → 4.4%(2023), MMORPG 77% → 69.5%, 스쿼드 12.7% → 17.7%.
  - 국내 방치형 매출 순위: 1위 레전드 오브 슬라임(국내 약 1,000만 달러·글로벌 약 7,700만 달러, 2022-08 출시), 2위 블레이드 키우기(2022-02), 3위 아처키우기(2021-02), 4위 개판오분전(2023-07-28), 6위 Hero Wars: Alliance.
  - 픽셀 히어로(2023-06): 스쿼드 RPG 매출 3위·성장 1위.
  - 출처: https://sensortower.com/ko/blog/Korea-stands-out-as-the-leading-country-with-RPG-revenue-constituting-approximately-60-percent-of-total-mobile-game-revenue
- 메이플 키우기(넥슨·에이블게임즈, 2025-11-06 출시)
  - 센서타워(2025-12-24 발표): 출시 약 45일 만에 다운로드 300만·매출 1억 달러. 매출 비중 한국 67%·미국 16.6%·대만 7.1%, 다운로드 비중 한국 37.8%·미국 16.9%·대만 10.5%. 2025 신작 방치형 RPG 매출 1위.
  - 출처: https://v.daum.net/v/0DpkUGTsyQ?f=p
- 아이뉴스24 2025-12-27 (https://v.daum.net/v/20251227081204720)
  - 메이플 키우기 안드로이드 DAU 15만(모바일인덱스, 2025-12-23). 비교: 라스트 워 10만 3,700, 마비노기 모바일 7만.
  - 세븐나이츠 키우기: 45일 누적 4,000만 달러(약 539억 원).
  - 넥슨이 바람의나라 키우기·바람키우기·방치바람 상표를 출원했다(KIPRIS).
  - 킹 오브 파이터즈 AFK(넷마블), 라그나로크 아이들 어드벤처 플러스(그라비티)가 2025년에 출시됐다.
  - 2025 게임이용자 실태조사: 게임 이용률 50.2%, 미이용 사유 1위 '이용 시간 부족' 44%, 대체 활동 OTT·영화·애니 86.3%.
- 메이플 키우기 2026-03 국내 매출 약 452억 원 1위, 양대 마켓 9주 연속 1위(모바일인덱스 2026년 4월 리포트) — **검색 요약**. 게이머스크롤 기사 원문은 410으로 조회 실패.
- 스톤에이지 키우기(넷마블): 센서타워 2026-03 글로벌 매출 성장 4위, 한국 성과가 가장 높고 동남아·미국에도 이용자층이 있다. https://sensortower.com/ko/blog/top-10-worldwide-mobile-games-by-revenue-and-downloads-in-march-2026-KR
  - 구글플레이 매출 4~5위권 진입 보도는 **검색 요약**.
- 창세기전 키우기(뉴노멀소프트): 원스토어 매출 톱10 보도 — **검색 요약**.
- 2026-09-21~27 구글플레이 인기 순위(베타뉴스 2026-09-28, https://www.betanews.net/article/view/beta202609280001)
  - 1위 아가타 키우기(에어캡): 방치형 RPG, 4인 스쿼드, 같은 등급 합성, 성인향 아트 컬렉션.
  - 2위 후더덕 서바이벌(조이게임즈): 2026-09-18 출시, 감자슉슈슉 후속, 디펜스+슈팅.
- 2026-09-11 구글플레이 매출: 메이플 키우기 2위, 총잡이 고양이 - 방치형 키우기 56위(전체 1위 제우스: 오만의 신) — **검색 요약**.
  - 게이머스크롤 순위 페이지(https://gamerscroll.com/rankings/genres/)는 '방치형' 필터가 있지만 목록 직접 조회에 실패했다. Top 200에 소울 헌터 키우기·캣 히어로·총잡이 고양이가 보인다(장르 분류는 미확인).
- 귀혼키우기(엠게임): 2026-11 출시 예정. 3인 전투대·문파·스테이지형 방치. https://www.inven.co.kr/webzine/news/?news=322001
- 배고파용 키우기: 2026-05-21 출시. https://www.wame.is/game/4205

**글로벌 모바일**
- 센서타워 미국 분기 블로그 2025 (예: https://sensortower.com/blog/2025-q2-unified-top-5-idle%20rpg-revenue-us-6040bbc2241bc16eb883a0cb , https://sensortower.com/blog/2025-q3-ios-top-5-idler%20games-revenue-us-602ae7fb241bc16eb874f8e1)
  - Q2 iOS idle RPG: Capybara Go! 주간 매출이 4월 초 약 100만 달러로 정점을 찍고 6월 말 약 38.2만 달러로 내려왔다. High Seas Hero는 5월 중순 39.3만 달러.
  - Q3 iOS: Capybara Go! 9월 초 약 43.8만 달러, Legend of Mushroom 약 21.95만 달러.
  - Q3 Android: Capybara Go! 약 14.9만 달러, AFK Journey 9월 말 11.4만 달러.
  - iOS idle(비RPG): Gold and Goblins 2월 중순 약 31.1만 달러(Q1), 8월 말 약 23.9만 달러(Q3).
- Capybara Go!(Habby)
  - 센서타워: 2024-12-11까지 약 2개월 만에 해외 매출 4,000만 달러, 2024-11 한국 매출 성장 1위. TechNode https://technode.com/2024/12/19/capybara-go-takes-40-million-in-overseas-revenue-within-two-months-of-launch/
  - AppMagic: 2025-02-10 기준 누적 약 1.09억 달러, 미국 1,610만 달러. https://www.pocketgamer.biz/habbys-capybara-go-surpasses-100m-in-gross-player-spending/
  - "2025 연간 방치형 RPG 매출 1위"라는 표현은 **검색 요약**에서만 확인.
- Legend of Mushroom: 센서타워 2023-11 이후 IAP 2.7억 달러, 한국 39.4%·일본 30% (오래된 자료). https://wnhub.io/news/finance/item-43484
- 센서타워 2026-03 전 세계 순위
  - 매출: Last War, 왕자영요, Whiteout Survival, Royal Match, Gossip Harbor.
  - 다운로드: Block Blast!, Free Fire, ROBLOX, Subway Surfers, **Pizza Ready!(5위, 아케이드 아이들)**.
- 일본 放置少女: App Store 월평균 매출 순위가 2026-01 80위 → 03 57위 → 06 65위. AppMedia https://appmedia.jp/app_review/5443987

**Steam(PC)**
- TBH: Task Bar Hero: 2026-05-27 무료 출시.
  - 출시 직후 동접 1만 미만에서 3일 만에 10만을 넘었다.
  - **최고 동접 526,572 (2026-06-14)**. https://allthings.how/task-bar-hero-tops-526000-concurrent-steam-players-amid-mixed-reviews/
  - 24시간 최고 539,098 (2026-06-16, Valve API 인용 기사).
  - 리뷰는 '복합적'. Steam 마켓 골드 파밍·봇, 서버 장애, 오정지 논란이 있었다. Inven Global에 따르면 아이템 제한 업데이트 이후 동접 약 14.3만. https://www.invenglobal.com/articles/22394/popular-idle-game-taskbar-hero-hits-140k-concurrent-users-but-gold-farmers-and-cheaters-leave-players-paying-the-price
  - 개발사 표기가 출처마다 다르다(Nugem Studio / NewGem Studio / Phat Cat Games).
- Deskrawl: Idle ARPG: 최근 30일 평균 동접 33,328. https://activeplayer.io/deskrawl-idle-arpg/
- Idle Clans: 30일 평균 약 654. https://steamcharts.com/app/2103530
- AppMagic 'Idle Games in 2026' (https://appmagic.rocks/research/idle-steam-games-2026, JS 렌더링이라 원문 미조회 — **검색 요약**)
  - Spirit City: Lofi Sessions·Cast n Chill 각각 530만 달러 이상.
  - Legends of IdleOn 약 5,900만 달러(2025-11 정식 출시).
  - Revolution Idle 310만 달러.
- Steam 전체 동접 기록 4,350만(2026). KitGuru

**로블록스**
- Steal an Egg: 2026-07-25 출시, 2개월이 안 되어 활성 약 300만·방문 31억(트래커 기준).
- Steal a Brainrot: 2025-10 처음으로 동접 2,500만을 돌파했다는 보도가 있고, 현재는 약 15.7만. https://en.wikipedia.org/wiki/Steal_a_Brainrot
- Grow a Garden: 2026 Q1 최고 약 25만. Fish It! 약 11만, Capybaras VS Plants 약 7.6만(트래커 기준). https://ejaw.net/roblox-charts/
- 저장소의 기존 공식 API 스냅샷: `research/roblox-global.json`, `research/roblox-global-api-snapshot.json` (2026-10-13).

## 9. 남은 작업 (순서대로)

1. 3절 표와 `*.notes.md`로 에이전트별 부분 결과를 확인한다. `status:"partial"`이면 `todo`를 이어서 수행하고, 파일이 없으면 [TASKS.md](TASKS.md) 지시문으로 처음부터 수행한다.
2. 카테고리 10개를 완성한다: 게임 정확히 10개, deepDive 1개, 추천 3개. 끝나면 `status`/`completed`/`todo` 필드는 지워도 된다(빌드에는 무관).
3. market / design-guide / build-guide를 완성한다.
4. `tools/check_links.py`로 출처 링크를 점검하고 broken을 고친다. 핵심 수치는 원문을 재확인한다. 특히 8절의 "검색 요약" 항목이 대상이다.
5. `overview.json`을 작성한다(7절). 핵심 결론 6~8개를 쓰고, 후보 방향 점수표, 상용 기획안 3개를 상세하게 작성한다. 로드맵 통과 기준은 벤치마크 수치로 채운다. 데스크톱 동접·로블록스 동접처럼 같은 정의의 수치는 `extraCharts`로 넣는다.
6. 빌드·검증을 돌린다: `python scripts/build_idle_report.py && python scripts/validate_idle_report.py`
7. 화면을 점검한다: `node research/idle/tools/shot.cjs docs/idle-games.html <폴더> full`. 가로 넘침·JS 오류·필터를 확인하고 스크린샷을 눈으로 본다.
8. README.md에 새 리포트(`docs/idle-games.html`)의 소개·조사 범위·재생성 명령을 추가한다. 기존 리포트 설명은 유지한다.
9. 커밋은 사용자가 요청할 때만 한다.

## 10. 주의 사항·알려진 문제

- WebFetch에서 실패한 페이지:
  - news.nate.com: EUC-KR 인코딩이 깨진다.
  - gamerscroll magazine 기사: 410.
  - appmagic.rocks research: JS 렌더링이라 본문이 없다.
  - SteamDB: 차단될 수 있다. 대안은 steamcharts·steambase·Steam 공식 API.
- 같은 사건이라도 출처마다 수치가 다르다(TBH 최고 동접 52.6만 vs 54만, 개발사명 등). 출처·시점을 함께 쓰고 하나로 단정하지 않는다.
- 세션 중 에이전트 3개가 각자 하위 에이전트를 띄웠다(`_sub-*.notes.md`). 어느 과제의 하위 작업인지는 노트 내용으로 확인한다.
- 검증 스크립트는 일부러 엄격하다(전 필드 필수). 부분 데이터 상태에서는 실패하는 것이 정상이다.
- 기존 리포트 관련 파일(`docs/index.html`, `docs/report-data.json`, `research/*.json`, `scripts/build_report.py`)은 이번 작업에서 수정하지 않았다.
