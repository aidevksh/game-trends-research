"""Validate research coverage, provenance, identity, and offline report output."""
from pathlib import Path
from html.parser import HTMLParser
import json
import re
from build_report import FILES, game_identity

ROOT = Path(__file__).resolve().parents[1]


class ReportParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cards = 0
        self.categories = 0
        self.ideas = 0
        self.ids = set()
        self.anchors = []
        self.external_assets = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get('class', '').split()
        self.cards += 'game-card' in classes
        self.categories += 'category' in classes
        self.ideas += 'idea-card' in classes
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f"Duplicate DOM id: {attrs['id']}"
            self.ids.add(attrs['id'])
        if tag == 'a' and attrs.get('href', '').startswith('#'):
            self.anchors.append(attrs['href'][1:])
        if tag in ('script', 'img', 'link') and attrs.get('src', attrs.get('href', '')).startswith(('http:', 'https:')):
            self.external_assets.append(attrs)


def main():
    all_games, recommendations = [], []
    for filename in FILES:
        data = json.loads((ROOT / 'research' / filename).read_text(encoding='utf-8-sig'))
        assert data.get('scope') and data.get('methodology'), f'Missing research method: {filename}'
        market_ids = []
        for category in data['categories']:
            assert 10 <= len(category['games']) <= 20, category['name']
            assert category.get('commonalities') and category.get('selectionBasis')
            assert [g['rank'] for g in category['games']] == list(range(1, len(category['games']) + 1))
            assert category.get('recommendations'), category['name']
            for rec in category['recommendations']:
                for field in ('name', 'pitch', 'mvp', 'difficulty', 'effort', 'monetization', 'why', 'risks', 'buildNext'):
                    assert rec.get(field), f'Missing {field}: {rec.get("name")}'
            recommendations.extend(category['recommendations'])
            for game in category['games']:
                for field in ('name', 'url', 'description', 'features', 'popularityFactors', 'monetization', 'evidence'):
                    assert game.get(field), f'Missing {field}: {game.get("name")}'
                assert game['url'].startswith(('https://www.roblox.com/games/', 'https://maplestoryworlds.nexon.com/'))
                assert game['monetization'].get('summary') and game['monetization'].get('unverified')
                assert any(s['url'] == game['url'] for s in game['evidence']), f'No official game source: {game["name"]}'
                for source in game['evidence']:
                    assert source.get('title') and source.get('note') and source.get('accessed')
                    assert source['url'].startswith(('https://', 'http://'))
                market_ids.append(game_identity(game))
                all_games.append(game)
        assert len(market_ids) == len(set(market_ids)), f'Duplicate game inside market: {filename}'
    content = (ROOT / 'docs' / 'index.html').read_text(encoding='utf-8')
    assert not re.search(r'\{\{[A-Z_]+\}\}', content), 'Unresolved template placeholder'
    assert '�' not in content, 'Unicode replacement character'
    parser = ReportParser()
    parser.feed(content)
    assert parser.cards == len(all_games) == 70
    assert parser.categories == 7
    assert parser.ideas == len(recommendations) == 18
    assert not parser.external_assets, 'Report requires network assets'
    assert set(parser.anchors) <= parser.ids, 'Broken internal anchors'
    license_text = (ROOT / 'LICENSE').read_text(encoding='utf-8')
    assert 'Apache License' in license_text and 'Version 2.0, January 2004' in license_text
    print(f'PASS: 7 categories / 70 entries / {len(set(map(game_identity, all_games)))} unique games / 18 recommendations; fields, provenance, anchors, offline assets, license checked.')


if __name__ == '__main__':
    main()
