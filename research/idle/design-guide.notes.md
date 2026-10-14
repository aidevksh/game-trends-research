# 방치형 게임 설계·경제 가이드 — 작업 기록 (기준일 2026-10-14)

- 산출물: `design-guide.json` (UTF-8, `python json.load` 검증 완료, 최상위 `"status": "partial"`, `"todo"` 9건)
- 채운 배열: summary 10 · taxonomy 9 · formulas 20 · prestige 8 · bigNumbers 12 · pacing 12 · krIdleRpgSystems 21 · monetizationDesign 15 · antiPatterns 12 · balancing 10 · telemetry 15 · sources 94
- 스키마 확장: 지시("각 항목에 근거 출처")에 따라 `taxonomy`·`telemetry` 항목에도 `source`를 추가했다. 그 외 필드는 지정 구조 그대로다.
- 하위 에이전트: 띄우지 않았다(직접 조사). 이 폴더의 `_sub-*.notes.md`, `SCHEMA.md`, `TASKS.md`, `config.json`, `tools/`는 다른 에이전트가 만든 파일이며 건드리지 않았다.
- 중단 사유: 조정자 요청으로 중단. 웹 검색 한도(턴당 200회, 모든 에이전트 공유)가 도중에 소진돼 이후는 이미 아는 URL을 직접 조회해 보완했다.

## 1. 확인한 공식 (정확한 수식 · 출처)

| 항목 | 수식 | 출처 |
|---|---|---|
| 단일 구매 비용 | cost_next = b × r^k | https://www.gamedeveloper.com/design/the-math-of-idle-games-part-i |
| 대량 구매 합계 | cost(n) = b × r^k × (r^n − 1)/(r − 1) | 같은 글 |
| 최대 구매 수 | n_max = floor(log_r(c(r−1)/(b·r^k) + 1)) | 같은 글 |
| 생산 | production_total = (production_base × owned) × multipliers | 같은 글 |
| AdCap 레모네이드 | b=3.738(첫 개 무료라 4/1.07), r=1.07, 1.67/초 | 같은 글 + https://adventure-capitalist.fandom.com/wiki/Businesses |
| 파생 성장 | n단계 체인 ≈ t^n/n!, 합 → e^t | https://www.gamedeveloper.com/disciplines/the-math-of-idle-games-part-ii |
| 프레스티지 일반형 | p = k(E/E0)^α → 2배에 E가 2^(1/α)배 필요 (α=1/2→4배, 1/3→8배, 0.14→약 128~141배) | https://www.gamedeveloper.com/design/the-math-of-idle-games-part-iii |
| AdCap 엔젤 | floor(150√(LE/10^15)) = floor(√(LE/(4×10^11/9))), 엔젤당 +2%(가산), 화성 300√(LE/10^15) | https://adventure-capitalist.fandom.com/wiki/Angel_Investors |
| Cookie Clicker(현행) | prestige = ∛(전 기간 누적 쿠키/10^12), 칩 1:1, 레벨당 CpS +1% × 해금 잠재력(5/25/50/75/100%) | https://cookieclicker.wiki.gg/wiki/Ascension , https://cookieclicker.wiki.gg/wiki/Upgrades |
| Cookie Clicker 건물 | Price = Base × 1.15^(M−F), ×10 = 20.303718238배, ×100 = 7,828,749.67배 | https://cookieclicker.wiki.gg/wiki/Buildings |
| Clicker Heroes 영혼 | floor(Σ영웅 레벨/2000) + floor(((L−80)/25)^1.3 × Ponyboy), 영혼당 DPS +10% | https://clickerheroes.fandom.com/wiki/Hero_Souls |
| Clicker Heroes HP | L≤140: ceil(10(L−1+1.55^(L−1))×[보스×10]), 141~500: ceil(10(139+1.55^139×1.145^(L−140))×[보스×10]), 보스 타이머 30−2·floor(Z/500)초 | https://clickerheroes.fandom.com/wiki/Formulas |
| Clicker Heroes 레벨 비용 | floor(floor(BaseCost×1.07^level)×CostReduction) | https://clickerheroes.fandom.com/wiki/Heroes |
| Egg Inc. EB | SE×(10+Soul Food+소울 스톤)×(1.05+0.01×Prophecy Bonus+…)^PE×1.01^EoT | https://egg-inc.fandom.com/wiki/Earnings_Bonus |
| Egg Inc. SE 획득 | 구간별 분수 지수(0.15→0.21) 합, 구식 (c_R/10^6)^0.14 | https://egg-inc.fandom.com/wiki/Earnings_Bonus/Soul_Eggs + Part III |
| Egg Inc. 오프라인 | 실로당 1시간 + 연구 6분×20레벨, 최대 30시간, 스탠다드 효율 50%·프로 100%, 실로 비용 100,000×(n−1)^(n+14) | https://egg-inc.fandom.com/wiki/Grain_Silos |
| Realm Grinder | p = (√(1+8·c_M/10^12) − 1)/2 | Part III |
| 회수 기간 PP | max(cost − bank, 0)/cps + cost/Δcps | https://github.com/CookieMonsterTeam/CookieMonster |
| 리셋 경험칙 | 이번 리셋 획득이 보유량의 +50~200%일 때 | https://www.slideshare.net/slideshow/quest-for-progress-gdc-europe-2016/65405507 |
| 타임워프 | d = x/(1.21y + 1), 1일 10골드·7일 25골드·14일 40골드 | https://adventure-capitalist.fandom.com/wiki/Time_Warps |
| 가챠 천장(수학적 유도) | E = (1−(1−p)^N)/p, P(천장 도달) = (1−p)^(N−1) | 예시 값: 메이플 키우기 잠재 0.21%/714회 → 평균 약 370회(나무위키) |
| 큰 수 한계 | 2^1024−2^971 ≈ 1.7976931348623157e308, 2^53−1, float 3.4e38 | MDN MAX_VALUE·MAX_SAFE_INTEGER, Microsoft Learn |

