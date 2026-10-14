"""Generate placeholder idle data for a layout test build (never shipped)."""
import json, sys
from pathlib import Path

out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
cfg = json.loads(Path(sys.argv[2]).read_text(encoding='utf-8'))
S = lambda t: {"url": "https://example.com/" + t, "title": "샘플 출처 " + t, "type": "공식", "note": "샘플 확인 내용 한 줄입니다.", "accessed": "2026-10-14"}
models = ["IAP 중심", "혼합", "광고 중심", "유료 구매", "무료(코스메틱)"]
plats = [["Android", "iOS"], ["Android", "iOS", "PC(구글 플레이 게임즈)"], ["PC(Steam)"], ["웹", "PC(Steam)", "Android"], ["Roblox"]]
regions = {"kr-major": "국내", "kr-indie": "국내", "global-rpg": "해외"}
for ci, c in enumerate(cfg["categories"]):
    games = []
    for i in range(10):
        gid = f"{c['id']}-game-{i+1}"
        url = f"https://example.com/{gid}"
        games.append({
            "rank": i + 1, "id": gid, "name": f"샘플 게임 {ci+1}-{i+1} 키우기", "originalName": "Sample Idle RPG",
            "url": url, "developer": "샘플 스튜디오", "publisher": "샘플 퍼블리셔", "origin": "한국", "release": "2025-11-06 (글로벌)",
            "platforms": plats[(ci + i) % 5], "subgenre": "IP 방치형 RPG", "businessModel": "부분유료(IAP 중심)+보상형 광고", "status": "서비스 중" if i % 4 else "2026-08-05 업데이트 중단",
            "description": "자동 사냥으로 골드를 모으고 스탯을 강화하며 스테이지를 돌파하는 방치형 RPG. 동료·펫·스킬 뽑기로 전투력을 보강한다.",
            "coreLoop": ["자동 사냥으로 골드·장비 획득", "골드로 공격력·체력 강화", "스테이지 보스 도전", "막히면 던전·뽑기로 보강"],
            "features": ["특징 하나는 이렇게 길게 쓸 수 있다", "PC·모바일 크로스 세이브", "길드 레이드와 주간 랭킹", "확률 공시 페이지 운영"],
            "progression": ["골드 스탯 강화", "장비 뽑기·합성", "동료 수집·승급", "펫", "스킬", "유물"],
            "idleMechanics": "오프라인 최대 12시간 골드·경험치 누적. 광고 시청 시 2배.",
            "socialAndLiveOps": ["길드 레이드", "주간 랭킹", "2주 단위 이벤트", "시즌 패스"],
            "popularityFactors": ["익숙한 IP가 진입 장벽을 낮춤(해석)", "짧은 접속으로 성장 체감(해석)"],
            "monetization": {"model": models[(ci + i) % 5], "summary": "성장 패스·월정액·단계별 패키지 중심. 확률형 뽑기 상품은 공시 확률을 제공한다.",
                             "products": [{"name": "월정액 다이아", "price": "₩5,900", "contents": "30일간 매일 다이아", "evidence": "App Store"}, {"name": "성장 패스", "price": "₩11,000", "contents": "레벨 구간 보상", "evidence": "App Store"}] if i % 3 else [],
                             "verified": ["앱스토어 앱 내 구입 목록 확인", "확률 공시 페이지"], "unverified": "현재 한정 패키지 가격과 지역별 가격은 미확인.", "productEvidence": bool(i % 3)},
            "metrics": {"downloads": "Google Play 100만+ (2026-10-14)", "revenue": "출시 45일 1억 달러 (센서타워 추정, 2025-12-24)", "chart": "2026-09-11 구글플레이 매출 2위", "rating": "Google Play 4.4 (3.2만 리뷰)"},
            "userFeedback": {"positive": ["짧은 시간에 성장 체감", "원작 감성 재현"], "negative": ["후반 과금 압박", "확률 불만"], "basis": "Google Play 최근 리뷰·공식 커뮤니티"},
            "takeaways": {"borrow": ["첫 5분 안에 3번 강화", "오프라인 보상 화면 연출"], "avoid": ["팝업 상점 남발", "PvP 과금 격차"]},
            "evidence": [S(gid), {**S(gid), "url": url, "title": "공식 스토어"}]
        })
    data = {
        "id": c["id"], "region": regions.get(c["id"], "글로벌"), "platformGroup": "모바일", "name": f"샘플 카테고리 {c['id']}", "asOf": "2026-10-14",
        "scope": "이 카테고리가 다루는 범위를 한두 문장으로 설명한다.", "selectionBasis": "2026년 국내 매출 근거 순. 연구자 선정 목록이며 공식 전체 순위가 아님.",
        "methodology": ["조사 방법 1", "한계 2"], "overview": "시장 개요 문단입니다. " * 8,
        "commonalities": ["공통점 하나", "공통점 둘", "공통점 셋", "공통점 넷"],
        "designPatterns": [{"name": f"패턴 {k}", "detail": "작동 방식 설명입니다.", "examples": ["게임 A", "게임 B"]} for k in range(6)],
        "monetizationPatterns": [{"name": f"과금 {k}", "detail": "과금 패턴 설명", "examples": ["게임 A"]} for k in range(4)],
        "risks": ["위험 하나", "위험 둘", "위험 셋"], "pipeline": [{"name": "준비작", "note": "2026-11 예정"}] if ci == 0 else [],
        "games": games,
        "deepDive": {"gameId": games[0]["id"], "title": "왜 해부하나", "summary": "요약 " * 30, "firstSession": ["1", "2", "3", "4"],
                     "coreLoop": [{"step": "자동 사냥", "detail": "골드 획득"}, {"step": "강화", "detail": "스탯"}, {"step": "보스", "detail": "돌파"}, {"step": "뽑기", "detail": "보강"}],
                     "currencies": [{"name": "골드", "earn": "사냥", "spend": "강화", "paid": False}, {"name": "다이아", "earn": "결제·퀘스트", "spend": "뽑기", "paid": True}],
                     "growthAxes": [{"name": "스탯", "detail": "골드", "monetized": "무료"}], "gacha": {"pools": ["장비"], "rates": ["최고 0.01%"], "pity": "없음", "source": "공시"},
                     "offline": "최대 12시간", "adPlacements": ["2배 보상"], "storeStructure": ["월정액 ₩5,900"], "liveOpsCadence": ["2주 이벤트"],
                     "metricsTimeline": [{"date": "2025-11-06", "event": "출시", "value": ""}], "strengths": ["a"], "weaknesses": ["b"], "lessons": ["c"], "evidence": [S("dd")]},
        "recommendations": [{"name": f"아이디어 {k}", "pitch": "한 문장", "target": "타깃", "platform": "모바일", "coreLoop": ["a", "b", "c"], "mvp": ["x", "y"], "difficulty": "중간",
                             "effort": "3인 4~6개월", "monetization": "광고+IAP", "why": "근거", "risks": "위험", "kpiGate": "D1 40%", "buildNext": "첫 작업"} for k in range(3)],
        "sources": [S("cat")]
    }
    (out / c["file"]).write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
