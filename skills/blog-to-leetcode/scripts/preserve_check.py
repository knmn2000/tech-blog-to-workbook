"""Checks that a rewritten Markdown file kept what it must, against its committed version.

    py -P preserve_check.py <repo-dir> <file> [<file> ...]      # files relative to the repo dir

FAIL (must fix): a heading changed, a fenced code block changed, an outside or in-book link went
missing, a test id in a heading changed, a requirement id (R1, E2E) was added or removed, a table's
row count changed.
WARN (read it): numbers, inline code spans or table cells present before and absent now (or new),
and a word count far from the original. Exit status 1 when anything FAILs.
"""
import re
import subprocess
import sys
from pathlib import Path


def committed(repo: Path, rel: str) -> str:
    out = subprocess.run(["git", "-C", str(repo), "show", f"HEAD:{rel}"], capture_output=True, check=True)
    return out.stdout.decode("utf-8").replace("\r\n", "\n")


def parts(text: str) -> dict:
    fences = re.findall(r"```.*?```", text, flags=re.S)
    bare = re.sub(r"```.*?```", " ", text, flags=re.S)
    heads = [l.strip() for l in bare.split("\n") if re.match(r"#{1,4}\s", l)]
    links = set(re.findall(r"\]\(([^)\s]+)\)", bare)) | set(re.findall(r'href="([^"]+)"', bare))
    tables = []
    for block in re.findall(r"(?:^\|.*\n?)+", bare, flags=re.M):
        rows = [r for r in block.strip().split("\n")]
        tables.append(rows)
    reqs = set(re.findall(r"^\s*- \*\*(R\d+|E2E)\*\*", bare, flags=re.M))
    tests = re.findall(r"\(test `([^`]+)`\)", bare)
    prose = re.sub(r"<!--.*?-->", " ", bare, flags=re.S)
    nums = set(re.findall(r"(?<![\w.])-?\d[\d,]*\.?\d*(?:e\d+)?(?![\w])|0x[0-9a-fA-F]+", prose))
    codes = set(re.findall(r"`([^`\n]+)`", prose))
    cells = set()
    for rows in tables:
        for r in rows:
            cells |= {c.strip() for c in r.strip().strip("|").split("|") if c.strip()}
    words = len(re.sub(r"```.*?```", " ", text, flags=re.S).split())
    return dict(fences=fences, heads=heads, links=links, tables=tables, reqs=reqs, tests=tests,
                nums=nums, codes=codes, cells=cells, words=words)


def check(repo: Path, rel: str) -> int:
    old, new = parts(committed(repo, rel)), parts((repo / rel).read_text(encoding="utf-8").replace("\r\n", "\n"))
    fails, warns = [], []
    if old["heads"] != new["heads"]:
        gone = [h for h in old["heads"] if h not in new["heads"]]
        fails.append(f"headings changed: missing {gone[:4]}, new {[h for h in new['heads'] if h not in old['heads']][:4]}")
    if old["fences"] != new["fences"]:
        fails.append(f"fenced code changed ({len(old['fences'])} -> {len(new['fences'])} blocks, "
                     f"{sum(1 for a, b in zip(old['fences'], new['fences']) if a != b)} differ)")
    if old["links"] - new["links"]:
        fails.append(f"links missing: {sorted(old['links'] - new['links'])[:4]}")
    if old["tests"] != new["tests"]:
        fails.append("test ids in headings changed")
    if old["reqs"] != new["reqs"]:
        fails.append(f"requirement ids differ: -{sorted(old['reqs'] - new['reqs'])} +{sorted(new['reqs'] - old['reqs'])}")
    if [len(t) for t in old["tables"]] != [len(t) for t in new["tables"]]:
        fails.append("table row counts changed")
    for what in ("nums", "codes", "cells"):
        gone, added = sorted(old[what] - new[what]), sorted(new[what] - old[what])
        if gone:
            warns.append(f"{what} gone ({len(gone)}): {gone[:12]}")
        if added:
            warns.append(f"{what} new ({len(added)}): {added[:12]}")
    ratio = new["words"] / max(1, old["words"])
    if ratio < 0.6 or ratio > 1.15:
        warns.append(f"word count {old['words']} -> {new['words']} ({ratio:.2f}x)")
    status = "FAIL" if fails else ("warn" if warns else "ok")
    print(f"{status:4} {rel}  ({old['words']} -> {new['words']} words)")
    for f in fails:
        print("     FAIL", f)
    for w in warns:
        print("     warn", w)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    repo = Path(sys.argv[1])
    sys.exit(max(check(repo, rel) for rel in sys.argv[2:]))
