#!/usr/bin/env python3
"""Run the Mira baseline test dataset against your n8n Chat Trigger and write documented results.

Usage:
  python scripts/run_baseline_tests.py --url https://YOUR-N8N-HOST/webhook/YOUR-WEBHOOK-ID/chat

Find the URL in n8n: open the Chat Trigger node -> Production URL (the chat page URL ends in /chat).
The workflow must be ACTIVE and the Chat Trigger set to Public.
Output: tests/test_results.md and tests/test_results.csv
Keyword syntax in the CSV: items split by '|' must ALL appear; inside an item 'a/b' means a OR b.
All checks are case-insensitive. Ground-truth task counts for T05 are computed from data/task_board.csv.
"""
import argparse, csv, json, time, urllib.request, uuid, os, re
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def ask(url, text, session):
    body = json.dumps({"action": "sendMessage", "sessionId": session, "chatInput": text}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=120) as r:
        data = json.loads(r.read().decode())
    return data.get("output") or data.get("text") or json.dumps(data), round(time.time() - t0, 1)

def has(item, text):
    return any(alt.strip().lower() in text.lower() for alt in item.split('/') if alt.strip())

def truth_counts():
    rows = list(csv.DictReader(open(os.path.join(ROOT, 'data', 'task_board.csv'), encoding='utf-8')))
    c = {}
    for r in rows: c[r['status']] = c.get(r['status'], 0) + 1
    return len(rows), c

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--url', required=True)
    ap.add_argument('--only', help='comma-separated test ids, e.g. T01,T05')
    a = ap.parse_args()
    tests = list(csv.DictReader(open(os.path.join(ROOT, 'tests', 'baseline_test_dataset.csv'), encoding='utf-8')))
    if a.only: tests = [t for t in tests if t['test_id'] in a.only.split(',')]
    total, counts = truth_counts()
    results, passed = [], 0
    for t in tests:
        try:
            out, secs = ask(a.url, t['input'], 'baseline-' + uuid.uuid4().hex[:8])
        except Exception as e:
            out, secs = 'ERROR: %s' % e, 0
        must = [x for x in t['must_contain'].split('|') if x]
        mustnot = [x for x in t['must_not_contain'].split('|') if x]
        missing = [x for x in must if not has(x, out)]
        forbidden = [x for x in mustnot if has(x, out)]
        # exact count check for the status report
        extra = ''
        if t['test_id'] == 'T05':
            for status, n in counts.items():
                if not re.search(r'%s\D{0,12}%d\b' % (re.escape(status), n), out, re.I):
                    extra += ' count-mismatch(%s should be %d)' % (status, n)
            if not re.search(r'\b%d\b' % total, out): extra += ' total-mismatch(%d)' % total
        ok = not missing and not forbidden and not extra and not out.startswith('ERROR')
        passed += ok
        results.append(dict(id=t['test_id'], category=t['category'], input=t['input'], output=out, seconds=secs,
                            missing=missing, forbidden=forbidden, extra=extra.strip(), result='Pass' if ok else 'Fail'))
        print('%s %s (%ss)' % (t['test_id'], 'PASS' if ok else 'FAIL', secs))
    with open(os.path.join(ROOT, 'tests', 'test_results.md'), 'w', encoding='utf-8') as f:
        f.write('# Baseline Test Results\n\nRun date: %s | Passed: %d / %d\n\n' % (date.today().isoformat(), passed, len(results)))
        f.write('Automated keyword check only. Review each output by hand for hallucinations and record your judgement in the last row of each table.\n\n')
        for r in results:
            f.write('## %s - %s\n\n| Field | Value |\n|---|---|\n' % (r['id'], r['category']))
            f.write('| Input | %s |\n| Seconds | %s |\n' % (r['input'], r['seconds']))
            f.write('| Expected keywords missing | %s |\n' % (', '.join(r['missing']) or 'none'))
            f.write('| Forbidden content found | %s |\n' % (', '.join(r['forbidden']) or 'none'))
            f.write('| Ground-truth check | %s |\n' % (r['extra'] or 'ok'))
            f.write('| Automated result | **%s** |\n| Hallucination detected (manual review) | TODO: No / Yes - describe |\n\n' % r['result'])
            f.write('**Output:**\n\n%s\n\n---\n\n' % r['output'])
    with open(os.path.join(ROOT, 'tests', 'test_results.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(['test_id', 'category', 'input', 'seconds', 'missing', 'forbidden', 'extra', 'result'])
        for r in results: w.writerow([r['id'], r['category'], r['input'], r['seconds'], ';'.join(r['missing']), ';'.join(r['forbidden']), r['extra'], r['result']])
    print('Passed %d / %d. Wrote tests/test_results.md and tests/test_results.csv' % (passed, len(results)))

if __name__ == '__main__':
    main()
