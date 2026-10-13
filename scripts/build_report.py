"""Build an offline, dependency-free Korean research report from reviewed JSON."""
from pathlib import Path
from html import escape
import json
import re

ROOT = Path(__file__).resolve().parents[1]
FILES = ["roblox-global.json", "roblox-korea.json", "maple-worlds.json"]
MARKET_IDS = ["global", "korea", "maple"]
MARKET_NAMES = ["로블록스 해외", "로블록스 국내", "메이플스토리 월드"]


def read(name):
    return json.loads((ROOT / "research" / name).read_text(encoding="utf-8-sig"))


def txt(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return " · ".join(txt(v) for v in value)
    if isinstance(value, dict):
        return " · ".join(f"{k}: {txt(v)}" for k, v in value.items())
    return str(value)


def e(value):
    return escape(txt(value), quote=True)


def game_identity(game):
    url = game.get("url", "")
    roblox = re.search(r'roblox\.com/games/(\d+)', url)
    if roblox:
        return 'roblox:' + roblox.group(1)
    maple = re.search(r'/play/([a-f0-9]{32})', url)
    if maple:
        return 'maple:' + maple.group(1)
    return url.rstrip('/') or game["name"]


def link(url, title):
    if not isinstance(url, str) or not url.startswith(("https://", "http://")):
        return e(title)
    return f'<a href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(title)} <span aria-hidden="true">↗</span></a>'


def bullets(items):
    if not items:
        return ""
    if isinstance(items, str):
        items = [items]
    if isinstance(items, dict):
        labels = {"asOf": "기준일", "timezone": "시간대", "rankingLabel": "번호의 의미", "selection": "선정 방법", "koreaEvidence": "국내 인기 근거", "metrics": "지표 해석", "monetization": "과금 확인", "interpretation": "분석 해석", "effortAssumption": "구현 일정 가정", "limits": "조사 범위"}
        items = [f'{labels.get(k, k)}: {txt(v)}' for k, v in items.items()]
    return '<ul>' + ''.join(f'<li>{e(item)}</li>' for item in items) + '</ul>'


def recommendations(category, market_id):
    rows = []
    for rec in category.get("recommendations", []):
        rows.append(f'''<article class="idea-card">
          <div class="idea-meta"><span class="pill">{e(rec.get("difficulty", "범위 조절 필요"))}</span><span>{e(rec.get("effort", "일정 미정"))}</span></div>
          <h4>{e(rec.get("name"))}</h4><p>{e(rec.get("pitch"))}</p>
          <h5>첫 MVP</h5>{bullets(rec.get("mvp"))}
          <p class="reason"><strong>추천 근거</strong> {e(rec.get("why"))}</p>
          <p><strong>과금 제안</strong> {e(rec.get("monetization"))}</p>
          <p><strong>구현 난점</strong> {e(rec.get("risks"))}</p>
          <p class="next"><strong>첫 작업</strong> {e(rec.get("buildNext"))}</p>
        </article>''')
    return ''.join(rows)


def metrics(game):
    data = game.get("metrics", {})
    labels = {"playing": "전 세계 동접", "ccu": "전 세계 동접", "visits": "누적 방문", "likes": "좋아요", "favorites": "즐겨찾기", "totalPlayCount": "누적 플레이", "totalUserCount": "누적 이용자", "totalPlayerCount": "누적 이용자", "totalPlayers": "누적 이용자", "koreaChartPosition": "한국 차트 노출", "snapshotAt": "조회", "capturedAt": "조회", "source": "지표 출처", "voteRatio": "좋아요 비율", "upVotes": "좋아요", "downVotes": "싫어요", "positiveVotePercent": "좋아요 비율(%)", "approvalPct": "좋아요 비율(%)", "dislikes": "싫어요", "asOf": "조회", "measuredAt": "조회", "lastUpdated": "월드 갱신일", "metricLabel": "지표 범위", "unitNote": "지표 범위", "rolimonsGlobalRank": "Rolimon’s 전체 추적 순서", "rolimonsCCU": "보조 동접(Rolimon’s)", "koreanEvidence": "국내 근거", "observedDate": "조회 날짜", "scope": "지표 범위", "chartPosition": "한국 차트 노출", "chartPanel": "차트 구간"}
    values = []
    for key, value in data.items():
        if value is None or key in ("universeId", "placeId", "officialCcuIsRestricted"):
            continue
        if key.endswith("URL") or key.endswith("Url"):
            values.append(f'<span>{link(value, "지표 원문")}</span>')
            continue
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            value = f'{value:,}'
        values.append(f'<span><b>{e(labels.get(key, key))}</b> {e(value)}</span>')
    return '<div class="metrics">' + ''.join(values) + '</div>' if values else ''


def game_card(game, category, market_id):
    mon = game.get("monetization", {})
    verified = mon.get("verified", []) if isinstance(mon, dict) else []
    unverified = mon.get("unverified", "") if isinstance(mon, dict) else "세부 상품 미확인"
    summary = mon.get("summary", "") if isinstance(mon, dict) else mon
    evidence = game.get("evidence", [])
    sources = ''.join(f'<li>{link(s.get("url"), s.get("title", "근거"))}<span class="source-note">{e(s.get("type"))} · {e(s.get("note"))} · 확인 {e(s.get("accessed", "2026-10-13"))}</span></li>' for s in evidence)
    search = ' '.join([txt(game.get(k)) for k in ("name", "description", "features", "popularityFactors", "monetization")] + [txt(category.get("name")), MARKET_NAMES[MARKET_IDS.index(market_id)]]).lower()
    status = game.get("operatingStatus", game.get("operationStatus", game.get("status", "")))
    return f'''<article class="game-card" data-search="{e(search)}" data-name="{e(game.get('name'))}" data-evidence="{'verified' if mon.get('productEvidence', False) else 'limited'}">
      <div class="game-heading"><span class="rank" aria-label="선정 목록 {e(game.get('rank'))}번">{int(game.get('rank', 0)):02d}</span><div><h4>{link(game.get("url"), game.get("name"))}</h4><p class="game-desc">{e(game.get("description"))}</p></div></div>
      {f'<p class="operation">운영 상태 · {e(status)}</p>' if status else ''}
      {metrics(game)}
      <div class="game-body"><div><h5>특징</h5>{bullets(game.get("features"))}</div><div><h5>인기 요소 <span class="analysis-tag">해석</span></h5>{bullets(game.get("popularityFactors"))}</div><div class="payment"><h5>과금 탐색</h5><p>{e(summary)}</p>{f'<div class="verified"><b>확인된 정보</b>{bullets(verified)}</div>' if verified else '<span class="pill muted">개별 상품 확인 제한</span>'}{f'<p class="unverified"><b>미확인 범위</b> {e(unverified)}</p>' if unverified else ''}</div></div>
      <details class="game-sources"><summary>출처와 확인 범위 · {len(evidence)}개</summary><ul>{sources}</ul></details>
    </article>'''


def main():
    overview = read("overview.json")
    markets = [read(f) for f in FILES]
    category_count = sum(len(m["categories"]) for m in markets)
    games = [g for m in markets for c in m["categories"] for g in c["games"]]
    unique = len({game_identity(g) for g in games})
    rec_count = sum(len(c.get("recommendations", [])) for m in markets for c in m["categories"])
    sections, options, navigator = [], [], []
    for mi, market in enumerate(markets):
        mid = MARKET_IDS[mi]
        market_categories = []
        for ci, category in enumerate(market["categories"]):
            cid = f'{mid}-{ci+1}'
            options.append(f'<option value="{cid}" data-market="{mid}">{e(MARKET_NAMES[mi])} / {e(category["name"])}</option>')
            navigator.append(f'<a href="#{cid}"><span>{e(MARKET_NAMES[mi])}</span>{e(category["name"])}</a>')
            cards = ''.join(game_card(g, category, mid) for g in category["games"])
            market_categories.append(f'''<section id="{cid}" class="category" data-market="{mid}" data-category="{cid}">
              <div class="category-header"><div><p class="eyebrow">{e(MARKET_NAMES[mi])} / CATEGORY {ci+1:02d}</p><h3>{e(category["name"])}</h3><p class="category-basis">{e(category.get("selectionBasis"))}</p></div><span class="count-badge">Top {len(category["games"])}<small>선정 목록</small></span></div>
              <div class="common-box"><h4>카테고리 공통점 <span class="analysis-tag">해석</span></h4>{bullets(category.get("commonalities"))}</div>
              <div class="games">{cards}</div>
              <div class="category-ideas"><div class="section-heading"><h4>이 카테고리에서 만들어 볼 게임</h4><span>원작의 규칙을 참고한 독립 아이디어 · {len(category.get("recommendations", []))}개</span></div><div class="ideas-grid">{recommendations(category, mid)}</div></div>
            </section>''')
        sections.append(f'''<div class="market" data-market="{mid}"><div class="market-intro"><h2>{e(MARKET_NAMES[mi])}</h2><p>{e(market.get("scope"))}</p><details><summary>이 시장의 선정 방법</summary><div class="method-text">{bullets(market.get("methodology", []))}</div></details></div>{''.join(market_categories)}</div>''')
    insight_html = ''.join(f'<article class="insight"><span class="small-number">{i+1:02d}</span><h3>{e(x["title"])}</h3><p>{e(x["body"])}</p><p class="implication">{e(x["implication"])}</p><p class="reference">관찰 사례 · {e(x.get("examples"))}</p></article>' for i,x in enumerate(overview["insights"]))
    picks_html = ''.join(f'''<article class="pick"><p class="eyebrow">우선순위 {e(x["priority"])} · {e(x["engine"])}</p><h3>{e(x["name"])}</h3><p>{e(x["pitch"])}</p><dl><dt>MVP 범위</dt><dd>{e(x["scope"])}</dd><dt>구현 추정</dt><dd>{e(x["effort"])}</dd><dt>과금 제안</dt><dd>{e(x["monetization"])}</dd></dl><p><strong>선정 이유</strong> {e(x["reason"])}</p><p class="validation"><strong>먼저 확인할 것</strong> {e(x["validation"])}</p><p class="reference">설계 참고 · {e(x["references"])}</p></article>''' for x in overview["firstBuilds"])
    platforms_html = ''.join(f'<article class="platform-card"><h3>{e(x["name"])}</h3><p><strong>제작</strong> {e(x["build"])}</p><p><strong>수익화</strong> {e(x["payment"])}</p><p><strong>구현 포인트</strong> {e(x["implementation"])}</p><div class="link-row">'+''.join(link(s["url"],s["title"]) for s in x["links"])+ '</div></article>' for x in overview["platforms"])
    plans_html = ''.join(f'<article class="plan-step"><span>{e(x["step"])}</span><div><h3>{e(x["title"])}</h3><p>{e(x["body"])}</p></div></article>' for x in overview["buildPlan"])
    replacements = {
        "TITLE": e(overview["title"]), "SUBTITLE": e(overview["subtitle"]), "DATE": e(overview["date"]),
        "GAME_COUNT": str(len(games)), "UNIQUE_COUNT": str(unique), "CATEGORY_COUNT": str(category_count), "REC_COUNT": str(rec_count),
        "METHODS": bullets(overview["methodology"]), "INSIGHTS": insight_html, "PICKS": picks_html, "PLATFORMS": platforms_html,
        "PLANS": plans_html, "PROMPT": e(overview["starterPrompt"]), "CATEGORY_OPTIONS": ''.join(options), "NAVIGATOR": ''.join(navigator), "RESEARCH": ''.join(sections)
    }
    template = (ROOT / "scripts" / "report-template.html").read_text(encoding="utf-8")
    for key, value in replacements.items():
        template = template.replace('{{' + key + '}}', value)
    template = '\n'.join(line.rstrip() for line in template.splitlines()) + '\n'
    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    (docs / "index.html").write_text(template, encoding="utf-8")
    (docs / "report-data.json").write_text(json.dumps({"overview": overview, "markets": markets}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f'Built docs/index.html: {len(games)} entries, {unique} unique games, {category_count} categories, {rec_count} recommendations')


if __name__ == '__main__':
    main()
