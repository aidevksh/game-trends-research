# 조사 과제 명세 (13개)

2026-10-14 세션에서 병렬 에이전트 13개에 배정했던 과제 원문 요약. 다른 AI가 미완료 과제를 이어서 수행할 때 그대로 지시문으로 쓰면 된다.

- 공통 규칙·JSON 구조: [SCHEMA.md](SCHEMA.md) (카테고리 10개 공통)
- 출력 위치: `research/idle/<파일명>` (UTF-8, 작성 후 `python -c "import json;json.load(open(r'<경로>',encoding='utf-8'))"`로 검증)
- 기준일: 2026-10-14 (KST). 모든 서술은 한국어.
- 웹 검색: 기본은 일반 검색, 2026년 최신 수치처럼 찾기 어려운 것만 심화 검색.
- 중단 시점 상태: [HANDOFF.md](HANDOFF.md)의 "에이전트별 진행 상태" 표 참고 (부분 결과는 `<id>.json`의 `status:"partial"`, `todo` 필드와 `<id>.notes.md`).

카테고리 간 중복 금지 원칙: 아래 각 과제의 "제외" 목록에 있는 게임은 다른 카테고리 담당이다. `game.id`는 전체 100개에서 유일해야 한다(`scripts/validate_idle_report.py`가 검사).

---

## 1. kr-major — 국내 매출 상위 키우기 RPG · 대형 IP/퍼블리셔
- 파일 `kr-major.json` · id `kr-major` · region `국내` · platformGroup `모바일`
- 범위: 한국 앱마켓(구글플레이·앱스토어·원스토어) 매출 상위권 방치형 RPG 중 대형 퍼블리셔 또는 유명 IP 기반 작품. 해외 개발사 작품도 한국 매출 상위면 포함(예: 버섯커 키우기).
- 후보(검증 후 10개 확정, 근거가 더 강하면 교체): 메이플 키우기(넥슨·에이블게임즈, 2025-11-06, 센서타워 출시 45일 매출 1억 달러/다운로드 300만, 모바일인덱스 2026-03 국내 매출 약 452억 원 1위 보도), 세븐나이츠 키우기(넷마블, 2023-09, 45일 4,000만 달러 보도), 스톤에이지 키우기(넷마블, 2026, 센서타워 2026-03 글로벌 매출 성장 4위), 버섯커 키우기/Legend of Mushroom(Joy Nice Games, 2024 상반기 국내 매출 3위·다운로드 1위, 반년 글로벌 3.5억 달러·한국 34% 보도), 킹 오브 파이터즈 AFK(넷마블, 2025), 라그나로크 아이들 어드벤처 플러스(그라비티, 2025), 창세기전 키우기(뉴노멀소프트, 원스토어 매출 톱10 보도), 소울 스트라이크(컴투스홀딩스, 2023), 일곱 개의 대죄 키우기/IDLE(넷마블), 애니멀 버스터즈(라인게임즈, 2026-04-07), 뮤: 포켓 나이츠(웹젠), 저니 오브 모나크(엔씨 — 방치형 여부 확인 후 판단).
- pipeline(목록 외): 던전앤파이터 키우기(넥슨 CMB 발표), 바람의나라 키우기(상표 출원), 귀혼키우기(엠게임, 2026-11 예정) — 상태 검증 후 기재.
- 제외: 레전드 오브 슬라임·블레이드 키우기·아처키우기·개판오분전·아가타 키우기·그로우 캐슬 등 국내 중소·인디작, Capybara Go!, AFK 시리즈.
- 순서: 최근(2025~2026) 국내 매출 근거(월 매출·차트 순위) 순.
- 조사 포인트: 출시일·개발/퍼블리셔·PC 지원, 핵심 루프, 성장 시스템(스탯/장비/동료/펫/스킬/유물/승급), 오프라인 보상 최대 시간, 길드/랭킹/레이드, 업데이트 주기, 과금 상품(apps.apple.com/kr '앱 내 구입' 상품명·₩가격, 공식 확률 공시, 공식 카페/라운지의 패스·월정액·패키지). 지표: 모바일인덱스, 게이머스크롤·게임메카 순위, 센서타워 한국 블로그, 넥슨/넷마블/그라비티/컴투스홀딩스 IR, 구글플레이 다운로드·평점. 유저 반응: 스토어 리뷰·공식 커뮤니티·보도된 논란.
- overview: '키우기'의 대형사 확산(2023 세븐나이츠 키우기 → 2024 버섯커 → 2025 메이플 키우기 → 2026 스톤에이지), IP 활용 공식, PC 동시 지원, 한국 매출 비중.
- deepDive: 메이플 키우기 (FTUE·재화·성장 축·**공시 확률 실제 수치**·상점 구성·광고·업데이트 주기·매출 타임라인).
- recommendations 3개: 대형 IP 없이 소규모 팀이 경쟁할 독립 기획(차별화 근거·KPI 게이트 포함).

