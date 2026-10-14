"""Build the offline idle-game research report (docs/idle-games.html) from reviewed JSON."""
from pathlib import Path
from html import escape
import json
import math
import os
import re

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / 'research' / 'idle' / 'config.json').read_text(encoding='utf-8-sig'))
# IDLE_DATA_DIR / IDLE_OUT_DIR let a layout test build from sample data without touching docs/.
IDLE = Path(os.environ.get('IDLE_DATA_DIR') or ROOT / 'research' / 'idle')
OUT = Path(os.environ['IDLE_OUT_DIR']) if os.environ.get('IDLE_OUT_DIR') else None

MODEL_BUCKETS = ['IAP 중심', '혼합', '광고 중심', '유료 구매', '무료·기타']
MODEL_COLORS = ['var(--series-1)', 'var(--series-2)', 'var(--series-3)', 'var(--series-4)', 'var(--series-other)']
PLATFORM_BUCKETS = ['모바일', 'PC', '웹', '로블록스', '콘솔']
METRIC_LABELS = {'downloads': '다운로드', 'revenue': '매출', 'chart': '차트', 'rating': '평점·리뷰', 'ccu': '동접', 'players': '이용자·방문', 'other': '기타 지표'}


def read(name):
    return json.loads((IDLE / name).read_text(encoding='utf-8-sig'))


def txt(value):
    if value is None:
        return ''
    if isinstance(value, str):
        return value
    if isinstance(value, bool):
        return '예' if value else '아니오'
    if isinstance(value, (int, float)):
        return f'{value:,}' if isinstance(value, int) else f'{value:g}'
    if isinstance(value, list):
        return ' · '.join(txt(v) for v in value if v not in (None, ''))
    if isinstance(value, dict):
        return ' · '.join(f'{k}: {txt(v)}' for k, v in value.items() if v not in (None, ''))
    return str(value)


def e(value):
    return escape(txt(value), quote=True)


def as_list(value):
    if value is None or value == '':
        return []
    if isinstance(value, list):
        return [v for v in value if v not in (None, '')]
    return [value]


def slug(value):
    return re.sub(r'[^a-z0-9]+', '-', str(value).lower()).strip('-') or 'x'


def link(url, title, cls=''):
    if not isinstance(url, str) or not url.startswith(('https://', 'http://')):
        return e(title)
    c = f' class="{cls}"' if cls else ''
    return f'<a{c} href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(title)} <span aria-hidden="true">↗</span></a>'


def bullets(items, cls=''):
    items = as_list(items)
    if not items:
        return ''
    c = f' class="{cls}"' if cls else ''
    return f'<ul{c}>' + ''.join(f'<li>{e(i)}</li>' for i in items) + '</ul>'


def src(source, prefix='출처'):
    if not source:
        return ''
    if isinstance(source, list):
        return ' '.join(src(s, prefix if i == 0 else '') for i, s in enumerate(source))
    if isinstance(source, str):
        return f'<span class="src">{e(prefix + " · ") if prefix else ""}{e(source)}</span>'
    meta = ' · '.join(x for x in [txt(source.get('type')), txt(source.get('accessed'))] if x)
    head = f'{e(prefix)} · ' if prefix else ''
    return f'<span class="src">{head}{link(source.get("url"), source.get("title", "근거"))}{f" <small>({e(meta)})</small>" if meta else ""}</span>'


def source_list(sources):
    rows = []
    for s in as_list(sources):
        if not isinstance(s, dict):
            continue
        rows.append(f'<li>{link(s.get("url"), s.get("title", "근거"))}<span class="source-note">{e(s.get("type"))} · {e(s.get("note"))} · 확인 {e(s.get("accessed", "2026-10-14"))}</span></li>')
    return '<ul>' + ''.join(rows) + '</ul>' if rows else ''


def model_bucket(game):
    mon = game.get('monetization') or {}
    raw = txt(mon.get('model') if isinstance(mon, dict) else mon) or txt(game.get('businessModel'))
    if '혼합' in raw or ('광고' in raw and 'IAP' in raw and '중심' not in raw):
        return '혼합'
    if 'IAP' in raw or '인앱' in raw or '부분유료' in raw:
        return 'IAP 중심'
    if '광고' in raw:
        return '광고 중심'
    if '유료' in raw or '프리미엄' in raw or '구매' in raw:
        return '유료 구매'
    return '무료·기타'


def platform_buckets(game):
    found = []
    for p in as_list(game.get('platforms')):
        s = txt(p).lower()
        if any(k in s for k in ('android', 'ios', 'ipad', '모바일', 'mobile', 'iphone')):
            found.append('모바일')
        if any(k in s for k in ('pc', 'steam', 'windows', 'mac', 'linux', '데스크톱', 'epic')):
            found.append('PC')
        if any(k in s for k in ('웹', 'web', 'browser', '브라우저', 'html')):
            found.append('웹')
        if 'roblox' in s or '로블록스' in s:
            found.append('로블록스')
        if any(k in s for k in ('switch', 'playstation', 'ps4', 'ps5', 'xbox', '콘솔', 'console')):
            found.append('콘솔')
    return [b for b in PLATFORM_BUCKETS if b in found] or ['기타']


def nice_ticks(vmax, count=4):
    if vmax <= 0:
        return [0, 1]
    raw = vmax / count
    mag = 10 ** math.floor(math.log10(raw))
    for m in (1, 2, 2.5, 5, 10):
        step = m * mag
        if step * count >= vmax:
            break
    ticks, v = [], 0.0
    while v < vmax + step * 0.999:
        ticks.append(round(v, 10))
        v += step
    return ticks


def compact(n):
    if n is None:
        return ''
    a = abs(n)
    for div, suf in ((1e12, 'T'), (1e9, 'B'), (1e6, 'M'), (1e3, 'K')):
        if a >= div:
            s = f'{n / div:.1f}'.rstrip('0').rstrip('.')
            return s + suf
    return f'{n:g}'


def fmt_value(v, unit):
    if isinstance(v, (int, float)):
        s = f'{v:,.1f}'.rstrip('0').rstrip('.') if isinstance(v, float) and not float(v).is_integer() else f'{int(v):,}'
    else:
        s = txt(v)
    return f'{s}{unit}' if unit in ('%', '배') else (f'{s} {unit}' if unit else s)


def table_view(headers, rows, caption='표로 보기'):
    head = ''.join(f'<th>{e(h)}</th>' for h in headers)
    body = ''.join('<tr>' + ''.join(f'<td>{e(c)}</td>' for c in r) + '</tr>' for r in rows)
    return f'<details><summary>{e(caption)}</summary><div class="table-scroll"><table class="data-table compact"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div></details>'


def chart_card(cid, title, subtitle, body, table, source=None, note='', wide=False, legend=''):
    return (f'<figure class="chart-card{" wide" if wide else ""}" id="{e(cid)}"><figcaption><h4>{e(title)}</h4><p>{e(subtitle)}</p></figcaption>'
            f'{legend}{body}{table}{f"<p class=src>{e(note)}</p>" if note else ""}{f"<p>{src(source)}</p>" if source else ""}</figure>')


def column_chart(cid, title, subtitle, points, unit, source, note=''):
    """Single-series vertical columns drawn in HTML so labels stay legible at every width."""
    pts = [p for p in points if isinstance(p.get('y'), (int, float))]
    if len(pts) < 2:
        return ''
    ticks = nice_ticks(max(p['y'] for p in pts))
    top = ticks[-1]
    vmax = max(p['y'] for p in pts)
    label_all = len(pts) <= 7
    grid = ''.join(f'<span class="cc-tick" style="bottom:{t / top * 100:.2f}%"><i>{e(compact(t))}{e(unit if unit == "%" else "")}</i></span>' for t in ticks)
    cols = ''
    for i, p in enumerate(pts):
        val = fmt_value(p['y'], unit)
        show = label_all or i in (0, len(pts) - 1) or p['y'] == vmax
        tip = txt(p['x']) + (' · ' + txt(p.get('label')) if p.get('label') else '')
        cols += f'<div class="cc-col"><span class="cc-bar" style="height:{p["y"] / top * 100:.2f}%" tabindex="0" data-tip-value="{e(val)}" data-tip-label="{e(tip)}">{f"<b>{e(val)}</b>" if show else ""}</span></div>'
    xs = ''.join(f'<span>{e(p["x"])}</span>' for p in pts)
    body = f'<div class="cc" role="img" aria-label="{e(title)}"><div class="cc-plot">{grid}<div class="cc-cols">{cols}</div></div><div class="cc-xs">{xs}</div></div>'
    table = table_view(['구분', '값', '비고'], [[p['x'], fmt_value(p['y'], unit), txt(p.get('label'))] for p in pts])
    return chart_card(cid, title, subtitle, body, table, source, note)