market = {"asOf": "2026-10-14", "summary": ["요약 1", "요약 2"],
          "marketStats": [{"id": f"s{k}", "label": "국내 모바일 매출 중 방치형 비중", "value": 16, "unit": "%", "period": "2024", "region": "한국", "note": "게임백서", "source": S("m")} for k in range(10)],
          "series": [{"id": "kr", "title": "국내 모바일 게임 매출 중 방치형 비중", "unit": "%", "points": [{"x": "2020", "y": 1.7}, {"x": "2021", "y": 4.2}, {"x": "2022", "y": 7.5}, {"x": "2023", "y": 11.0}, {"x": "2024", "y": 16}], "note": "게임백서", "source": S("s")}],
          "topTitles": [{"name": "메이플 키우기", "metric": "출시 45일 매출", "value": "1억 달러", "period": "2025-11~12", "note": "추정", "source": S("t")}],
          "chartSnapshots": [{"date": "2026-09-11", "store": "구글플레이 매출", "entries": [{"rank": 2, "name": "메이플 키우기"}], "source": S("c")}],
          "timeline": [{"date": "2013-08", "event": "Cookie Clicker", "significance": "장르의 시작", "source": S("tl")}],
          "trends": [{"title": "트렌드", "body": "본문", "evidence": ["근거"], "implication": "시사점"}],
          "benchmarks": [{"metric": "D1 리텐션", "segment": "아이들", "value": "35%", "note": "GameAnalytics 상위 25%", "source": S("b")}],
          "userInsights": [{"stat": "빠른 레벨업 위해 구매", "value": "46.0%", "note": "", "source": S("u")}],
          "regionNotes": [{"region": "한국", "notes": "메모", "sources": [S("r")]}]}
