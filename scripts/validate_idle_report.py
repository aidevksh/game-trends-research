"""Validate idle-game research coverage, provenance, identity, and offline report output."""
from pathlib import Path
from html.parser import HTMLParser
import json
import re
from build_idle_report import CONFIG, IDLE, ROOT, as_list, model_bucket

GAME_FIELDS = ('rank', 'id', 'name', 'url', 'developer', 'origin', 'release', 'platforms', 'description', 'coreLoop', 'features', 'progression', 'idleMechanics', 'popularityFactors', 'monetization', 'evidence', 'takeaways')
REC_FIELDS = ('name', 'pitch', 'mvp', 'difficulty', 'effort', 'monetization', 'why', 'risks', 'buildNext', 'kpiGate')
CAT_FIELDS = ('id', 'region', 'platformGroup', 'name', 'scope', 'selectionBasis', 'methodology', 'overview', 'commonalities', 'designPatterns', 'monetizationPatterns', 'risks', 'games', 'deepDive', 'recommendations')


class ReportParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.counts = {'game-card': 0, 'category': 0, 'idea-card': 0, 'deepdive': 0, 'concept': 0}
        self.ids = set()
        self.anchors = []
        self.external_assets = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = (attrs.get('class') or '').split()
        for k in self.counts:
            self.counts[k] += k in classes
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f"Duplicate DOM id: {attrs['id']}"
            self.ids.add(attrs['id'])
        if tag == 'a' and (attrs.get('href') or '').startswith('#'):
            self.anchors.append(attrs['href'][1:])
        if tag in ('script', 'img', 'link', 'iframe') and (attrs.get('src') or attrs.get('href') or '').startswith(('http:', 'https:', '//')):
            self.external_assets.append(attrs)


def check_source(s, where):
    assert isinstance(s, dict), f'Source must be an object: {where}'
    assert str(s.get('url', '')).startswith(('https://', 'http://')), f'Bad source URL: {where}'
    assert s.get('title') and s.get('accessed'), f'Source missing title/accessed: {where}'


def main():
    total_games, ideas, deepdives, ids = 0, 0, 0, set()
    for cfg in CONFIG['categories']:
        data = json.loads((IDLE / cfg['file']).read_text(encoding='utf-8-sig'))
        for f in CAT_FIELDS:
            assert data.get(f), f'{cfg["file"]}: missing {f}'
        assert data['id'] == cfg['id'], f'{cfg["file"]}: id mismatch'
        games = data['games']
        assert len(games) == cfg['expectedGames'], f'{cfg["file"]}: {len(games)} games'
        assert [g['rank'] for g in games] == list(range(1, len(games) + 1)), f'{cfg["file"]}: ranks'
        for g in games:
            where = f'{cfg["file"]} / {g.get("name")}'
            for f in GAME_FIELDS:
                assert g.get(f) not in (None, '', []), f'{where}: missing {f}'
            assert g['url'].startswith(('https://', 'http://')), f'{where}: url'
            mon = g['monetization']
            assert isinstance(mon, dict) and mon.get('summary') and mon.get('unverified'), f'{where}: monetization summary/unverified'
            assert any(s.get('url', '').rstrip('/') == g['url'].rstrip('/') for s in g['evidence']), f'{where}: url not in evidence'
            for s in g['evidence']:
                check_source(s, where)
            if mon.get('productEvidence'):
                assert as_list(mon.get('products')) or as_list(mon.get('verified')), f'{where}: productEvidence without products/verified'
            assert model_bucket(g), where
            key = g['id']
            assert key not in ids, f'Duplicate game id across categories: {key}'
            ids.add(key)
            total_games += 1
        dd = data['deepDive']
        assert dd.get('gameId') in {g['id'] for g in games}, f'{cfg["file"]}: deepDive gameId not in games'
        for s in as_list(dd.get('evidence')):
            check_source(s, f'{cfg["file"]} deepDive')
        deepdives += 1
        recs = data['recommendations']
        assert len(recs) >= 3, f'{cfg["file"]}: recommendations'
        for r in recs:
            for f in REC_FIELDS:
                assert r.get(f), f'{cfg["file"]}: recommendation {r.get("name")} missing {f}'
        ideas += len(recs)
    guides = {k: json.loads((IDLE / v).read_text(encoding='utf-8-sig')) for k, v in CONFIG['guides'].items()}
    ov = guides['overview']
    for f in ('date', 'title', 'subtitle', 'methodology', 'summary', 'criteria', 'directions', 'concepts', 'roadmap', 'starterPrompt'):
        assert ov.get(f), f'overview: missing {f}'
    for c in ov['concepts']:
        for f in ('name', 'pitch', 'why', 'coreLoop', 'systems', 'economy', 'monetization', 'kpi', 'team', 'risks'):
            assert c.get(f), f'overview concept {c.get("name")}: missing {f}'
    for k in ('marketStats', 'timeline', 'trends', 'benchmarks'):
        assert guides['market'].get(k), f'market: missing {k}'
    for k in ('formulas', 'krIdleRpgSystems', 'monetizationDesign', 'antiPatterns', 'taxonomy'):
        assert guides['design'].get(k), f'design-guide: missing {k}'
    for k in ('regulationsKR', 'storeEconomics', 'techStack', 'checklist'):
        assert guides['build'].get(k), f'build-guide: missing {k}'
    content = (ROOT / CONFIG['output']).read_text(encoding='utf-8')
    assert not re.search(r'\{\{[A-Z_]+\}\}', content), 'Unresolved template placeholder'
    assert '�' not in content, 'Unicode replacement character'
    parser = ReportParser()
    parser.feed(content)
    assert parser.counts['game-card'] == total_games, f'cards {parser.counts["game-card"]} != {total_games}'
    assert parser.counts['category'] == len(CONFIG['categories'])
    assert parser.counts['idea-card'] == ideas
    assert parser.counts['deepdive'] == deepdives
    assert parser.counts['concept'] == len(ov['concepts'])
    assert not parser.external_assets, f'Report requires network assets: {parser.external_assets[:2]}'
    missing = set(parser.anchors) - parser.ids
    assert not missing, f'Broken internal anchors: {sorted(missing)[:5]}'
    license_text = (ROOT / 'LICENSE').read_text(encoding='utf-8')
    assert 'Apache License' in license_text
    print(f'PASS: {parser.counts["category"]} categories / {total_games} games / {deepdives} deep dives / {ideas} ideas / {len(ov["concepts"])} concepts; fields, provenance, ids, anchors, offline assets checked.')


if __name__ == '__main__':
    main()
