"""Structural AI-smell metrics that the word-level scanners (slop_scan.py, aiw_scan.py) miss.

Run it before and after a prose pass and keep the numbers; references/voice.md says what to aim for.

    py -P smell_metrics.py <dir-or-file> [...]

Per group of Markdown files (prose only: code, tables and HTML are dropped) it prints
  sents    sentences, and mean words per sentence
  cv       coefficient of variation of sentence length (stdev / mean); flat text is low, ~0.5+ is human
  short    share of sentences under 7 words (fragments and quick lines are scarce in generated text)
  opener   share of paragraphs whose first two words match another paragraph's in the same file
  stock    hits of the stock phrases that announce structure ("later assignments", "adds to", ...)
  rep5     occurrences of 5-word phrases that appear in 3 or more files (liturgical repetition)
"""
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

STOCK = [
    r"\blater (assignments?|ones?|steps?)\b", r"\bno later assignment\b", r"\bused by assignments?\b",
    r"\badds? to\b", r"\bthis (module|class|header|file|program|page) (holds|declares|defines|reads|keeps|is)\b",
    r"\bone assignment at a time\b", r"\bearlier (assignments?|files?|ones?)\b",
    r"\bit needs (none|no) of\b", r"\byou (can|may) use\b", r"\bthe checker (runs|compares|feeds)\b",
    r"\bso (that )?(you|the)\b", r"\bin (this|your) (assignment|project)\b",
]
STOCK_RE = [re.compile(p, re.I) for p in STOCK]


def prose(text: str) -> list:
    """Paragraph strings with code, tables, HTML and markup removed."""
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"<(svg|figure)\b.*?</\1>", " ", text, flags=re.S)
    paras = []
    for block in re.split(r"\n\s*\n", text):
        lines = [l for l in block.split("\n") if l.strip() and not l.lstrip().startswith(("|", "#", "<", "!["))]
        if not lines:
            continue
        s = " ".join(re.sub(r"^\s*([-*]|\d+\.)\s+", "", l).strip() for l in lines)
        s = re.sub(r"`[^`]*`", "X", s)
        s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
        s = re.sub(r"[*_]", "", s)
        if len(s.split()) >= 3:
            paras.append(s)
    return paras


def sentences(paras: list) -> list:
    out = []
    for p in paras:
        for s in re.split(r"(?<=[.!?])\s+(?=[A-Z\"(])", p):
            n = len(s.split())
            if n:
                out.append(n)
    return out


def files(args):
    for a in args:
        p = Path(a)
        yield from sorted(p.rglob("*.md")) if p.is_dir() else [p]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    paths = list(files(sys.argv[1:]))
    lens, opener_hits, opener_total, stock, per_file_grams = [], 0, 0, Counter(), []
    for f in paths:
        paras = prose(f.read_text(encoding="utf-8"))
        lens += sentences(paras)
        firsts = [" ".join(p.lower().split()[:2]) for p in paras]
        c = Counter(firsts)
        opener_hits += sum(n for n in c.values() if n > 1)
        opener_total += len(firsts)
        joined = " ".join(paras)
        for rx in STOCK_RE:
            stock[rx.pattern] += len(rx.findall(joined))
        words = re.findall(r"[a-z']+", joined.lower())
        per_file_grams.append(Counter(" ".join(words[i:i + 5]) for i in range(len(words) - 4)))
    spread = Counter()
    for g in per_file_grams:
        spread.update(g.keys())
    rep5 = sum(c for g in per_file_grams for k, c in g.items() if spread[k] >= 3)
    distinct5 = sum(1 for k, n in spread.items() if n >= 3)
    mean = statistics.mean(lens) if lens else 0
    cv = statistics.pstdev(lens) / mean if mean else 0
    short = sum(1 for n in lens if n < 7) / len(lens) if lens else 0
    words_total = sum(lens)
    print(f"{len(paths)} files, {words_total} words | sents {len(lens)} (mean {mean:.1f}) | cv {cv:.2f} | short {short:.0%}"
          f" | opener {opener_hits / max(1, opener_total):.0%} | stock {sum(stock.values())} ({sum(stock.values()) * 1000 / max(1, words_total):.1f}/1k words)"
          f" | rep5 {rep5} in {distinct5} phrases")


if __name__ == "__main__":
    main()