## 2. 시스템·수익화·안티패턴 정리분 (JSON 본문 요약)

- 한국형 키우기 표준: 골드 스탯 강화(레전드 오브 슬라임 10종), 소환 레벨형 가챠(메이플 키우기 무기 다이아 20개/회·소환 레벨 18=212,050회, 동료 50개/회·13레벨=45,800회), 보유/장착 효과, 유물 5☆ 각성, 슬롯 강화(스타포스 30성·실패 포인트 천장), 성장 던전(일 3회·최대 10회 누적), 길드·월드보스·레이드·아레나, 무기/동료 패스, 월정액(세나키 9,900원·28일 광고 제거+루비, 메이플 12,000원 오프라인 1.5배), 첫 결제 보상, 확률 공시(제33조② 2024-03-22 시행, 제33조의2 고의 시 3배·입증책임 2025-08-01 시행).
- 수익화: 2배 부스트(Kongregate 표준 2배·4시간, Egg Inc. 2→8시간), 오프라인 2배, 무료 재화, 광고 제거(영구 vs 기간제), 타임워프, 영구 배수(AdCap ×3/×12/×27), 가격 사다리, 패스, 구독(Egg Inc. ULTRA $3.99/$7.99), Pro Permit($9.99), 저금통, 가챠, 이벤트 상점, 광고+IAP 하이브리드(PUC-Rio: 5종 모두 IAP·4종 광고), 고래 구조.
- 안티패턴: 확률 오류·비공지 수정(메이플 키우기 → 전액 환불), 표기 스탯 불일치(공속 임계값), 광고 과다·기간제 광고 제거(세나키), 허위·표절 광고(버섯커), 방치 불가 레벨 디자인, 오프라인 처벌, 서버 통합 격차, 매크로·버그, 시간 조작·보상 위조(AdMob SSV), 발열, 팝업·푸시 남발, 미성년자 수익화(Grow a Garden).

## 3. 검증 못 한 항목

- 국내 키우기류 오프라인 보상 '통상 최대 시간' — 공식 근거 없음(메이플 키우기 효율만 확인).
- 메이플 키우기 사과·환불 공지 원문, 국가법령정보센터 조문 원문 — JS 페이지라 직접 확인 못 함(나무위키·CEO스코어데일리로 대체).
- Habby·Game Hive·Hyper Hippo 공개 수익화 발표 — 미확보.
- Mind Studios 수치(광고 60~70% 등)는 출처 미인용 → JSON에 '근거 약함'으로 표시.
- 나무위키 수치는 사용자 편집 위키라 공식 교차 검증 필요(JSON 각 source.note에 명시).
- '(일반적 설계 관행, 근거 약함)' 표시 항목: FTUE 30초/5분 목표, 오프라인 상한-리듬 매핑, A/B 대상 목록, 팝업 빈도, 큰 수 직렬화, 치명 피해 곱연산, 시간 조작 설명.

## 4. 실패·막힌 출처

- blog.kongregate.com 원문(Part I~III) → 404 (Game Developer 재게재본 사용).
- fandom 위키 일반 페이지 → WebFetch 402/curl 403 (MediaWiki API `action=parse`로 우회 조회 성공).
- yna.co.kr → WebFetch 차단.
- maplestoryidle.nexon.com, forum.nexon.com, habby.com → JS 렌더링으로 본문 없음.
- law.go.kr → JS 로딩으로 본문 없음.
- GDC Vault 본편 → 회원 전용. 슬라이드의 차트 수치 → 이미지라 미추출.
- gameanalytics.com/?p=6634 → 홈페이지로 연결(해당 글 없음).
- 웹 검색 → 턴 공유 한도 200회 소진(이 에이전트 사용 약 13회).

## 5. 남은 할 일

`design-guide.json`의 `todo` 배열과 같다: 1차 출처 재확인, 국내 오프라인 상한 근거, Habby·Game Hive·Hyper Hippo 사례, 강연 정량 차트, 근거 약함 항목 보강, 시간 조작 대응 문서, 나무위키 수치 공식 교차 검증, Mind Studios 수치 대체 데이터, 아케이드·하이브리드 대표작 근거.

## 6. 재생성

생성 스크립트는 세션 스크래치패드(`.../scratchpad/tools/build_design_guide.py`)에 있어 세션 종료 후 남지 않을 수 있다. JSON 자체가 완결본이므로 이후 수정은 JSON을 직접 편집하면 된다.
