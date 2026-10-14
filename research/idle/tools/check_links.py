"""Check that source URLs in research JSON files resolve. Usage: python -I check_links.py out.json file1.json [file2.json ...]
403/429/5xx are reported as 'blocked/unknown' (bot protection), 404/410/DNS failures as 'broken'."""
import json
import sys
import ssl
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36'
CTX = ssl.create_default_context()


def collect(obj, where, acc):
    if isinstance(obj, dict):
        u = obj.get('url')
        if isinstance(u, str) and u.startswith('http'):
            acc.setdefault(u, set()).add(where)
        for k, v in obj.items():
            if k != 'url':
                collect(v, where, acc)
    elif isinstance(obj, list):
        for v in obj:
            collect(v, where, acc)


def check(url):
    for method in ('HEAD', 'GET'):
        req = urllib.request.Request(url, method=method, headers={'User-Agent': UA, 'Accept': 'text/html,application/json;q=0.9,*/*;q=0.8', 'Accept-Language': 'ko-KR,ko;q=0.9,en;q=0.8'})
        try:
            with urllib.request.urlopen(req, timeout=20, context=CTX) as r:
                return url, r.status, 'ok'
        except urllib.error.HTTPError as e:
            if method == 'HEAD' and e.code in (403, 405, 400, 404, 429, 500, 501, 503):
                continue
            kind = 'broken' if e.code in (404, 410) else 'blocked/unknown'
            return url, e.code, kind
        except Exception as e:  # DNS, TLS, timeout
            if method == 'HEAD':
                continue
            msg = str(e)
            kind = 'broken' if ('Name or service not known' in msg or 'getaddrinfo failed' in msg or 'nodename' in msg) else 'error/unknown'
            return url, None, f'{kind}: {msg[:80]}'
    return url, None, 'unknown'


def main():
    out, files = sys.argv[1], sys.argv[2:]
    acc = {}
    for f in files:
        data = json.load(open(f, encoding='utf-8-sig'))
        collect(data, f.split('/')[-1].split('\\')[-1], acc)
    with ThreadPoolExecutor(max_workers=16) as ex:
        results = list(ex.map(check, sorted(acc)))
    report = [{'url': u, 'status': s, 'kind': k, 'files': sorted(acc[u])} for u, s, k in results]
    json.dump(report, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    bad = [r for r in report if r['kind'].startswith('broken')]
    unk = [r for r in report if r['kind'] != 'ok' and not r['kind'].startswith('broken')]
    print(f'{len(report)} URLs: ok {len(report) - len(bad) - len(unk)}, broken {len(bad)}, blocked/unknown {len(unk)}')
    for r in bad:
        print('BROKEN', r['status'], r['url'], r['files'])


if __name__ == '__main__':
    main()