def hbar_chart(cid, title, subtitle, points, unit, source, note='', wide=False, highlight=None):
    pts = sorted([p for p in points if isinstance(p.get('value'), (int, float))], key=lambda p: -p['value'])
    if not pts:
        return ''
    ticks = nice_ticks(max(p['value'] for p in pts))
    top = ticks[-1]
    rows = ''
    for p in pts:
        val = fmt_value(p['value'], unit)
        shown = compact(p['value']) if p['value'] >= 1e4 else val
        fill = 'var(--series-1)' if (highlight is None or p.get('label') == highlight) else 'var(--series-other)'
        tip = txt(p['label']) + (' · ' + txt(p.get('note')) if p.get('note') else '')
        rows += f'<div class="hb-row"><span class="hb-label">{e(p["label"])}</span><div class="hb-scale"><span class="hb-bar" style="width:{p["value"] / top * 100:.2f}%;background:{fill}" tabindex="0" data-tip-value="{e(val)}" data-tip-label="{e(tip)}"></span><b class="hb-val" style="left:{p["value"] / top * 100:.2f}%">{e(shown)}</b></div></div>'
    axis = ''.join(f'<span style="left:{t / top * 100:.2f}%">{e(compact(t))}</span>' for t in ticks)
    body = f'<div class="hb" role="img" aria-label="{e(title)}">{rows}<div class="hb-row hb-axis-row"><span class="hb-label"></span><div class="hb-axis">{axis}</div></div></div>'
    table = table_view(['항목', '값', '시점·비고'], [[p['label'], fmt_value(p['value'], unit), txt(p.get('note'))] for p in pts])
    return chart_card(cid, title, subtitle, body, table, source, note, wide)


def stacked_bm_chart(categories):
    rows, trows = '', []
    for cat in categories:
        counts = {b: 0 for b in MODEL_BUCKETS}
        for g in cat['games']:
            counts[model_bucket(g)] += 1
        segs = ''
        for bi, b in enumerate(MODEL_BUCKETS):
            n = counts[b]
            if not n:
                continue
            ink = '#ffffff' if bi == 0 else '#192b29'
            segs += f'<span class="sb-seg" style="flex:{n} 1 0;background:{MODEL_COLORS[bi]};color:{ink}" tabindex="0" data-tip-value="{e(f"{n}개")}" data-tip-label="{e(cat["name"] + " · " + b)}">{n}</span>'
        rows += f'<div class="sb-row"><span class="sb-label">{e(cat["name"])}</span><div class="sb-bar">{segs}</div></div>'
        trows.append([cat['name']] + [counts[b] for b in MODEL_BUCKETS])
    legend = '<ul class="legend">' + ''.join(f'<li><i style="background:{MODEL_COLORS[i]}"></i>{e(b)}</li>' for i, b in enumerate(MODEL_BUCKETS)) + '</ul>'
    body = f'<div class="sb" role="img" aria-label="하위 장르별 수익 모델 구성">{rows}</div>'
    table = table_view(['하위 장르'] + MODEL_BUCKETS, trows)
    return chart_card('bm-chart', '하위 장르별 수익 모델 구성 (각 10개)', '각 게임의 주 수익원을 연구자가 분류했습니다. 막대 안 숫자는 게임 수입니다.', body, table, wide=True, legend=legend)


# ---------------------------------------------------------------- sections

def summary_html(overview):
    out = []
    for i, x in enumerate(overview.get('summary', [])):
        out.append(f'<article class="exec"><span class="num">{i + 1:02d}</span><div><h3>{e(x.get("title"))}</h3><p>{e(x.get("body"))}</p>{f"<p class=implication>{e(x.get("implication"))}</p>" if x.get("implication") else ""}{f"<p class=evidence-line>근거 · {e(x.get("evidence"))}</p>" if x.get("evidence") else ""}</div></article>')
    return ''.join(out)


def kr_units(v):
    """1억 2,000만 style for large money/count values."""
    eok, man = divmod(int(round(v)), 100_000_000)
    man //= 10_000
    if eok and man:
        return f'{eok:,}억 {man:,}만' if man % 1000 else f'{eok + man / 10000:g}억'
    if eok:
        return f'{eok:,}억'
    return f'{man:,}만'


def stat_tile(stat):
    unit = txt(stat.get('unit'))
    value = stat.get('value')
    if isinstance(value, (int, float)) and unit in ('달러', '건', '명') and value >= 1_000_000:
        value = kr_units(value)
    shown = fmt_value(value, unit) if isinstance(value, (int, float)) else (txt(value) + (unit if unit and unit not in txt(value) and len(unit) <= 3 else ''))
    return f'<div class="stat-tile"><span class="label">{e(stat.get("label"))}</span><span class="value">{e(shown)}</span><span class="note">{e(" · ".join(x for x in [txt(stat.get("period")), txt(stat.get("region")), txt(stat.get("note"))] if x))}</span>{src(stat.get("source"))}</div>'


