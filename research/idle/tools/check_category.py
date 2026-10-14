"""Quick per-file check of a category JSON against the report's required fields. Usage: python check_category.py research/idle/<id>.json"""
import json, sys
sys.path.insert(0, 'scripts')
from validate_idle_report import GAME_FIELDS, REC_FIELDS, CAT_FIELDS
for path in sys.argv[1:]:
    d = json.load(open(path, encoding='utf-8'))
    probs = [f'cat:{f}' for f in CAT_FIELDS if not d.get(f)]
    games = d.get('games', [])
    if len(games) != 10: probs.append(f'games={len(games)}')
    for g in games:
        miss = [f for f in GAME_FIELDS if g.get(f) in (None, '', [])]
        if miss: probs.append(f"{g.get('name')}: {miss}")
        if g.get('url') and not any(s.get('url','').rstrip('/') == g['url'].rstrip('/') for s in g.get('evidence', [])): probs.append(f"{g.get('name')}: url not in evidence")
        m = g.get('monetization') or {}
        if not (m.get('summary') and m.get('unverified')): probs.append(f"{g.get('name')}: monetization summary/unverified")
    dd = d.get('deepDive') or {}
    if dd.get('gameId') not in {g.get('id') for g in games}: probs.append('deepDive.gameId')
    for r in d.get('recommendations', []):
        miss = [f for f in REC_FIELDS if not r.get(f)]
        if miss: probs.append(f"rec {r.get('name')}: {miss}")
    print(path, 'status=' + str(d.get('status', 'final')), 'OK' if not probs else 'PROBLEMS: ' + ' | '.join(probs[:12]))
