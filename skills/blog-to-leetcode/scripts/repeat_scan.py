"""The phrases that repeat across a workbook's pages: stock lines, announced dependencies, boilerplate.

    py -P scripts/repeat_scan.py <problems-dir> [words=7] [min-files=4] [rows=40]

Prints the longest-running repeats first with how many files carry them and one sample in
context. A page-by-page rewrite can't see these, so run it after the pages are written, then
vary or cut each family (references/voice.md, "The cross-page sweep").
"""
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from smell_metrics import prose  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
N = int(sys.argv[2]) if len(sys.argv) > 2 else 7
MIN_FILES = int(sys.argv[3]) if len(sys.argv) > 3 else 4
ROWS = int(sys.argv[4]) if len(sys.argv) > 4 else 40
d = Path(sys.argv[1])
where = defaultdict(set)
count = Counter()
sample = {}
for f in sorted(d.glob("*.md")):
    text = " ".join(prose(f.read_text(encoding="utf-8")))
    words = re.findall(r"[A-Za-z0-9'`<>_./-]+", text)
    low = [w.lower() for w in words]
    for i in range(len(low) - N + 1):
        g = " ".join(low[i:i + N])
        where[g].add(f.name[:2])
        count[g] += 1
        sample.setdefault(g, " ".join(words[max(0, i - 3):i + N + 6]))
rows = [(len(v), count[g], g) for g, v in where.items() if len(v) >= MIN_FILES]
rows.sort(reverse=True)
seen = []
for files, n, g in rows:
    if any(g in s or s in g for s in seen):
        continue
    seen.append(g)
    print(f"{files:2} files {n:3}x  {sample[g]}")
    if len(seen) >= ROWS:
        break