def market_html(market, overview):
    out = []
    stats = market.get('marketStats', [])
    hl_ids = overview.get('marketHighlights') or [s.get('id') for s in stats[:8]]
    by_id = {s.get('id'): s for s in stats}
    tiles = [by_id[i] for i in hl_ids if i in by_id]
    if market.get('summary'):
        out.append('<div class="cat-overview"><h4>시장 요약</h4>' + bullets(market['summary']) + '</div>')
    if tiles:
        out.append('<div class="kpi-row">' + ''.join(stat_tile(s) for s in tiles) + '</div>')
    charts = []
    for s in market.get('series', []):
        charts.append(column_chart('series-' + slug(s.get('id', s.get('title'))), s.get('title'), txt(s.get('note')) or txt(s.get('unit')), s.get('points', []), txt(s.get('unit')), s.get('source')))
    for c in overview.get('extraCharts', []):
        if c.get('section', 'market') == 'market':
            charts.append(hbar_chart(c['id'], c['title'], c.get('subtitle', ''), c['points'], c.get('unit', ''), c.get('source'), c.get('note', ''), c.get('wide', False), c.get('highlight')))
    charts = [c for c in charts if c]
    if charts:
        out.append('<div class="chart-grid">' + ''.join(charts) + '</div>')
    rest = [s for s in stats if s.get('id') not in hl_ids]
    if rest:
        rows = ''.join(f'<tr><th scope="row">{e(s.get("label"))}</th><td class="num">{e(fmt_value(s.get("value"), txt(s.get("unit"))) if isinstance(s.get("value"), (int, float)) else txt(s.get("value")) + " " + txt(s.get("unit")))}</td><td>{e(s.get("period"))}</td><td>{e(s.get("region"))}</td><td>{e(s.get("note"))}</td><td>{src(s.get("source"), "")}</td></tr>' for s in rest)
        out.append(f'<div class="sub-heading"><h3>추가 시장 지표</h3><span>정의와 시점이 서로 다릅니다. 같은 행끼리만 해석하세요.</span></div><div class="table-scroll"><table class="data-table"><thead><tr><th>지표</th><th class="num">값</th><th>기간</th><th>지역</th><th>정의·주의</th><th>출처</th></tr></thead><tbody>{rows}</tbody></table></div>')
    if market.get('topTitles'):
        rows = ''.join(f'<tr><th scope="row">{e(t.get("name"))}</th><td>{e(t.get("metric"))}</td><td><b>{e(t.get("value"))}</b></td><td>{e(t.get("period"))}</td><td>{e(t.get("note"))}</td><td>{src(t.get("source"), "")}</td></tr>' for t in market['topTitles'])
        out.append(f'<div class="sub-heading"><h3>대표작의 공개 성과 지표</h3><span>데이터 기업 추정치와 공식 발표가 섞여 있습니다. 기간·지역·지표 정의가 달라 순위로 비교하지 않습니다.</span></div><div class="table-scroll"><table class="data-table"><thead><tr><th>게임</th><th>지표</th><th>값</th><th>기간</th><th>비고</th><th>출처</th></tr></thead><tbody>{rows}</tbody></table></div>')
    if market.get('chartSnapshots'):
        cards = []
        for snap in market['chartSnapshots']:
            items = ''.join(f'<li><b>{e(x.get("rank"))}위</b> {e(x.get("name"))}{f" <small>({e(x.get("note"))})</small>" if x.get("note") else ""}</li>' for x in snap.get('entries', []))
            cards.append(f'<article class="info-card"><h4>{e(snap.get("store"))}</h4><p>{e(snap.get("date"))}</p><ul>{items}</ul><p class="ex">{src(snap.get("source"))}</p></article>')
        out.append('<div class="sub-heading"><h3>차트 스냅샷</h3><span>특정 시점의 순위입니다. 매출 순위와 인기(다운로드) 순위를 구분하세요.</span></div><div class="card-grid">' + ''.join(cards) + '</div>')
    if market.get('trends'):
        cards = ''.join(f'<article class="info-card"><h4>{e(t.get("title"))}</h4><p>{e(t.get("body"))}</p>{bullets(t.get("evidence"))}{f"<p class=implication>{e(t.get("implication"))}</p>" if t.get("implication") else ""}</article>' for t in market['trends'])
        out.append(f'<div class="sub-heading"><h3>2024~2026 핵심 트렌드</h3><span>트렌드별 근거와 신작 시사점</span></div><div class="card-grid">{cards}</div>')
    if market.get('timeline'):
        items = ''.join(f'<li><span class="t-date">{e(t.get("date"))}</span><span class="t-event">{e(t.get("event"))}</span><span class="t-sig">{e(t.get("significance"))}</span>{src(t.get("source"), "")}</li>' for t in market['timeline'])
        out.append(f'<div class="sub-heading"><h3>방치형 장르 연표</h3><span>장르를 바꾼 출시·기록·인수·규제</span></div><div class="timeline-wrap"><ol class="timeline">{items}</ol></div>')
    if market.get('benchmarks'):
        rows = ''.join(f'<tr><th scope="row">{e(b.get("metric"))}</th><td>{e(b.get("segment"))}</td><td><b>{e(b.get("value"))}</b></td><td>{e(b.get("note"))}</td><td>{src(b.get("source"), "")}</td></tr>' for b in market['benchmarks'])
        out.append(f'<div class="sub-heading"><h3>KPI 벤치마크</h3><span>리포트마다 표본·지역·정의가 다릅니다. 목표치는 같은 출처의 분위수끼리 비교하세요.</span></div><div class="table-scroll"><table class="data-table"><thead><tr><th>지표</th><th>구분</th><th>값</th><th>정의·표본</th><th>출처</th></tr></thead><tbody>{rows}</tbody></table></div>')
    if market.get('userInsights'):
        cards = ''.join(f'<article class="info-card"><h4>{e(u.get("value"))}</h4><p>{e(u.get("stat"))}</p>{f"<p class=ex>{e(u.get("note"))}</p>" if u.get("note") else ""}<p class="ex">{src(u.get("source"))}</p></article>' for u in market['userInsights'])
        out.append(f'<div class="sub-heading"><h3>이용자 인사이트</h3><span>설문·조사 기반 수치</span></div><div class="card-grid four">{cards}</div>')
    if market.get('regionNotes'):
        cards = ''.join(f'<article class="info-card tone"><h4>{e(r.get("region"))}</h4><p>{e(r.get("notes"))}</p><p class="ex">{src(r.get("sources"))}</p></article>' for r in market['regionNotes'])
        out.append(f'<div class="sub-heading"><h3>지역별 특성</h3><span>출시 지역 선택에 쓰는 요약</span></div><div class="card-grid">{cards}</div>')
    return ''.join(out)


FIT_CLASS = {'상': 'high', '중': 'mid', '하': 'low'}


def genres_html(design, categories, overview):
    out = []
    tax = design.get('taxonomy', [])
    if tax:
        rows = ''.join(f'<tr><th scope="row">{e(t.get("name"))}</th><td>{e(t.get("definition"))}</td><td>{e(t.get("coreLoop"))}</td><td>{e(t.get("monetization"))}</td><td>{e(t.get("examples"))}</td><td><span class="fit {FIT_CLASS.get(txt(t.get("smallTeamFit")), "mid")}">{e(t.get("smallTeamFit"))}</span><br><small>{e(t.get("fitReason"))}</small></td></tr>' for t in tax)
        out.append(f'<div class="table-scroll"><table class="data-table"><thead><tr><th>하위 장르</th><th>정의</th><th>핵심 루프</th><th>주 수익원</th><th>대표작</th><th>소규모 팀 적합도</th></tr></thead><tbody>{rows}</tbody></table></div>')
    charts = [stacked_bm_chart(categories)]
    for c in overview.get('extraCharts', []):
        if c.get('section') == 'genres':
            charts.append(hbar_chart(c['id'], c['title'], c.get('subtitle', ''), c['points'], c.get('unit', ''), c.get('source'), c.get('note', ''), c.get('wide', False), c.get('highlight')))
    out.append('<div class="sub-heading"><h3>100선의 수익 모델과 대표 지표</h3><span>장르마다 돈을 버는 방식이 다릅니다. 동접·매출 차트는 같은 정의의 수치끼리만 묶었습니다.</span></div><div class="chart-grid">' + ''.join(c for c in charts if c) + '</div>')
    rows = []
    for cat in categories:
        top = ', '.join(g['name'] for g in cat['games'][:3])
        counts = {b: 0 for b in MODEL_BUCKETS}
        for g in cat['games']:
            counts[model_bucket(g)] += 1
        mix = ' · '.join(f'{b} {n}' for b, n in counts.items() if n)
        verified = sum(1 for g in cat['games'] if (g.get('monetization') or {}).get('productEvidence'))
        risk = as_list(cat.get('risks'))[:1]
        rows.append(f'<tr><th scope="row"><a href="#cat-{e(cat["id"])}">{e(cat["name"])}</a></th><td>{e(cat.get("region"))} · {e(cat.get("platformGroup"))}</td><td>{e(top)}</td><td>{e(mix)}</td><td class="num">{verified}/10</td><td>{e(risk)}</td></tr>')
    out.append('<div class="sub-heading"><h3>하위 장르 10개 요약</h3><span>상품·가격 근거 수는 공식 스토어·확률 공시 등에서 실제 상품명·가격을 확인한 게임 수입니다.</span></div><div class="table-scroll"><table class="data-table"><thead><tr><th>하위 장르</th><th>지역·플랫폼</th><th>대표작(선정 1~3위)</th><th>수익 모델 분포</th><th class="num">상품 근거</th><th>신작 위험 요인</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>')
    return ''.join(out)


def score_cell(v):
    try:
        n = int(v)
    except (TypeError, ValueError):
        return f'<td>{e(v)}</td>'
    return f'<td data-v="{n}"><span class="score" aria-label="5점 중 {n}점">' + ''.join(f'<i class="{"on" if i < n else ""}"></i>' for i in range(5)) + f'</span><span class="score-num">{n}</span></td>'


