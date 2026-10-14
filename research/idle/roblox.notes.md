# 로블록스 방치·타이쿤·성장 시뮬레이터 — 조사 기록 (부분 결과)

- 기준일: 2026-10-14 KST
- 상태: **partial**. 작업 중단 요청으로 저장했다.
  - `roblox.json`: 게임 10개 전체 항목과 카테고리 공통 섹션(overview·commonalities·designPatterns·monetizationPatterns·risks·pipeline·sources)을 작성했다.
  - `deepDive`·`recommendations`는 서술 전이다. 재료는 아래에 정리했다.
- 원자료: `roblox-api-snapshot.json`
  - 공식 API 지표·패스·개발자 상품·공식 이벤트·그룹 정보와 제3자 Rolimon's 값.
  - 장문 설명은 제외했다.
- 공식 지표 조회 시각: 2026-10-13 22:30:23 UTC (2026-10-14 07:30 KST)

## 1. 선정 10개와 근거

- 순서: 공식 API 동접 스냅샷 내림차순.
- 공통 조건: 공식 장르가 Simulation/Tycoon 또는 Simulation/Incremental Simulator이고, 방치 메커닉이 공식 설명·상품·이벤트로 확인된 작품.

| # | 게임 (universeId) | 동접 스냅샷 | 핵심 근거 |
|---|---|---|---|
| 1 | Steal An Egg (10563114921) | 900,094 | 2026-07-25 생성. Rolimon's 최고 14,293,524(약 3주 전). 펫이 초당 돈 생산, 알 실시간 성장. 러닝머신 동영상 피드가 2026-08-25 Roblox 보상형 피드 정책 대상(Inven Global) |
| 2 | Steal a Brainrot (7709344486) | 622,905 → 18분 뒤 517,399 | 공식 Q3 2025 주주서한 "2,500만 돌파". Rolimon's 25,836,222(2025-10-11). 화요일 22:00 UTC Taco Tuesday(Dexerto) |
| 3 | Fish It! (6701277882) | 67,901 | Rolimon's 최고 2,716,766(2025-12-07). 일 01:00 UTC 주간 업데이트. AFK 낚시 전제는 **미확인**(공식 설명은 클릭 충전·연타) |
| 4 | Pet Simulator 99! (3317771874) | 50,665 | Auto Farm 175·Auto Tap 350 Robux. 2026-09-05 오프라인 Coin Tray(BIG Games 블로그). 최고 732,936(2023-12-09) |
| 5 | Anime Dice (10708913337) | 50,581 | 2026-08-15 생성. 공식 설명 "MONEY GENERATES WHILE YOU ARE OFFLINE". 57일간 업데이트 8회. 긍정 99.2% |
| 6 | Sol's RNG (5361032378) | 27,679 | 자동 굴림 RNG. Quick roll 100. 시즌 패스 499. 최고 193,836(2024-05-12). Roblox 공식 광고 가이드 사례 |
| 7 | Bee Swarm Simulator (601130232) | 26,697 | 2018년부터 운영. 필드 체류형 반자동 채집. 게임패스 4종 판매 중지(2026-08-04 갱신, 사유 미확인). 최고 264,505(2025-12-29) |
| 8 | Grow a Garden (7436755782) | 12,992 | 공식 "your garden literally grows while you are offline". 공식 "2025년 7월 약 2,200만". Rolimon's 22,375,597(2025-08-23) |
| 9 | Bubble Gum Simulator INFINITY (6504986360) | 10,049 | 2025-04-11 출시. 금요일 업데이트. Auto Fishing 349. 최고 380,959(2025-05-04) |
| 10 | Plants & Brainrots (8316902627) | 1,916 | 구 Plants vs Brainrots. 최고 8,654,525(2025-10-11)에서 급감. 그룹 소유자 jandel |

## 2. 확인한 핵심 수치와 출처