## 2. kr-indie — 국내 중소·인디 방치형 RPG
- 파일 `kr-indie.json` · id `kr-indie` · region `국내` · platformGroup `모바일`
- 범위: 한국 중소·인디 개발사의 방치형 RPG·키우기·방치형 디펜스(국내 차트 진입 또는 글로벌 흥행). **개발사 국적 필수 확인**, 중국 등 해외 개발 '키우기'는 제외(overview에서만 언급).
- 후보: 레전드 오브 슬라임(로드컴플릿, 2022-08, 센서타워: 2023년 1~8월 국내 방치형 매출 1위·글로벌 누적 약 7,700만 달러), 블레이드 키우기(2022-02, 2023 국내 방치형 매출 2위), 아처키우기: 방치형 디펜스(2021-02, 3위), 개판오분전(2023-07, 4위), 아가타 키우기(에어캡, 2026-09 구글플레이 인기 1위 보도), 그로우 캐슬(라온게임즈? 국적 확인), 픽셀 히어로(2023-06 스쿼드 RPG 매출 성장 1위 — 방치형 여부 확인), 소드마스터 스토리(슈퍼플래닛·카카오게임즈?), 총잡이 고양이 - 방치형 키우기, 소울 헌터 키우기, 캣 히어로: 방치형 RPG, 배고파용 키우기(2026-05-21), 슈퍼플래닛·게임듀오·모비릭스·클로버게임즈 등 키우기 전문 중소사 대표작.
- 제외: 메이플/세븐나이츠/스톤에이지/버섯커 키우기 등 대형작, 고양이와 스프(힐링), Pizza Ready!/Burger Please!(아케이드 아이들).
- 조사 포인트: 개발사 규모(인원·투자·매출 공시/인터뷰), 출시 전략(글로벌 원빌드·다국어·광고+IAP), 루프·성장·오프라인·광고 보상 위치, 과금 상품(App Store KR), 다운로드·평점·업데이트 주기·유저 반응. 다작(포트폴리오) 전략·투자·연매출을 overview/designPatterns에.
- deepDive: 레전드 오브 슬라임(또는 근거가 더 풍부한 대표작).
- recommendations 3개: 1~5인 팀이 실제 출시·운영 가능한 기획.
- 출처 힌트: 센서타워 한국 블로그(2023-10 'RPG 비중 60%' 리포트), 인벤·게임메카·디스이즈게임·아이뉴스24·벤처스퀘어·플래텀 인터뷰/투자 기사.

## 3. global-rpg — 해외 방치형 RPG · 영웅 수집형(AFK형)
- 파일 `global-rpg.json` · id `global-rpg` · region `해외` · platformGroup `모바일`
- 범위: 한국 외(미·일·중·동남아·유럽·중동) 매출/다운로드 상위 방치형 RPG·영웅 수집형, 일본 '放置' RPG, 중국 출해 방치 RPG.
- 후보: AFK Arena(Lilith, 2019), AFK Journey(Farlight/Lilith, 2024), Idle Heroes(DHGames, 2016), Memento Mori(Bank of Innovation, 2022), 放置少女~百花繚乱の萌姫たち~, Ulala: Idle Adventure(XD), Isekai: Slow Life, Tap Titans 2(Game Hive), Hero Wars: Alliance(Nexters), High Seas Hero(센서타워 2025 Q2 미국 idle RPG 상위 — 개발사 확인), Valor Legends / Mythic Heroes / Eternal Evolution / Soul Land / Pixel Heroes / Watcher of Realms 등. 센서타워 2025~2026 분기 'Top 5 Idle RPG'(국가별), AppMagic, pocketgamer.biz·mobilegamer.biz·gamesindustry.biz 근거로 선정.
- 제외: Capybara Go!, Legend of Mushroom, Legend of Slime, The Tower, 모든 한국 개발작.
- 조사 포인트: AFK 보상(최대 누적 시간·구성), 영웅 수집/진영/승급/장비/유물, 시즌·이벤트, 길드·PvP, 과금 상품(App Store US/KR, 월정액·배틀패스·VIP), 누적 매출/다운로드 추정, 평점, 유저 반응(과금·파워크립·서비스 종료).
- overview: AFK형의 시장 위치(2019 이후), 중국 출해 퍼블리셔 공식, 일본 시장 특성, 2025~2026 흐름.
- deepDive: AFK Journey 또는 AFK Arena (AFK 보상·뽑기 확률/천장·재화·상점·시즌·매출 타임라인).

