"""Turn subagent JSONL transcripts into per-category research logs (no LLM needed).
Usage: python -I extract_transcripts.py <subagents_dir> <out_dir>
Each log lists every tool call (search query, fetched URL, shell command, sub-agent prompt)
followed by its result, so a later pass can rebuild the category JSON without re-searching."""
import json
import re
import sys
from pathlib import Path

MAIN = {
    'ac3ca8b8f42439120': 'kr-major', 'acf361b82959fb02c': 'kr-indie', 'a2e7b09317fcc591a': 'global-rpg',
    'a999102cbc1104803': 'hybrid', 'a1e9cd93290fc00ae': 'tycoon', 'a23f9543a01499160': 'arcade-idle',
    'aa2240ab448497788': 'desktop', 'a9a0af7dd2e8f69d7': 'incremental', 'ab348589ad5a7dac2': 'roblox',
    'a1fa970fd38e749d2': 'cozy', 'a94ec2b0a690d6909': 'market', 'a131d51fea5a61b39': 'design-guide',
    'a769a962fffa92155': 'build-guide',
}
LIMIT = {'Bash': 8000, 'Read': 3000, 'Write': 1500, 'Edit': 800}


def result_text(content):
    if isinstance(content, str):
        return content
    out = []
    for b in content or []:
        if isinstance(b, dict) and b.get('type') == 'text':
            out.append(b.get('text', ''))
    return '\n'.join(out)


def describe(name, inp):
    if name == 'WebSearch':
        return f"WebSearch ({inp.get('mode', '')}): {inp.get('query', '')}"
    if name == 'WebFetch':
        return f"WebFetch: {inp.get('url', '')}\n  prompt: {inp.get('prompt', '')[:300]}"
    if name == 'Bash':
        return 'Bash: ' + inp.get('command', '')[:1500]
    if name == 'Agent':
        return 'Agent (sub-agent): ' + inp.get('description', '') + '\n  prompt: ' + inp.get('prompt', '')[:2000]
    if name in ('Write', 'Edit', 'Read'):
        return f"{name}: {inp.get('file_path', '')}"
    return f'{name}: ' + json.dumps(inp, ensure_ascii=False)[:500]


def convert(path, label):
    calls, results, texts = [], {}, []
    for line in open(path, encoding='utf-8'):
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        m = d.get('message')
        if not isinstance(m, dict):
            continue
        content = m.get('content')
        if d.get('type') == 'assistant' and isinstance(content, list):
            for b in content:
                if b.get('type') == 'tool_use':
                    calls.append((b['id'], b.get('name', ''), b.get('input', {})))
                elif b.get('type') == 'text' and b.get('text', '').strip():
                    calls.append((None, '_text', b['text']))
        elif d.get('type') == 'user' and isinstance(content, list):
            for b in content:
                if b.get('type') == 'tool_result':
                    results[b.get('tool_use_id')] = result_text(b.get('content'))
    lines = [f'# Research log — {label}', f'source transcript: {Path(path).name}', '']
    n = 0
    for cid, name, inp in calls:
        if name == '_text':
            lines += ['> 에이전트 메모: ' + inp.strip().replace('\n', '\n> '), '']
            continue
        if name in ('ToolSearch', 'TaskStop', 'SendMessage'):
            continue
        n += 1
        res = results.get(cid, '(결과 없음)')
        lim = LIMIT.get(name)
        if lim and len(res) > lim:
            res = res[:lim] + f'\n…(이하 {len(res) - lim}자 생략)'
        if name == 'Write':
            res = '(파일 작성)'
        lines += [f'## [{n}] ' + describe(name, inp), '', res.strip(), '']
    return '\n'.join(lines), n


def main():
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    files = {p.stem.replace('agent-', ''): p for p in src.glob('agent-*.jsonl')}
    parent = {}
    for aid, p in files.items():
        if aid in MAIN:
            continue
        for mid in MAIN:
            if mid in files and aid in files[mid].read_text(encoding='utf-8'):
                parent[aid] = mid
                break
    for aid, p in sorted(files.items()):
        if aid in MAIN:
            label, name = MAIN[aid], MAIN[aid]
        else:
            pid = parent.get(aid)
            label = f'{MAIN.get(pid, "unknown")} 하위 에이전트 {aid}'
            name = f'{MAIN.get(pid, "unknown")}.sub-{aid}'
        text, n = convert(p, label)
        (out / f'{name}.log.md').write_text(text, encoding='utf-8')
        print(f'{name}.log.md  calls={n}  chars={len(text):,}')


if __name__ == '__main__':
    main()