def recommend_html(overview):
    out = []
    crit = overview.get('criteria', [])
    dirs = overview.get('directions', [])
    if crit and dirs:
        head = ''.join(f'<th data-sort="num" title="{e(c.get("desc"))}">{e(c.get("label"))}</th>' for c in crit)
        rows = ''
        for d in dirs:
            scores = d.get('scores', {})
            total = sum(int(scores.get(c['key'], 0)) * float(c.get('weight', 1)) for c in crit)
            rows += f'<tr><th scope="row">{e(d.get("name"))}<br><small class="muted">{e(d.get("example"))}</small></th>' + ''.join(score_cell(scores.get(c['key'])) for c in crit) + f'<td class="num" data-v="{total:.1f}"><b>{total:.1f}</b></td><td>{e(d.get("verdict"))}</td></tr>'
        legend = ' · '.join(f'{txt(c.get("label"))}(가중 {txt(c.get("weight", 1))}): {txt(c.get("desc"))}' for c in crit)
        out.append(f'<div class="sub-heading" style="border-top:0;padding-top:0;margin-top:0"><h3>후보 방향 비교</h3><span>연구자의 정성 평가(5점)입니다. 높을수록 유리합니다(경쟁 강도·개발 부담은 낮을수록 높은 점수). 머리글을 누르면 정렬됩니다.</span></div><div class="table-scroll"><table class="data-table sortable"><thead><tr><th data-sort="text">방향</th>{head}<th data-sort="num" class="num">가중 합계</th><th>판단</th></tr></thead><tbody>{rows}</tbody></table></div><p class="src">{e(legend)}</p>')
    concepts = []
    for c in overview.get('concepts', []):
        tags = '<ul class="concept-tags">' + ''.join(f'<li>{e(t)}</li>' for t in as_list(c.get('tags'))) + '</ul>'
        prod_rows = ''.join(f'<tr><td>{e(p.get("name"))}</td><td class="price">{e(p.get("price"))}</td><td>{e(p.get("contents"))}</td></tr>' for p in as_list(c.get('products')))
        products = f'<table class="products"><thead><tr><th>상품</th><th>가격(안)</th><th>구성·의도</th></tr></thead><tbody>{prod_rows}</tbody></table>' if prod_rows else ''
        blocks = [
            ('왜 지금, 왜 이것인가', bullets(c.get('why')), ''),
            ('타깃·플랫폼', f'<p><b>타깃</b> {e(c.get("target"))}</p><p><b>플랫폼</b> {e(c.get("platform"))}</p><p><b>포지셔닝</b> {e(c.get("positioning"))}</p>', ''),
            ('핵심 루프', ('<ol>' + ''.join(f'<li>{e(s)}</li>' for s in as_list(c.get('coreLoop'))) + '</ol>'), ''),
            ('출시 시스템 범위', bullets(c.get('systems')), ''),
            ('경제 설계 초안', bullets(c.get('economy')), 'dark'),
            ('과금 설계', bullets(c.get('monetization')) + products, ''),
            ('콘텐츠·라이브옵스 (첫 90일)', bullets(c.get('content')), ''),
            ('KPI 게이트', bullets(c.get('kpi')), ''),
            ('팀·일정', bullets(c.get('team')) + ('<ol>' + ''.join(f'<li>{e(s)}</li>' for s in as_list(c.get('timeline'))) + '</ol>' if c.get('timeline') else ''), ''),
            ('위험과 대응', bullets(c.get('risks')), 'warn'),
            ('설계 참고작', bullets(c.get('references')), ''),
            ('첫 2주 작업', bullets(c.get('firstSteps')), ''),
        ]
        grid = ''.join(f'<div class="concept-block {cls}"><h4>{e(t)}</h4>{body}</div>' for t, body, cls in blocks if body)
        concepts.append(f'<article class="concept" id="concept-{e(c.get("rank"))}"><div class="concept-head"><div><p class="eyebrow">추천 {e(c.get("rank"))} · {e(c.get("genre"))}</p><h3>{e(c.get("name"))}</h3><p class="pitch">{e(c.get("pitch"))}</p>{tags}</div></div><div class="concept-grid">{grid}</div></article>')
    if concepts:
        out.append('<div class="sub-heading"><h3>상용 기획안</h3><span>가격·수치는 근거 사례를 바탕으로 한 초기 가정이며, 소프트런칭 지표로 조정해야 합니다.</span></div><div class="concepts">' + ''.join(concepts) + '</div>')
    if overview.get('roadmap'):
        phases = ''.join(f'<article class="phase"><span class="ph-num">{e(p.get("phase"))}</span><h4>{e(p.get("title"))}</h4><span class="ph-dur">{e(p.get("duration"))}</span>{bullets(p.get("tasks"))}{f"<p class=gate><b>다음 단계 조건</b> {e(p.get("gate"))}</p>" if p.get("gate") else ""}</article>' for p in overview['roadmap'])
        out.append(f'<div class="sub-heading"><h3>제작·출시 로드맵</h3><span>각 단계의 통과 조건을 못 채우면 다음 단계 예산을 쓰지 않습니다.</span></div><div class="roadmap">{phases}</div>')
    if overview.get('starterPrompt'):
        out.append(f'<div class="prompt-box"><div class="section-heading"><h3>첫 프로토타입 요청문 (AI 코딩 도구용)</h3><button type="button" id="copy-prompt">요청문 복사</button></div><p id="starter-prompt">{e(overview["starterPrompt"])}</p><span id="copy-status" role="status" aria-live="polite"></span></div>')
    return ''.join(out)


def game_card(game, cat):
    mon = game.get('monetization') or {}
    if not isinstance(mon, dict):
        mon = {'summary': txt(mon)}
    model = model_bucket(game)
    plats = platform_buckets(game)
    gid = f'g-{cat["id"]}-{slug(game.get("id") or game.get("name"))}'
    search = ' '.join(txt(game.get(k)) for k in ('name', 'originalName', 'developer', 'publisher', 'origin', 'subgenre', 'businessModel', 'description', 'coreLoop', 'features', 'progression', 'idleMechanics', 'socialAndLiveOps', 'popularityFactors', 'userFeedback', 'takeaways'))
    search += ' ' + txt(mon.get('summary')) + ' ' + txt(mon.get('verified')) + ' ' + ' '.join(txt(p.get('name')) for p in as_list(mon.get('products')) if isinstance(p, dict)) + ' ' + txt(cat.get('name')) + ' ' + model + ' ' + ' '.join(plats)
    chips = []
    for label, key in (('개발', 'developer'), ('퍼블리셔', 'publisher'), ('국가', 'origin'), ('출시', 'release')):
        v = txt(game.get(key))
        if v and not (key == 'publisher' and v == txt(game.get('developer'))):
            chips.append(f'<li><b>{label}</b>{e(v)}</li>')
    if game.get('platforms'):
        chips.append(f'<li><b>플랫폼</b>{e(" · ".join(as_list(game.get("platforms"))))}</li>')
    if game.get('subgenre'):
        chips.append(f'<li><b>장르</b>{e(game.get("subgenre"))}</li>')
    chips.append(f'<li class="model">{e(model)}</li>')
    status = txt(game.get('status'))
    status_html = f'<p class="operation">운영 상태 · {e(status)}</p>' if status and status not in ('서비스 중', '운영 중') else ''
    metrics = game.get('metrics') or {}
    mhtml = ''.join(f'<span><b>{e(METRIC_LABELS.get(k, k))}</b>{e(v)}</span>' for k, v in metrics.items() if v not in (None, ''))
    mhtml = f'<div class="metrics">{mhtml}</div>' if mhtml else ''
    loop = as_list(game.get('coreLoop'))
    loop_html = ('<p class="loop-label">핵심 루프</p><ol class="loop-steps">' + ''.join(f'<li>{e(s)}</li>' for s in loop) + '<li class="back">↺ 반복</li></ol>') if loop else ''
    products = [p for p in as_list(mon.get('products')) if isinstance(p, dict)]
    prod_html = ''
    if products:
        prod_html = '<table class="products"><thead><tr><th>상품</th><th>가격</th><th>구성</th></tr></thead><tbody>' + ''.join(f'<tr><td>{e(p.get("name"))}</td><td class="price">{e(p.get("price"))}</td><td>{e(p.get("contents"))}</td></tr>' for p in products[:12]) + '</tbody></table>'
        if len(products) > 12:
            prod_html += f'<p class="unverified">외 {len(products) - 12}개 상품은 데이터 JSON 참고</p>'
    verified = as_list(mon.get('verified'))
    fb = game.get('userFeedback') or {}
    tk = game.get('takeaways') or {}
    fb_html = ''
    if fb:
        fb_html = f'<div class="feedback"><h5>유저 반응</h5>{"<p class=fb-label>좋은 평가</p>" + bullets(fb.get("positive"), "pos") if fb.get("positive") else ""}{"<p class=fb-label>불만·논란</p>" + bullets(fb.get("negative"), "neg") if fb.get("negative") else ""}{f"<p class=basis>근거 · {e(fb.get("basis"))}</p>" if fb.get("basis") else ""}</div>'
    tk_html = ''
    if tk:
        tk_html = f'<div class="takeaways"><div class="borrow"><h5>신작에 가져올 점</h5>{bullets(tk.get("borrow"))}</div><div class="avoid"><h5>피할 점</h5>{bullets(tk.get("avoid"))}</div></div>'
    foot = f'<div class="game-foot">{fb_html}{tk_html}</div>' if (fb_html or tk_html) else ''
    orig = txt(game.get('originalName'))
    title = f'{e(game.get("name"))}{f" <span class=orig>{e(orig)}</span>" if orig and orig != txt(game.get("name")) else ""}'
    url = game.get('url')
    h4 = f'<a href="{e(url)}" target="_blank" rel="noopener noreferrer">{title} <span aria-hidden="true">↗</span></a>' if isinstance(url, str) and url.startswith('http') else title
    evidence = as_list(game.get('evidence'))
    return f'''<article class="game-card" id="{e(gid)}" data-search="{e(search.lower())}" data-platform="{e("|".join(plats))}" data-model="{e(model)}" data-evidence="{"verified" if mon.get("productEvidence") else "limited"}">
<div class="game-heading"><span class="rank" aria-label="선정 목록 {e(game.get("rank"))}번">{int(game.get("rank", 0)):02d}</span><div class="gh-main"><h4>{h4}</h4><p class="game-desc">{e(game.get("description"))}</p><ul class="chips">{"".join(chips)}</ul></div></div>
{status_html}{mhtml}{loop_html}
<div class="game-body"><div><h5>특징</h5>{bullets(game.get("features"))}<h5>성장 시스템</h5>{bullets(game.get("progression"))}</div><div><h5>방치 메커닉</h5><p class="idle-box">{e(game.get("idleMechanics") or "미확인")}</p><h5>소셜·라이브옵스</h5>{bullets(game.get("socialAndLiveOps"))}<h5>인기 요인 <span class="analysis-tag">해석</span></h5>{bullets(game.get("popularityFactors"))}</div><div class="payment"><h5>과금 구조 · {e(mon.get("model") or model)}</h5><p>{e(mon.get("summary"))}</p>{prod_html}{f'<div class="verified"><b>확인된 정보</b>{bullets(verified)}</div>' if verified else '<span class="pill muted">개별 상품 확인 제한</span>'}{f'<p class="unverified"><b>미확인 범위</b> {e(mon.get("unverified"))}</p>' if mon.get("unverified") else ""}</div></div>
{foot}
<details class="game-sources"><summary>출처와 확인 범위 · {len(evidence)}개</summary>{source_list(evidence)}</details>
</article>'''