## 4. hybrid — 방치 하이브리드 · 로그라이트/디펜스/머지
- 파일 `hybrid.json` · id `hybrid` · region `글로벌` · platformGroup `모바일`
- 범위: 방치 성장 + 로그라이트 선택·타워 디펜스·머지·텍스트 어드벤처·서바이벌·4X 등 '판단' 요소 결합 모바일 게임.
- 후보: Capybara Go!(Habby, 2024 — AppMagic 2025-02 누적 약 1.09억 달러), The Tower - Idle Tower Defense(Tech Tree Games), Gold and Goblins: Idle Merger(센서타워 2025 미국 iOS idle 상위), Top Heroes: Kingdom Saga, Wittle Defender, Idle Siege, Monster Never Cry, Survivor형 방치, 2025~2026 'idle + X' 흥행작.
- 제외: 버섯커 키우기, 레전드 오브 슬라임, 그로우 캐슬, 아처키우기, 국내 키우기 전반, AFK형 RPG, 타이쿤, 아케이드 아이들, Cell to Singularity.
- 조사 포인트: 방치↔판단 결합 방식(한 판 길이·선택 빈도·오프라인 성장), 메타 성장, 이벤트/시즌, 과금 상품(App Store), 매출/다운로드 추정, 평점·반응. The Tower는 토너먼트·Workshop 영구 성장 구조를 구체적으로.
- deepDive: Capybara Go!.

## 5. tycoon — 방치형 타이쿤 · 경영 시뮬레이션
- 파일 `tycoon.json` · id `tycoon` · region `글로벌` · platformGroup `모바일`
- 후보: Idle Miner Tycoon(Kolibri/Ubisoft), Eatventure(Hungry Studio), Egg, Inc.(Auxbrain), AdVenture Capitalist(Hyper Hippo), Idle Bank Tycoon, Idle Lumber Empire, Idle Supermarket Tycoon(Codigames), Idle Theme Park Tycoon, Idle Planet Miner(Tech Tree Games), Idle Factory Tycoon, Prison Empire Tycoon, Idle Mafia, Idle Office Tycoon, Idle Restaurant Tycoon, Idle Mining Empire. 근거: 센서타워 분기 'Top 5 Idler games'(2025~2026), AppMagic, pocketgamer.biz.
- 제외: 아케이드 아이들(Pizza Ready! 등), Gold and Goblins, Cell to Singularity, 로블록스 타이쿤.
- 조사 포인트: 루프(생산→판매→업그레이드→매니저 자동화→프레스티지), 비용 증가 공식, 프레스티지 재화·공식(AdCap 엔젤, Egg Inc. 소울/프레스티지 에그), 오프라인 수익 상한·광고 2배, 이벤트·리더보드, 과금 상품(광고 제거·스타터팩·시즌 패스·구독 Egg Inc. Ultra 등), 광고 수익 비중, 다운로드·매출 추정, 유저 반응.
- deepDive: Eatventure 또는 Idle Miner Tycoon.