design = {"summary": ["원칙"], "taxonomy": [{"name": "방치형 RPG", "definition": "정의", "coreLoop": "루프", "monetization": "IAP", "examples": ["A"], "smallTeamFit": "중", "fitReason": "이유"}],
          "formulas": [{"name": "비용 증가", "formula": "cost_n = b × r^n", "explanation": "설명", "typicalValues": "1.07~1.15", "examples": "AdCap", "source": S("f")}],
          "prestige": [{"game": "AdCap", "currency": "엔젤", "formula": "150·√(E/1e15)", "effect": "+2%", "source": S("p")}],
          "pacing": [{"topic": "FTUE", "guideline": "30초", "rationale": "이유", "source": S("pc")}],
          "krIdleRpgSystems": [{"system": "스테이지", "detail": "설명", "monetization": "패스", "examples": ["A"], "source": S("k")}],
          "monetizationDesign": [{"pattern": "보상형 2배", "detail": "d", "bestPractice": "b", "risk": "r", "examples": ["A"], "source": S("md")}],
          "antiPatterns": [{"issue": "팝업 남발", "why": "w", "fix": "f", "examples": ["A"], "source": S("ap")}],
          "balancing": [{"step": "스프레드시트", "detail": "d", "tools": "Sheets", "source": S("bl")}], "telemetry": [{"event": "level_up", "purpose": "p", "keyParams": "k"}],
          "bigNumbers": [{"topic": "break_infinity", "detail": "d", "source": S("bn")}], "sources": [S("ds")]}
build = {"disclaimer": "법률 자문 아님", "regulationsKR": [{"topic": "확률 공개", "rule": "r", "effective": "2024-03-22", "whatToDo": "w", "penalty": "p", "source": S("rk")}],
         "regulationsGlobal": [{"region": "Apple", "topic": "3.1.1", "rule": "r", "whatToDo": "w", "source": S("rg")}],
         "storeEconomics": [{"platform": "Google Play", "fee": "15%/30%", "notes": "n", "source": S("se")}], "adMonetization": [{"topic": "MAX", "detail": "d", "source": S("am")}],
         "techStack": [{"layer": "엔진", "options": [{"name": "Unity", "pros": "p", "cons": "c", "cost": "무료~", "source": S("ts")}]}],
         "launchPlaybook": [{"phase": "사전예약", "detail": "d", "source": S("lp")}],
         "checklist": [{"area": "법무", "item": "확률 공시", "priority": "필수"}, {"area": "기술", "item": "서버 시간", "priority": "권장"}], "sources": [S("bs")]}
overview = {"date": "2026-10-14", "title": "방치형 게임, 무엇을 만들어야 하나", "subtitle": "부제", "intro": "소개", "methodology": ["m1"],
            "summary": [{"title": f"결론 {k}", "body": "본문", "implication": "시사점", "evidence": "근거"} for k in range(6)],
            "criteria": [{"key": "market", "label": "시장성", "weight": 1.5, "desc": "d"}, {"key": "team", "label": "소규모 적합", "weight": 1, "desc": "d"}],
            "directions": [{"name": "방향 A", "example": "예", "scores": {"market": 4, "team": 3}, "verdict": "판단"}],
            "concepts": [{"rank": "01", "genre": "장르", "name": "기획 A", "pitch": "p", "tags": ["t"], "why": ["w"], "target": "t", "platform": "p", "positioning": "p", "coreLoop": ["a"], "systems": ["s"], "economy": ["e"], "monetization": ["m"], "products": [{"name": "월정액", "price": "₩5,900", "contents": "c"}], "content": ["c"], "kpi": ["D1 40%"], "team": ["3인"], "timeline": ["M1"], "risks": ["r"], "references": ["ref"], "firstSteps": ["f"]}],
            "roadmap": [{"phase": "0", "title": "컨셉 검증", "duration": "2주", "tasks": ["t"], "gate": "g"}], "starterPrompt": "프롬프트",
            "extraCharts": [{"id": "ccu-steam", "section": "market", "title": "Steam 데스크톱 방치 최고 동접", "subtitle": "SteamDB 최고 동접", "unit": "명", "points": [{"label": "TBH: Task Bar Hero", "value": 526572, "note": "2026-06-14"}, {"label": "Banana", "value": 917272, "note": "2024-06"}, {"label": "Bongo Cat", "value": 200000, "note": "2025"}], "source": S("x")}]}
for name, obj in (("market.json", market), ("design-guide.json", design), ("build-guide.json", build), ("overview.json", overview)):
    (out / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
print("sample written to", out)