def deepdive_html(dd, cat):
    if not dd:
        return ''
    game = next((g for g in cat['games'] if g.get('id') == dd.get('gameId')), None)
    name = game['name'] if game else txt(dd.get('gameId'))
    parts = [f'<section class="deepdive" aria-label="{e(name)} 해부"><p class="eyebrow">DEEP DIVE · {e(cat["name"])}</p><h4>{e(name)} 해부</h4><p class="dd-title">{e(dd.get("title"))}</p><p class="dd-summary">{e(dd.get("summary"))}</p>']
    loop = [s for s in as_list(dd.get('coreLoop'))]
    if loop:
        items = ''.join(f'<li><b>{e(s.get("step") if isinstance(s, dict) else s)}</b><span>{e(s.get("detail") if isinstance(s, dict) else "")}</span></li>' for s in loop)
        parts.append(f'<h5>핵심 루프</h5><ol class="dd-loop">{items}</ol>')
    left = f'<div><h5>첫 접속 경험 (FTUE)</h5><ol>{"".join(f"<li>{e(x)}</li>" for x in as_list(dd.get("firstSession")))}</ol></div>' if dd.get('firstSession') else ''
    cur = as_list(dd.get('currencies'))
    cur_html = ''
    if cur:
        rows = ''.join(f'<tr><td><b>{e(c.get("name"))}</b>{" <small>(유료)</small>" if c.get("paid") else ""}</td><td>{e(c.get("earn"))}</td><td>{e(c.get("spend"))}</td></tr>' for c in cur if isinstance(c, dict))
        cur_html = f'<div><h5>재화 구조</h5><div class="table-scroll"><table class="dd-table"><thead><tr><th>재화</th><th>획득처</th><th>사용처</th></tr></thead><tbody>{rows}</tbody></table></div></div>'
    if left or cur_html:
        parts.append(f'<div class="dd-grid">{left}{cur_html}</div>')
    axes = as_list(dd.get('growthAxes'))
    if axes:
        rows = ''.join(f'<tr><td><b>{e(a.get("name"))}</b></td><td>{e(a.get("detail"))}</td><td>{e(a.get("monetized"))}</td></tr>' for a in axes if isinstance(a, dict))
        parts.append(f'<h5>성장 축과 과금 연결</h5><div class="table-scroll"><table class="dd-table"><thead><tr><th>성장 축</th><th>설명</th><th>과금</th></tr></thead><tbody>{rows}</tbody></table></div>')
    boxes = []
    gacha = dd.get('gacha')
    if isinstance(gacha, dict) and (gacha.get('pools') or gacha.get('rates')):
        boxes.append(f'<div><h5>뽑기·확률</h5><div class="dd-box"><p><b>종류</b> {e(gacha.get("pools"))}</p>{bullets(gacha.get("rates"))}<p><b>천장·보정</b> {e(gacha.get("pity") or "미확인")}</p><p><small>{e(gacha.get("source"))}</small></p></div></div>')
    if dd.get('offline'):
        boxes.append(f'<div><h5>오프라인 보상</h5><div class="dd-box"><p>{e(dd.get("offline"))}</p></div></div>')
    if dd.get('adPlacements'):
        boxes.append(f'<div><h5>광고 배치</h5><div class="dd-box">{bullets(dd.get("adPlacements"))}</div></div>')
    if dd.get('storeStructure'):
        boxes.append(f'<div><h5>상점 구성</h5><div class="dd-box">{bullets(dd.get("storeStructure"))}</div></div>')
    if dd.get('liveOpsCadence'):
        boxes.append(f'<div><h5>업데이트·이벤트 주기</h5><div class="dd-box">{bullets(dd.get("liveOpsCadence"))}</div></div>')
    if boxes:
        parts.append(f'<div class="dd-grid three">{"".join(boxes)}</div>')
    tl = as_list(dd.get('metricsTimeline'))
    if tl:
        items = ''.join(f'<li><b>{e(t.get("date"))}</b><span>{e(t.get("event"))}{" — " + e(t.get("value")) if t.get("value") else ""}</span></li>' for t in tl if isinstance(t, dict))
        parts.append(f'<h5>지표·사건 타임라인</h5><ol class="dd-timeline">{items}</ol>')
    sw = ''.join(f'<div><h5>{t}</h5>{bullets(dd.get(k))}</div>' for t, k in (('강점', 'strengths'), ('약점', 'weaknesses'), ('우리 신작에 적용할 교훈', 'lessons')) if dd.get(k))
    if sw:
        parts.append(f'<div class="dd-sw">{sw}</div>')
    if dd.get('evidence'):
        parts.append(f'<details class="game-sources"><summary>해부 출처 · {len(as_list(dd.get("evidence")))}개</summary>{source_list(dd.get("evidence"))}</details>')
    parts.append('</section>')
    return ''.join(parts)


def rec_card(rec):
    loop = as_list(rec.get('coreLoop'))
    return f'''<article class="idea-card"><div class="idea-meta"><span class="pill">{e(rec.get("difficulty", "범위 조절 필요"))}</span><span>{e(rec.get("effort", "일정 미정"))}</span></div>
<h4>{e(rec.get("name"))}</h4><p>{e(rec.get("pitch"))}</p>
<p class="kv"><strong>타깃</strong> {e(rec.get("target"))}</p><p class="kv"><strong>플랫폼</strong> {e(rec.get("platform"))}</p>
{('<h5>핵심 루프</h5><ol>' + ''.join(f'<li>{e(s)}</li>' for s in loop) + '</ol>') if loop else ''}
<h5>MVP 범위</h5>{bullets(rec.get("mvp"))}
<p class="kv"><strong>추천 근거</strong> {e(rec.get("why"))}</p><p class="kv"><strong>과금 설계</strong> {e(rec.get("monetization"))}</p><p class="kv"><strong>위험</strong> {e(rec.get("risks"))}</p>
{f'<p class="gate"><strong>KPI 게이트</strong> {e(rec.get("kpiGate"))}</p>' if rec.get("kpiGate") else ''}
<p class="next"><strong>첫 작업</strong> {e(rec.get("buildNext"))}</p></article>'''