## 6. arcade-idle — 아케이드 아이들 · 하이브리드 캐주얼
- 파일 `arcade-idle.json` · id `arcade-idle` · region `글로벌` · platformGroup `모바일`
- 범위: 캐릭터를 직접 움직여 운반·응대·생산하고 직원 고용으로 자동화되는 arcade idle. 광고 중심 하이퍼/하이브리드 캐주얼 퍼블리셔(Supersonic, SayGames, Voodoo, Homa, CrazyLabs, Rollic 등)와 한국 개발사.
- 후보: Pizza Ready!(센서타워 2026-03 전 세계 다운로드 5위 — 개발사 확인, 한국 슈퍼센트 여부), Burger Please!, My Perfect Hotel(SayGames), My Mini Mart(Supersonic?), Hospital Empire / Car Fix Tycoon / Fishing Village / Supermarket Manager / Idle Outpost / Bakery 계열 등 2024~2026 다운로드 상위작.
- 제외: 버튼형 타이쿤(Idle Miner 등), 로블록스 타이쿤, Capybara Go!.
- 조사 포인트: 루프(이동→수집/운반→판매→확장→직원 자동화→새 구역), 확장 구조, 세션 길이, 광고 배치(인터스티셜 빈도·보상형), IAP(광고 제거·VIP·스타터팩), 다운로드·매출 추정, 유저 반응. 한국 개발사(슈퍼센트 등) 인터뷰, 퍼블리셔 계약 모델, 프로토타입→CPI 테스트→소프트런칭, 공개된 CPI/리텐션 목표치.
- deepDive: Pizza Ready!.

## 7. desktop — PC 데스크톱·작업표시줄 방치 (Steam)
- 파일 `desktop.json` · id `desktop` · region `글로벌` · platformGroup `PC/Steam`
- 후보: TBH: Task Bar Hero(2026-05-27 무료, 2026-06 중순 최고 동접 약 52.6만~54만 보도, 골드 파밍·Steam 마켓 논란, 개발사 표기 엇갈림), Bongo Cat(2025), Rusty's Retirement(2024), Deskrawl: Idle ARPG(최근 30일 평균 동접 3.3만 보도), Spirit City: Lofi Sessions, Cast n Chill(AppMagic 530만 달러 이상), Ropuka's Idle Island, Banana(2024), Tiny Pasture, Desktop Mates, Chill Corner, Idle Waters. 근거: SteamDB/SteamCharts, Steam 상점(가격·리뷰 수·긍정률·출시일·DLC), AppMagic/Gamalytic/VG Insights, 매체.
- 제외: Cookie Clicker·IdleOn·Melvor·Revolution Idle·Gnorp·Nodebuster(인크리멘탈 담당).
- 조사 포인트: 화면 점유 방식, 입력 방식(키 입력 기반 성장 등), 백그라운드 진행, 수익 모델(유료·무료+코스메틱·Steam 인벤토리/마켓·DLC), 팀 규모, 동접·리뷰·추정 매출. Steam 아이템 드롭·마켓 거래가 동접 급등과 봇/골드파머를 만든 구조와 Valve 정책 대응.
- deepDive: TBH: Task Bar Hero(또는 Bongo Cat).
- Steam API: `https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid=…`, steamcharts.com, steambase.io.