### 공식 문서
- **DevEx 환율** (https://create.roblox.com/docs/production/monetization/developer-exchange)
  - 0.0038달러/Earned Robux(30,000=114달러).
  - 2025-09-05 10am PT 이전 적립분은 0.0035달러.
  - 최소 30,000 Robux, 13세 이상.
- **미국 18세 이상 우대 환율** (https://create.roblox.com/docs/production/monetization/18-plus-devex-rate)
  - 0.0054달러, 2026-06-08 시행, R15 필수.
- **게임패스 수익 배분** (https://create.roblox.com/docs/monetize-experiences)
  - 크리에이터 70%(타 크리에이터 패스 재판매 시 10% 제휴 수수료).
- **Creator Rewards** (https://create.roblox.com/docs/creator-rewards)
  - Active Spender가 그날 첫 3개 경험 중 하나로 10분 이상 플레이하면 5 Robux.
  - 신규·복귀 유저는 첫 60일 결제 100달러까지 35%.
- **보상형 광고** (https://create.roblox.com/docs/production/promotion/rewarded-video-ads)
  - 보상은 개발자 상품이어야 하고 랜덤 보상은 금지.
  - 3~10 Robux 상당 보상을 권장.
- **공식 장르 가이드 PDF(2026)**
  - Incremental Sim(https://prod.docsiteassets.roblox.com/assets/ads/IncrementalSim_Playbook.pdf): Opt-in 13%+·일 2.8회. 'Welcome Back Earnings'(오프라인 수익 2배) 전략, Sol's RNG Fast Roll 사례.
  - Tycoon(https://prod.docsiteassets.roblox.com/assets/ads/Tycoon_Playbook.pdf): 15%+·3회+. Grow a Garden을 Progressive Rewards 사례로 명시.
- **유료 랜덤 아이템 정책** (https://create.roblox.com/docs/production/monetization/paid-random-items)
  - 알 부화·행운 부스트 등은 수치 확률 공개 의무.
  - PolicyService의 ArePaidRandomItemsRestricted·IsPaidItemTradingAllowed로 국가별 제한 이용자 처리.
- **유휴 접속 해제** (https://create.roblox.com/docs/reference/engine/classes/Player — Player.Idled)
  - 20분 유휴 시 자동 접속 해제.

### IR 주주서한 (https://s27.q4cdn.com/984876518/files/doc_financials/…)
- **Q2 2025**
  - Grow a Garden이 출시 1개월 안에 지출 1위, 6월 세계 기록 뒤 7월 약 2,200만 명.
  - Grow a Garden을 뺀 경험 내 지출 +36%.
  - Grow a Garden DAU의 75% 이상이 같은 날 다른 경험도 플레이.
  - 플랫폼 동접 3,200만 명.
- **Q3 2025**
  - Steal a Brainrot 2,500만 돌파.
  - 2025-08-23 플랫폼 동접 4,500만 명 이상.
  - DevEx 1,000 Robux당 3.50→3.80달러.
- **Q4 2025**
  - 2025년 매출 49억 달러, 부킹 68억 달러(+55%).
  - 상위 1,000 크리에이터 평균 130만 달러.
- **Q1 2026**
  - 미국 18세 이상 지출의 크리에이터 몫 26.6%→37.8%('노블 게임' 장려).
- **Q2 2026**
  - 부킹 +8%.
  - '고수익 2025년산 바이럴 게임'에서 참여 이동.
  - Grow a Garden 2가 빠르게 상위권 진입.

### RDC 보도자료
- **RDC 2026** (2026-09-11, ir.roblox.com)
  - Roblox Everywhere 독립 앱, 크롬 웹 플레이, 오프라인 모드, 비동기 알림 발표.
  - 최근 12개월 크리에이터 수익 약 17억 달러.

### 공식 이벤트 API의 업데이트 시각 최빈값 (UTC)
- Grow a Garden: 토 14·20시, 수 22시
- Steal a Brainrot: 토 19~20시
- PS99: 토 16시
- Sol's RNG: 토 08시
- BGSI: 금 20~21시
- Fish It!: 일 01시
- Steal An Egg: 토 15시
- Plants & Brainrots: 토 22시

### Grow a Garden 월 중앙값 동접 (Rolimon's 내장 이력, 6시간 표본, 직접 재계산)
- 2025-06: 2,379,731
- 2025-10: 379,423
- 2026-02: 37,867
- 2026-04: 123,661
- 2026-10(1~13일): 17,629
- 좋아요 비율: 94.1%(2025-05) → 89.9%(2026-07)

## 3. 검토 후 제외한 후보와 이유
- **Break and Steal an Egg** (동접 94,565, 최고 935,530): 공식 설명에 "inspired by steal an egg"라고 적힌 파생작. 복제 위험 사례로만 인용.
- **Capybaras VS Plants** (1,574): 오프라인 수익·날씨 변이·'Triple Offline Earnings' 24 Robux가 있으나 규모가 작아 패턴 사례로만 인용.
- **PLS DONATE** (2,271): 공식 장르가 Social이고 기부 중심이라 성장 루프가 아님.
- **Ride A Pet** (47,148): 맵 탐색형.
- **+1 Speed Keyboard Escape** (41,911): 이동 기반 증분형으로 방치가 아님.
- 참고만 한 작품:
  - **Grow a Garden 2**: 공식 후속작. 같은 소유자 DevNamedDavid. 최고 929,371(2026-06-19). 2026-08-17~25 급락, 원인 미확인.
  - **Idle Mafia Game**: 'Offline Operations' 480 Robux 패스.
  - **Merge a Nuke!**: 오프라인 수익, Auto Merge 199.

## 4. 실패하거나 막힌 출처
- 웹 검색: 세션 공유 한도 소진으로 중간부터 불가. 이후 공식 문서·IR·API는 직접 URL로만 조회.
- `games.roblox.com/v1/games/{id}/game-passes`: HTTP 404. `apis.roblox.com/game-passes` 로 대체.
- WebFetch 차단(403/402): en.help.roblox.com, Fandom 위키.
  - Fandom 위키는 하위 에이전트가 MediaWiki API로 일부 열람.
- 하위 에이전트 보고상 원문을 못 연 매체: Bloomberg, Polygon, IGN, Reuters, Business Insider, GamesIndustry.biz, Reddit. 헤드라인·위키백과 인용으로만 확인.
- 미확인으로 남은 사항:
  - Fish It! 자동 낚시 무료 여부
  - Bee Swarm 매크로 정책과 패스 판매 중지 사유
  - Steal a Brainrot·Steal An Egg의 오프라인 수익 여부
  - 전 게임 매출(공식·언론 수치 없음)

## 5. 하위 에이전트 결과 (3개 모두 완료·종료, 실행 중 없음)
- **Grow a Garden 심층**: 원작자 BMWLux, Splitting Point(Jandel) 2025-04 합류, Do Big Studios 소수 지분.
  - 동접 이정표: 500만(2025-05-17, Kotaku), 890만(PocketGamer.biz), 1,100만(05-31, Game Rant), 2,130만(06-21, PocketGamer.biz), 7월 약 2,200만(공식), 2,237만(08-23, Rolimon's).
  - 위키 기반 메커닉: 상점 5분 재입고, 알 30분, 부화 10분~8시간, 변이 배수 Wet×2~Cosmic×240, Gold×20·Rainbow×50, 비 약 20분 주기.
  - 운영·경제: 거래 2025-08-02, 거래 월드 2025-11-29, Sheckle 거래세(2025-08-30~09-10).
  - 평가: AP 'chill', Kotaku '프로토타입 같다', PC Gamer 이벤트 전담팀.
- **약탈 타이쿤**
  - Admin War(2025-08-23): Grow a Garden 2,110만·Steal a Brainrot 2,000만·Roblox 4,740만(Tubefilter, 직접 확인).
  - Steal a Brainrot: Taco Tuesday(Dexerto), Spyder Games 소송·Tung Tung Tung Sahur 분쟁(Aftermath·GamesBeat).
  - Steal An Egg: 러닝머신 피드와 2026-08-25 정책(Inven Global·PocketGamer.biz, 직접 확인), 2026-08-24~25 약 3시간 비공개(AllThingsHow, 커뮤니티).
- **펫/RNG**
  - PS99: 2023-12-01 출시, Coin Tray 오프라인(블로그 직접 확인), Blood Moon 2시간마다 10분(블로그 직접 확인).
  - BGSI: 2025-04-11 출시, 2025-05-04 최고 동접.
  - Sol's RNG: 매크로 허용은 나무위키만 근거(미검증).
  - Anime Dice: 업데이트 8회, IP 위험(해석).
  - Hindenburg 보고서: 다계정·AFK 지표 의혹, 적대적 출처.

## 6. 딥다이브 재료 (Grow a Garden, 서술만 남음)
- **FTUE**: 빈 플롯 8칸, 시작 씨앗, 당근 10¢·약 8초 성장, 10분 한정 Starter Pack(공식 상품 99 Robux), 친구당 Sheckles +10%(최대 40%).
- **재화**
  - Sheckles(판매, 무료)
  - 이벤트 재화(Honey 등)
  - Trade Tokens(1토큰=1 Robux, 유료)
  - 시즌 패스(749 Robux, Skip Tier 49, Skip All 1,699)
  - Garden Coins(Ascension)
- **상점(공식 카탈로그)**
  - 재입고: Auto Restock 79, Restock Shop 79
  - 성장 스킵: Skip Growth 49, Grow All Plants 375
  - 씨앗 직구: Carrot 7 ~ Alien Apple 1,700, Super Seed 199/575/1,699
  - 확률형: Premium 알 149~4,999, Exotic 상자 199~6,999
  - 날씨형: Seed Rain 199/699/1,299
  - 기타: Expand Garden 99, Trading Ticket 19
  - 광고 보상: Ad Reward 상품 2종(2026-02-13)
- **업데이트 타임라인**: 공식 이벤트 108건, 2025-04-19부터 매주 토요일.
  - 2025-05-24 MONSTER MASH RECORD
  - 2025-08-02 TRADING
  - 2025-08-23 ADMIN WAR
  - 2025-09-27 Seed Stages + 시즌 패스
  - 2026-04-15부터 수 22:00 Watering Wednesday
  - 2026-06-12 Grow a Garden 2 예고
  - 다음 업데이트 2026-10-17 20:30 UTC
- **업데이트 당일 표본**: 2025-12-13 860,130(당일 낮 157,193), 2026-04-04 1,071,787(89,514), 2026-10-10 103,532.

## 7. 추천 3개 초안 방향 (미작성)
1. **Roblox — 약탈 없는 협동형 오프라인 농장(차밭 등)**
   - 날씨 변이, 복귀 보상 광고(오프라인 수익 2배), 토·수 2박자 운영.
   - KPI: 세션 10분+(Creator Rewards 기준선), 광고 Opt-in 15%+·일 3회+(공식 Tycoon 가이드).
2. **독립 플랫폼(모바일/Steam) — RNG 교배 수족관**
   - 자동 시도와 오프라인 상한(PS99 Coin Tray 참고), 비동기 방문, 확률 공시.
3. **Roblox O18 — R15 크루를 쓰는 비동기 습격 운영형**
   - 미국 18세 이상 우대 DevEx 0.0054와 RDC 2026 비동기 알림 활용.
   - 손실 상한으로 약탈 좌절 완화.

## 8. 남은 할 일
`roblox.json`의 `todo` 필드와 같다.
1. deepDive 서술
2. recommendations 3개
3. overview를 7문장 이내로 압축하고 최신 정책 반영
4. risks·patterns 보강
5. 최종 검수와 json.load 재검증

빌드 스크립트(scratchpad `build/`)는 세션 임시 폴더라 보존이 보장되지 않는다. 원자료는 `roblox-api-snapshot.json`에 있다.