def category_html(cat, index):
    cid = f'cat-{cat["id"]}'
    patterns = ''
    if cat.get('designPatterns') or cat.get('monetizationPatterns'):
        dp = ''.join(f'<div class="pattern"><b>{e(p.get("name"))}</b><p>{e(p.get("detail"))}</p><small>{e(p.get("examples"))}</small></div>' for p in as_list(cat.get('designPatterns')) if isinstance(p, dict))
        mp = ''.join(f'<div class="pattern"><b>{e(p.get("name"))}</b><p>{e(p.get("detail"))}</p><small>{e(p.get("examples"))}</small></div>' for p in as_list(cat.get('monetizationPatterns')) if isinstance(p, dict))
        patterns = f'<details class="patterns cat-extra" open><summary>설계 패턴 {len(as_list(cat.get("designPatterns")))}개 · 과금 패턴 {len(as_list(cat.get("monetizationPatterns")))}개</summary>{"<h5>설계 패턴</h5><div class=pattern-grid>" + dp + "</div>" if dp else ""}{"<h5>과금 패턴</h5><div class=pattern-grid>" + mp + "</div>" if mp else ""}</details>'
    pipeline = ''
    if cat.get('pipeline'):
        pipeline = '<div class="pipeline cat-extra"><h5>출시 예정·준비작 (목록 외)</h5><ul>' + ''.join(f'<li><b>{e(p.get("name"))}</b> — {e(p.get("note"))}</li>' for p in as_list(cat.get('pipeline')) if isinstance(p, dict)) + '</ul></div>'
    cards = ''.join(game_card(g, cat) for g in cat['games'])
    recs = ''.join(rec_card(r) for r in as_list(cat.get('recommendations')))
    method = f'<details class="cat-method cat-extra"><summary>이 장르의 조사 방법과 한계</summary><div class="method-text">{bullets(cat.get("methodology"))}{("<p><b>카테고리 출처</b></p>" + source_list(cat.get("sources"))) if cat.get("sources") else ""}</div></details>'
    return f'''<section id="{e(cid)}" class="category" data-region="{e(cat.get("region"))}" data-category="{e(cid)}">
<div class="category-header"><div><p class="eyebrow">CATEGORY {index:02d} · {e(cat.get("region"))} · {e(cat.get("platformGroup"))}</p><h3>{e(cat["name"])}</h3><p class="scope">{e(cat.get("scope"))}</p><p class="category-basis">{e(cat.get("selectionBasis"))}</p></div><span class="count-badge">{len(cat["games"])}선<small>연구자 선정</small></span></div>
<div class="cat-overview cat-extra"><h4>시장 개요</h4><p>{e(cat.get("overview"))}</p></div>
<div class="cat-two cat-extra"><div class="common-box"><h4>공통점 <span class="analysis-tag">해석</span></h4>{bullets(cat.get("commonalities"))}</div><div class="risk-box"><h4>신작 위험 요인</h4>{bullets(cat.get("risks"))}</div></div>
{patterns}{pipeline}
<div class="games">{cards}</div>
<div class="cat-extra">{deepdive_html(cat.get("deepDive"), cat)}</div>
<div class="category-ideas cat-extra"><div class="section-heading"><h4>이 장르에서 만들어 볼 신작</h4><span>원작 복제가 아닌 독립 기획 · {len(as_list(cat.get("recommendations")))}개</span></div><div class="ideas-grid">{recs}</div></div>
{method}
</section>'''


def key_metric(game):
    m = game.get('metrics') or {}
    for k in ('revenue', 'downloads', 'ccu', 'players', 'chart', 'rating'):
        if m.get(k):
            return f'{METRIC_LABELS[k]}: {txt(m[k])}'
    return ''


def date_key(value):
    m = re.search(r'(\d{4})(?:[-./년 ]+(\d{1,2}))?(?:[-./월 ]+(\d{1,2}))?', txt(value))
    if not m:
        return '9999'
    return f'{m.group(1)}-{int(m.group(2) or 1):02d}-{int(m.group(3) or 1):02d}'


def compare_html(categories):
    rows = []
    for ci, cat in enumerate(categories):
        for g in cat['games']:
            gid = f'g-{cat["id"]}-{slug(g.get("id") or g.get("name"))}'
            ev = (g.get('monetization') or {}).get('productEvidence')
            search = ' '.join(txt(x) for x in (g.get('name'), g.get('originalName'), cat['name'], g.get('origin'), g.get('platforms'), g.get('subgenre'), model_bucket(g), g.get('developer'))).lower()
            rows.append(f'<tr data-search="{e(search)}"><td data-v="{ci * 100 + int(g.get("rank", 0))}">{e(cat["name"])} <small class="muted">#{int(g.get("rank", 0))}</small></td><th scope="row"><a href="#{e(gid)}" data-jump-category>{e(g.get("name"))}</a></th><td>{e(g.get("origin"))}</td><td data-v="{date_key(g.get("release"))}">{e(g.get("release"))}</td><td>{e(" · ".join(platform_buckets(g)))}</td><td>{e(model_bucket(g))}</td><td>{e(g.get("subgenre"))}</td><td>{e(key_metric(g))}</td><td data-v="{1 if ev else 0}">{"확인" if ev else "<span class=muted>제한</span>"}</td></tr>')
    return f'''<div class="compare-tools"><input id="compare-search" type="search" placeholder="표 안에서 검색: 국가, 장르, 모델…" aria-label="비교표 검색"><span id="compare-count">{len(rows)} / {len(rows)}개</span></div>
<div class="table-scroll" style="max-height:720px"><table class="data-table sortable compact" id="compare-table"><thead><tr><th data-sort="num">하위 장르</th><th data-sort="text">게임</th><th data-sort="text">국가</th><th data-sort="text">출시</th><th data-sort="text">플랫폼</th><th data-sort="text">수익 모델</th><th data-sort="text">세부 장르</th><th>대표 지표 (정의 상이)</th><th data-sort="num">상품 근거</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>'''


SIM_HTML = '''<div class="sim" id="sim"><div class="section-heading" style="margin-bottom:6px"><h3 style="font-size:20px">경제 곡선 시뮬레이터</h3><span>생산 시설 1종을 레벨업하는 단순 모델입니다. 비용 = b × r^레벨, 초당 수익 = p × 레벨 × (마일스톤 배수)^(레벨÷간격) × 프레스티지 배수.</span></div>
<div class="sim-controls"><label for="sim-b">기본 비용 b<input id="sim-b" type="number" value="10" min="0.01" step="any"></label><label for="sim-r">비용 증가율 r<input id="sim-r" type="number" value="1.07" min="1.001" step="0.01"></label><label for="sim-p">레벨당 초당 생산 p<input id="sim-p" type="number" value="1" min="0.01" step="any"></label><label for="sim-step">마일스톤 간격(레벨)<input id="sim-step" type="number" value="25" min="1" step="1"></label><label for="sim-mult">마일스톤 배수<input id="sim-mult" type="number" value="2" min="1" step="0.5"></label><label for="sim-prestige">프레스티지 배수<input id="sim-prestige" type="number" value="1" min="1" step="0.5"></label></div>
<div class="compare-tools"><span>예시:</span><button type="button" data-sim-preset="4,1.07,1.67,25,2,1">AdCap 레모네이드 근사</button><button type="button" data-sim-preset="15,1.15,0.1,25,2,1">Cookie Clicker 커서 근사</button><button type="button" data-sim-preset="10,1.12,1,10,3,1">짧은 벽·큰 돌파</button><button type="button" data-sim-preset="10,1.07,1,25,2,10">프레스티지 ×10 이후</button></div>
<svg id="sim-chart" viewBox="0 0 900 300" role="img" aria-label="레벨별 다음 구매까지 대기 시간(로그 축)"></svg>
<div class="sim-out"><div><b id="sim-o1">-</b><span>Lv10→11 대기</span></div><div><b id="sim-o2">-</b><span>Lv100→101 대기</span></div><div><b id="sim-o3">-</b><span>Lv100까지 누적 시간</span></div><div><b id="sim-o4">-</b><span>Lv200까지 누적 시간</span></div></div>
<details><summary>표로 보기</summary><div class="table-scroll"><table class="data-table compact" id="sim-table"><thead><tr><th>레벨</th><th>다음 비용</th><th>초당 수익</th><th>대기</th><th>누적</th></tr></thead><tbody></tbody></table></div></details>
<p class="sim-note">세로축은 로그 눈금입니다. 마일스톤 직후 대기 시간이 떨어지고(돌파) 다시 오르는(벽) 톱니 모양이 방치형 페이싱의 기본 리듬입니다. 실제 게임은 여러 생산원·업그레이드·오프라인 보상이 겹치므로, 이 모델은 감 잡기용입니다. 예시값은 공개 위키 수치를 단순화한 근사입니다.</p></div>'''