## 8. incremental — 클래식 인크리멘탈 · 클리커 (PC·웹·모바일)
- 파일 `incremental.json` · id `incremental` · region `글로벌` · platformGroup `PC·웹·모바일`
- 후보: Cookie Clicker, Legends of IdleOn(AppMagic Steam 매출 약 5,900만 달러, 2025-11 정식 출시), Melvor Idle, Revolution Idle(AppMagic 약 310만 달러), Gnorp Apologue, Nodebuster, Idle Champions of the Forgotten Realms, Leaf Blower Revolution, Cell to Singularity, NGU Idle, Antimatter Dimensions, Clicker Heroes, Idle Slayer, Unnamed Space Idle, Dwarf Eats Mountain, Universal Paperclips, Kittens Game, Exponential Idle.
- 제외: 데스크톱 방치(TBH·Bongo Cat·Rusty's), The Tower, Egg Inc./AdCap, 로블록스.
- 조사 포인트: 레이어 구조, 비용 증가율(Cookie Clicker 건물 ×1.15 등), **프레스티지 공식 실제 수식**(위키·공식 근거), 오프라인 진행, active vs idle 균형, 수익 모델, 리뷰·동접·매출 추정. 장르사(2013 이후, 웹→Steam 상업화, 2024~2026 short incremental 흐름).
- deepDive: Cookie Clicker 또는 Legends of IdleOn (수식 정확히).

## 9. roblox — 로블록스 방치·타이쿤·성장 시뮬레이터
- 파일 `roblox.json` · id `roblox` · region `글로벌` · platformGroup `로블록스`
- 재사용 가능: `research/roblox-global.json`(2026-10-13, Steal An Egg·Steal a Brainrot·Fish It!·Pet Simulator 99!·Sol's RNG·Bee Swarm Simulator·Grow a Garden 포함), `research/roblox-global-api-snapshot.json`, `research/collect_roblox_global.py`·`collect_roblox_products.py`. 단, '방치 메커닉' 관점으로 새로 분석하고 지표는 갱신.
- 후보: Grow a Garden, Steal a Brainrot(2025-10 동접 2,500만 돌파 보도), Steal an Egg(2026-07-25 출시), Plants vs Brainrots, Pet Simulator 99, Sol's RNG, Bee Swarm Simulator, Fish It!, Capybaras VS Plants, Pls Donate, 기타 2026 방치/타이쿤 상위작.
- API: `https://games.roblox.com/v1/games?universeIds=…`, `https://apis.roblox.com/universes/v1/places/{placeId}/universe`, `https://games.roblox.com/v1/games/{universeId}/game-passes?limit=100&sortOrder=Asc`, `https://games.roblox.com/v1/games/votes?universeIds=…` (수집 시각 기록).
- deepDive: Grow a Garden(또는 Steal a Brainrot). overview에 DevEx 등 로블록스 수익 구조(공식 문서).

## 10. cozy — 힐링·컬렉션·라이프 방치 (코지 아이들)
- 파일 `cozy.json` · id `cozy` · region `글로벌` · platformGroup `모바일`
- 후보: 고양이와 스프/Cats & Soup(HIDEA, 한국), Neko Atsume 2(Hit-Point, 2024), 旅かえる/Tabikaeru(Hit-Point), Tsuki's Odyssey(HyperBeard), Pokémon Sleep(포함 근거 명시), AbyssRium/Tap Tap Fish(개발사·국적 확인), Usagi Shima, Penguin Isle(Habby), Cats & Soup 후속/스핀오프, Hamster Inn·Cat Snack Bar·Fluffy 계열, Finch.
- 제외: 전투 중심 방치 RPG, 타이쿤, 아케이드 아이들, 데스크톱 방치, 로블록스.
- 조사 포인트: 접속 루틴(하루 몇 번·몇 분·알림), 수집 구조, 꾸미기, 시간 경과 이벤트, IP 확장(굿즈·콜라보·애니), 수익 모델(광고 제거·보상형·코스메틱·구독·시즌 패스), 다운로드·매출·평점·반응. HIDEA 개발 규모·성과·IP 사업 상세.
- deepDive: 고양이와 스프.

---

## 11. market — 시장·KPI 벤치마크 (`market.json`)
구조: `asOf`, `summary[]`, `marketStats[{id,label,value,unit,period,region,note,source}]`, `series[{id,title,unit,points[{x,y}],note,source}]`(같은 정의 연속 수치 3개 이상), `topTitles[{name,metric,value,period,note,source}]`, `chartSnapshots[{date,store,entries[{rank,name,note}],source}]`, `timeline[{date,event,significance,source}]`(15~25개), `trends[{title,body,evidence[],implication}]`(8~10개), `benchmarks[{metric,segment,value,note,source}]`, `userInsights[{stat,value,note,source}]`, `regionNotes[{region,notes,sources[]}]`, `sources[]`. SOURCE = `{url,title,type,note,accessed}`.
조사: ①한국 방치형 비중·규모·추이와 2025~2026 상위작 월별 지표, 2026-09~10 차트 스냅샷 ②글로벌 Idle/Idle RPG 매출·다운로드·국가별 비중 ③Steam 방치/인크리멘탈 출시 수·매출 상위·데스크톱 붐 지표 ④KPI 벤치마크(D1/D7/D30, ARPDAU, 결제 전환, 보상형 광고 시청률·eCPM, CPI, 세션) — GameAnalytics·Liftoff·AppsFlyer·Adjust·Unity·AppLovin·Sensor Tower 등 2024~2026 ⑤장르 연표 ⑥트렌드.
검증할 단서: [HANDOFF.md](HANDOFF.md) "사전 조사로 확인한 사실" 참고.

## 12. design-guide — 방치형 설계·경제 가이드 (`design-guide.json`)
구조: `asOf`, `summary[]`, `taxonomy[{name,definition,coreLoop,monetization,examples[],smallTeamFit(상|중|하),fitReason}]`, `formulas[{name,formula,explanation,typicalValues,examples,source}]`(10개 이상), `prestige[{game,currency,formula,effect,source}]`, `bigNumbers[{topic,detail,source}]`, `pacing[{topic,guideline,rationale,source}]`(8개 이상), `krIdleRpgSystems[{system,detail,monetization,examples[],source}]`(12개 이상), `monetizationDesign[{pattern,detail,bestPractice,risk,examples[],source}]`(10개 이상), `antiPatterns[{issue,why,fix,examples[],source}]`(8개 이상), `balancing[{step,detail,tools,source}]`, `telemetry[{event,purpose,keyParams}]`, `sources[]`.
조사: Kongregate 'The Math of Idle Games' Part I~III(Anthony Pecorella, 2016)·GDC 강연, 비용/생산/프레스티지 공식(AdCap 엔젤 150·√(누적/1e15), Cookie Clicker 천상의 칩 현행 공식, Clicker Heroes, Egg Inc.), 오프라인 수익 상한, 큰 수(break_infinity.js/break_eternity.js, BreakInfinity C#), 한국형 키우기 표준 시스템, FTUE·세션 설계, 수익화 패턴, 안티패턴, 밸런싱·텔레메트리, 하위 장르 분류표(소규모 팀 적합도). 근거 약한 통념은 "(일반적 설계 관행, 근거 약함)" 표시.

## 13. build-guide — 규제·플랫폼·기술·출시 (`build-guide.json`)
구조: `asOf`, `disclaimer`, `regulationsKR[{topic,rule,effective,whatToDo,penalty,source}]`, `regulationsGlobal[{region,topic,rule,whatToDo,source}]`, `storeEconomics[{platform,fee,notes,source}]`, `adMonetization[{topic,detail,source}]`, `techStack[{layer,options[{name,pros,cons,cost,source}]}]`, `launchPlaybook[{phase,detail,source}]`, `checklist[{area(법무|스토어|기술|운영|마케팅),item,priority(필수|권장)}]`(25개 이상), `sources[]`.
조사: 한국 — 확률형 아이템 표시 의무(게임산업법 개정, 2024-03-22 시행), 확률 조작 손해배상 개정 여부·시행일, 해외 게임사 국내대리인 지정(2025-10 시행 여부), 등급분류(오픈마켓 자체등급분류사업자, PC/Steam·웹 자체 서비스 시 필요 여부, Steam 지정 여부), 전자상거래법 청약철회·미성년자 결제 취소·2025-02-14 다크패턴 규제, 개인정보보호법(만 14세 미만), 게임 재화 환전 금지(게임산업법 제32조), 확률형 아이템 자율규제, 인앱결제 강제 금지·외부결제 수수료. 글로벌 — Apple 3.1.1, Google Play 확률 공개·가족 정책, 벨기에/네덜란드, 일본 콤프가챠·경품표시법, 중국 판호·미성년자, COPPA, GDPR/DSA, ATT. 수수료 — Apple 30/15%, Google 15/30%, 원스토어, Steam 30/25/20%·Steam Direct 100달러, Poki/CrazyGames, Roblox DevEx 현행 환율, Google Play Games on PC. 광고 — AppLovin MAX, Unity LevelPlay, AdMob 미디에이션·보상형 정책. 기술 — Unity(2024-09 런타임 요금 철회, Unity 6 요금제), Godot, Cocos Creator, Defold, Phaser, 백엔드(뒤끝·PlayFab·Firebase·Nakama·UGS·NHN Gamebase·Hive), 영수증 검증, 오프라인 시간 조작 방지, 분석·원격 설정·크래시. 출시 플레이북·체크리스트.