def design_html(design):
    out = []
    if design.get('summary'):
        out.append('<div class="cat-overview"><h4>설계 원칙 요약</h4>' + bullets(design['summary']) + '</div>')
    if design.get('formulas'):
        cards = ''.join(f'<article class="formula"><h4>{e(f.get("name"))}</h4><code>{e(f.get("formula"))}</code><p>{e(f.get("explanation"))}</p>{f"<p class=tv><b>일반 값</b> {e(f.get("typicalValues"))}</p>" if f.get("typicalValues") else ""}{f"<p class=tv><b>사례</b> {e(f.get("examples"))}</p>" if f.get("examples") else ""}<p class="src">{src(f.get("source"))}</p></article>' for f in design['formulas'])
        out.append(f'<div class="sub-heading"><h3>핵심 공식</h3><span>비용·생산·프레스티지·오프라인 보상의 기본 수학</span></div><div class="formula-grid">{cards}</div>')
    out.append(SIM_HTML)
    if design.get('prestige'):
        rows = ''.join(f'<tr><th scope="row">{e(p.get("game"))}</th><td>{e(p.get("currency"))}</td><td><code>{e(p.get("formula"))}</code></td><td>{e(p.get("effect"))}</td><td>{src(p.get("source"), "")}</td></tr>' for p in design['prestige'])
        out.append(f'<div class="sub-heading"><h3>프레스티지(리셋) 공식 사례</h3><span>공개 위키·공식 자료로 확인한 수식</span></div><div class="table-scroll"><table class="data-table"><thead><tr><th>게임</th><th>재화</th><th>공식</th><th>효과</th><th>출처</th></tr></thead><tbody>{rows}</tbody></table></div>')
    if design.get('pacing'):
        rows = ''.join(f'<tr><th scope="row">{e(p.get("topic"))}</th><td>{e(p.get("guideline"))}</td><td>{e(p.get("rationale"))}</td><td>{src(p.get("source"), "")}</td></tr>' for p in design['pacing'])
        out.append(f'<div class="sub-heading"><h3>페이싱·세션 설계</h3><span>FTUE, 첫 프레스티지, 오프라인 상한, 알림</span></div><div class="table-scroll"><table class="data-table"><thead><tr><th>주제</th><th>가이드</th><th>근거·이유</th><th>출처</th></tr></thead><tbody>{rows}</tbody></table></div>')
    if design.get('krIdleRpgSystems'):
        rows = ''.join(f'<tr><th scope="row">{e(s.get("system"))}</th><td>{e(s.get("detail"))}</td><td>{e(s.get("monetization"))}</td><td>{e(s.get("examples"))}</td><td>{src(s.get("source"), "")}</td></tr>' for s in design['krIdleRpgSystems'])
        out.append(f'<div class="sub-heading"><h3>한국형 키우기 RPG 표준 시스템</h3><span>국내 매출 상위작에서 반복되는 시스템과 과금 연결</span></div><div class="table-scroll"><table class="data-table"><thead><tr><th>시스템</th><th>작동 방식</th><th>과금 연결</th><th>사례</th><th>출처</th></tr></thead><tbody>{rows}</tbody></table></div>')
    if design.get('monetizationDesign'):
        cards = ''.join(f'<article class="info-card"><h4>{e(m.get("pattern"))}</h4><p>{e(m.get("detail"))}</p>{f"<p class=implication>{e(m.get("bestPractice"))}</p>" if m.get("bestPractice") else ""}{f"<p class=ex><b>위험</b> {e(m.get("risk"))}</p>" if m.get("risk") else ""}{f"<p class=ex>사례 · {e(m.get("examples"))}</p>" if m.get("examples") else ""}<p class="ex">{src(m.get("source"))}</p></article>' for m in design['monetizationDesign'])
        out.append(f'<div class="sub-heading"><h3>수익화 설계 패턴</h3><span>광고·IAP·패스·구독·가챠의 배치와 주의점</span></div><div class="card-grid">{cards}</div>')
    if design.get('antiPatterns'):
        rows = ''.join(f'<tr><th scope="row">{e(a.get("issue"))}</th><td>{e(a.get("why"))}</td><td>{e(a.get("fix"))}</td><td>{e(a.get("examples"))}</td><td>{src(a.get("source"), "")}</td></tr>' for a in design['antiPatterns'])
        out.append(f'<div class="sub-heading"><h3>안티패턴과 해결책</h3><span>유저 이탈·리뷰 폭락·규제 위험으로 이어진 사례</span></div><div class="table-scroll"><table class="data-table"><thead><tr><th>문제</th><th>왜 문제인가</th><th>해결</th><th>사례</th><th>출처</th></tr></thead><tbody>{rows}</tbody></table></div>')
    if design.get('balancing'):
        items = ''.join(f'<article class="phase"><span class="ph-num">{i + 1}</span><h4>{e(b.get("step"))}</h4><p style="font-size:12px">{e(b.get("detail"))}</p>{f"<p class=gate><b>도구</b> {e(b.get("tools"))}</p>" if b.get("tools") else ""}<p class="src">{src(b.get("source"), "")}</p></article>' for i, b in enumerate(design['balancing']))
        out.append(f'<div class="sub-heading"><h3>밸런싱 절차</h3><span>스프레드시트 → 시뮬레이션 → 텔레메트리 → A/B</span></div><div class="roadmap">{items}</div>')
    if design.get('telemetry'):
        rows = ''.join(f'<tr><th scope="row"><code>{e(t.get("event"))}</code></th><td>{e(t.get("purpose"))}</td><td>{e(t.get("keyParams"))}</td></tr>' for t in design['telemetry'])
        out.append(f'<div class="sub-heading"><h3>필수 텔레메트리 이벤트</h3><span>출시 첫날부터 수집해야 밸런스·과금·리텐션 문제를 진단할 수 있습니다.</span></div><div class="table-scroll"><table class="data-table"><thead><tr><th>이벤트</th><th>목적</th><th>핵심 파라미터</th></tr></thead><tbody>{rows}</tbody></table></div>')
    if design.get('bigNumbers'):
        cards = ''.join(f'<article class="info-card"><h4>{e(b.get("topic"))}</h4><p>{e(b.get("detail"))}</p><p class="ex">{src(b.get("source"))}</p></article>' for b in design['bigNumbers'])
        out.append(f'<div class="sub-heading"><h3>큰 수 처리와 표기</h3><span>double 한계(약 1.8e308)를 넘는 인크리멘탈은 전용 라이브러리가 필요합니다.</span></div><div class="card-grid">{cards}</div>')
    if design.get('sources'):
        out.append(f'<details class="cat-method"><summary>설계 가이드 출처 · {len(design["sources"])}개</summary><div class="method-text">{source_list(design["sources"])}</div></details>')
    return ''.join(out)


def launch_html(build):
    out = []
    if build.get('disclaimer'):
        out.append(f'<p class="operation">{e(build["disclaimer"])}</p>')
    if build.get('regulationsKR'):
        rows = ''.join(f'<tr><th scope="row">{e(r.get("topic"))}</th><td>{e(r.get("rule"))}</td><td style="white-space:nowrap">{e(r.get("effective"))}</td><td>{e(r.get("whatToDo"))}</td><td>{e(r.get("penalty"))}</td><td>{src(r.get("source"), "")}</td></tr>' for r in build['regulationsKR'])
        out.append(f'<div class="sub-heading" style="border-top:0;padding-top:0"><h3>한국 규제</h3><span>확률 공개·등급·청약철회·다크패턴·개인정보·대리인 지정</span></div><div class="table-scroll"><table class="data-table"><thead><tr><th>주제</th><th>규정</th><th>시행</th><th>개발팀 조치</th><th>제재</th><th>출처</th></tr></thead><tbody>{rows}</tbody></table></div>')
    if build.get('regulationsGlobal'):
        rows = ''.join(f'<tr><th scope="row">{e(r.get("region"))}</th><td><b>{e(r.get("topic"))}</b><br>{e(r.get("rule"))}</td><td>{e(r.get("whatToDo"))}</td><td>{src(r.get("source"), "")}</td></tr>' for r in build['regulationsGlobal'])
        out.append(f'<div class="sub-heading"><h3>해외 규제·스토어 정책</h3><span>글로벌 출시 시 확인할 항목</span></div><div class="table-scroll"><table class="data-table"><thead><tr><th>지역·스토어</th><th>규정</th><th>조치</th><th>출처</th></tr></thead><tbody>{rows}</tbody></table></div>')
    if build.get('storeEconomics'):
        rows = ''.join(f'<tr><th scope="row">{e(s.get("platform"))}</th><td><b>{e(s.get("fee"))}</b></td><td>{e(s.get("notes"))}</td><td>{src(s.get("source"), "")}</td></tr>' for s in build['storeEconomics'])
        out.append(f'<div class="sub-heading"><h3>플랫폼 수수료·수익 구조</h3><span>순매출 계산과 플랫폼 선택의 기준</span></div><div class="table-scroll"><table class="data-table"><thead><tr><th>플랫폼</th><th>수수료</th><th>조건·비고</th><th>출처</th></tr></thead><tbody>{rows}</tbody></table></div>')
    if build.get('adMonetization'):
        cards = ''.join(f'<article class="info-card"><h4>{e(a.get("topic"))}</h4><p>{e(a.get("detail"))}</p><p class="ex">{src(a.get("source"))}</p></article>' for a in build['adMonetization'])
        out.append(f'<div class="sub-heading"><h3>광고 수익화 스택</h3><span>미디에이션·보상형 광고 정책·빈도</span></div><div class="card-grid">{cards}</div>')
    for layer in as_list(build.get('techStack')):
        if not isinstance(layer, dict):
            continue
        rows = ''.join(f'<tr><th scope="row">{e(o.get("name"))}</th><td>{e(o.get("pros"))}</td><td>{e(o.get("cons"))}</td><td>{e(o.get("cost"))}</td><td>{src(o.get("source"), "")}</td></tr>' for o in as_list(layer.get('options')) if isinstance(o, dict))
        out.append(f'<div class="sub-heading"><h3>기술 스택 · {e(layer.get("layer"))}</h3><span></span></div><div class="table-scroll"><table class="data-table"><thead><tr><th>선택지</th><th>장점</th><th>단점</th><th>비용</th><th>출처</th></tr></thead><tbody>{rows}</tbody></table></div>')
    if build.get('launchPlaybook'):
        items = ''.join(f'<li><span class="t-date">{e(p.get("phase"))}</span><span class="t-sig" style="color:var(--ink);font-size:13px">{e(p.get("detail"))}</span>{src(p.get("source"), "")}</li>' for p in build['launchPlaybook'])
        out.append(f'<div class="sub-heading"><h3>출시 플레이북</h3><span>사전예약부터 라이브옵스까지</span></div><ol class="timeline">{items}</ol>')
    if build.get('checklist'):
        groups = {}
        for c in build['checklist']:
            groups.setdefault(txt(c.get('area')) or '기타', []).append(c)
        html = []
        for area, items in groups.items():
            rows = ''.join(f'<label><input type="checkbox" data-key="{e(slug(area))}-{i}"><span class="prio {"must" if txt(c.get("priority")) == "필수" else ""}">{e(c.get("priority"))}</span><span>{e(c.get("item"))}</span></label>' for i, c in enumerate(items))
            html.append(f'<div class="check-group"><h4>{e(area)} <span class="check-count">0/{len(items)}</span></h4>{rows}</div>')
        out.append(f'<div class="sub-heading"><h3>출시 체크리스트</h3><span>체크 상태는 이 브라우저에만 저장됩니다.</span></div><div class="checklist">{"".join(html)}</div>')
    if build.get('sources'):
        out.append(f'<details class="cat-method"><summary>출시 가이드 출처 · {len(build["sources"])}개</summary><div class="method-text">{source_list(build["sources"])}</div></details>')
    return ''.join(out)


def collect_urls(obj, acc):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == 'url' and isinstance(v, str) and v.startswith('http'):
                acc.add(v.rstrip('/'))
            else:
                collect_urls(v, acc)
    elif isinstance(obj, list):
        for v in obj:
            collect_urls(v, acc)


def main():
    guides = CONFIG['guides']
    overview = read(guides['overview'])
    market = read(guides['market'])
    design = read(guides['design'])
    build = read(guides['build'])
    categories = [read(c['file']) for c in CONFIG['categories']]
    games = [g for c in categories for g in c['games']]
    urls = set()
    collect_urls([overview, market, design, build, categories], urls)
    regions = []
    for c in categories:
        if c.get('region') not in regions:
            regions.append(c.get('region'))
    plats = [p for p in PLATFORM_BUCKETS + ['기타'] if any(p in platform_buckets(g) for g in games)]
    navigator = ''.join(f'<a href="#cat-{e(c["id"])}"><span>{e(c.get("region"))} · {e(c.get("platformGroup"))}</span>{e(c["name"])}</a>' for c in categories)
    research = ''.join(category_html(c, i + 1) for i, c in enumerate(categories))
    deepdives = sum(1 for c in categories if c.get('deepDive'))
    ideas = sum(len(as_list(c.get('recommendations'))) for c in categories)
    replacements = {
        'TITLE': e(overview['title']), 'SUBTITLE': e(overview['subtitle']), 'DATE': e(overview['date']), 'INTRO': e(overview.get('intro')),
        'GAME_COUNT': str(len(games)), 'CATEGORY_COUNT': str(len(categories)), 'DEEPDIVE_COUNT': str(deepdives), 'IDEA_COUNT': str(ideas),
        'CONCEPT_COUNT': str(len(overview.get('concepts', []))), 'SOURCE_COUNT': f'{len(urls):,}', 'METHODS': bullets(overview.get('methodology')),
        'SUMMARY': summary_html(overview), 'MARKET': market_html(market, overview), 'GENRES': genres_html(design, categories, overview),
        'RECOMMEND': recommend_html(overview), 'NAVIGATOR': navigator,
        'REGION_OPTIONS': ''.join(f'<option value="{e(r)}">{e(r)}</option>' for r in regions),
        'CATEGORY_OPTIONS': ''.join(f'<option value="cat-{e(c["id"])}" data-region="{e(c.get("region"))}">{e(c["name"])}</option>' for c in categories),
        'PLATFORM_OPTIONS': ''.join(f'<option value="{e(p)}">{e(p)}</option>' for p in plats),
        'MODEL_OPTIONS': ''.join(f'<option value="{e(m)}">{e(m)}</option>' for m in MODEL_BUCKETS if any(model_bucket(g) == m for g in games)),
        'RESEARCH': research, 'COMPARE': compare_html(categories), 'DESIGN': design_html(design), 'LAUNCH': launch_html(build),
    }
    template = (ROOT / CONFIG['template']).read_text(encoding='utf-8')
    for key, value in replacements.items():
        template = template.replace('{{' + key + '}}', value)
    template = '\n'.join(line.rstrip() for line in template.splitlines()) + '\n'
    out_html = OUT / Path(CONFIG['output']).name if OUT else ROOT / CONFIG['output']
    out_data = OUT / Path(CONFIG['data']).name if OUT else ROOT / CONFIG['data']
    out_html.write_text(template, encoding='utf-8')
    out_data.write_text(json.dumps({'overview': overview, 'market': market, 'designGuide': design, 'buildGuide': build, 'categories': categories}, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Built {CONFIG["output"]}: {len(games)} games, {len(categories)} categories, {deepdives} deep dives, {ideas} ideas, {len(urls)} unique source URLs')


if __name__ == '__main__':
    main()
