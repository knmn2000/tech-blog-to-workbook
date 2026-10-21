"""Flags writing patterns that make text read as machine-written (the stop-slop rules, adapted in
references/authoring-guide.md section 8). A hit is a prompt to look, not a verdict: "every point
gets a marker" is a spec, "it is stored big-endian" can be the clearest way to say it.

    py -P slop_scan.py <workbook-folder>          the problem pages, READMEs, starters' comments,
                                                  workbook.json and the book's and checker's text
    py -P slop_scan.py FILE_OR_FOLDER... [--only DASH,FILLER] [--skip PASSIVE] [--summary]

Categories: DASH, FILLER, ADVERB, ABSOLUTE, CONTRAST, META, QUESTION, PASSIVE, WH, SHORT, OPENER.
"""

import re
import sys
from collections import Counter
from pathlib import Path

LY_WORDS = set("""only early family apply reply supply assembly rely ally fly poly anomaly multiply
comply imply july ugly belly holy jelly rally tally italy friendly daily weekly monthly yearly hourly
costly lonely lovely silly elderly orderly butterfly firefly curly bully wily oily hilly chilly
smelly underly homely monopoly readonly""".split())

PASSIVE_VERBS = (r"\w+ed|written|given|made|done|shown|seen|known|built|read|kept|run|taken|found|"
                 r"drawn|set|put|left|meant|chosen|broken|thrown|held|sent|told|said|stored|split|cut")

CHECKS = [
    ("DASH", re.compile("—|\\s–\\s|\\s--\\s")),
    ("FILLER", re.compile(r"\b(just|really|simply|actually|basically|exactly|very|quite|truly|literally|"
                          r"essentially|honestly|obviously|definitely|certainly|of course|indeed)\b", re.I)),
    ("ADVERB", re.compile(r"\b[A-Za-z]+ly\b")),
    ("ABSOLUTE", re.compile(r"\b(always|never|everything|everyone|everybody|nobody|no one|entirely|"
                            r"totally|completely)\b", re.I)),
    ("CONTRAST", re.compile(r"\bnot (just|only|merely|simply)\b|\b(isn't|aren't|is not|are not)\b[^.;]{0,60}"
                            r"[,;.]\s*(it's|it is|they're|they are)\b|\bnot\b[^.;:()]{1,40},\s*but\b", re.I)),
    ("META", re.compile(r"\b(note that|keep in mind|remember that|it's worth|worth noting|let's|let us|"
                        r"here's|here is the|in other words|that said|in short|simply put|as mentioned|"
                        r"the key (is|here)|crucial|essential|importantly|powerful|seamless|robust|leverage|"
                        r"delve|dive into|deep dive|journey|unlock|elevate|game.changer|landscape|"
                        r"under the hood|the magic|don't worry|feel free)\b", re.I)),
    ("QUESTION", re.compile(r"[A-Za-z)]\?(?=\s|$|['\"`<*])")),
    ("PASSIVE", re.compile(rf"\b(is|are|was|were|be|been|being|gets|get|got)\s+(?:\w+ly\s+)?({PASSIVE_VERBS})\b",
                           re.I)),
    ("WH", re.compile(r"(?:^|[.!:]\s+|^\s*[-*>]\s+)(What|When|Where|Why|How|Which)\b(?![^.!]*\?)")),
    ("SHORT", re.compile(r"(?:^|[.!?]\s+)([A-Z][a-z']*(?:\s+[a-z']+){0,2}\.)(?=\s|$)")),
    ("OPENER", re.compile(r"(?:^|[.!?]\s+)(So|Look|Now|Well|Remember),? ")),
]

CODE_SUFFIXES = {".cpp", ".cc", ".c", ".h", ".hpp", ".rs", ".go", ".java", ".ts", ".js", ".cs", ".swift", ".kt"}


def prose_lines(path: Path):
    """(line number, text) for the parts of the file a learner reads as prose."""
    text = path.read_text(encoding="utf-8", errors="replace")
    suffix = path.suffix.lower()
    in_fence = in_comment = False
    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if suffix == ".md":
            if stripped.startswith("#"):
                continue  # headings: the book parses some of them, and pages link to others
            if stripped.startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            if "<!--" in line:
                in_comment = "-->" not in line
                continue
            if in_comment:
                in_comment = "-->" not in line
                continue
        elif suffix in CODE_SUFFIXES:
            # Starters: only the comments are prose.
            match = re.search(r"//(.*)|^\s*/?\*+(.*)", line)
            if not match:
                continue
            line = match.group(1) or match.group(2) or ""
        elif suffix == ".py":
            if stripped.startswith("#") or not re.search(r"[\"'][^\"']*\w+ \w+ \w+", line):
                continue
        elif suffix in (".html", ".htm"):
            if stripped.startswith(("//", "/*", "*")) or re.match(r"^[.#@\w-][^\"'`]*\{|^[\w-]+\s*:[^\"'`]*;$", stripped):
                continue
        yield number, line


def clean(line: str) -> str:
    line = re.sub(r"`[^`]*`", "`x`", line)                      # inline code
    line = re.sub(r"\]\([^)]*\)|https?://\S+", "]", line)        # link targets
    line = re.sub(r"<[^>]+>", " ", line)                          # tags
    return line


def scan(path: Path, only, skip):
    hits = []
    for number, line in prose_lines(path):
        text = clean(line)
        for name, pattern in CHECKS:
            if (only and name not in only) or name in skip:
                continue
            for m in pattern.finditer(text):
                word = m.group(0).strip()
                if name == "ADVERB" and word.lower() in LY_WORDS:
                    continue
                if name == "SHORT" and len(m.group(1).split()) > 3:
                    continue
                start = max(0, m.start() - 50)
                context = " ".join(text[start:m.end() + 50].split())
                hits.append((path, number, name, word, context))
    return hits


def workbook_files(root: Path):
    files = sorted((root / "problems").glob("*.md"))
    files += [p for p in [root / "README.md", root / "workbook.json", root / "tools" / "book_template.html",
                          root / "tools" / "check.py", root / "tools" / "serve.py"] if p.exists()]
    files += [p for p in sorted((root / "starters").rglob("*")) if p.is_file()
              and (p.suffix.lower() in CODE_SUFFIXES or p.suffix.lower() == ".md")]
    return files


def expand(arg: str):
    path = Path(arg)
    if path.is_dir() and (path / "workbook.json").exists():
        return workbook_files(path)
    if path.is_dir():
        return [p for p in sorted(path.rglob("*")) if p.is_file() and p.suffix.lower()
                in CODE_SUFFIXES | {".md", ".html", ".py", ".json"}]
    return [path]


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # pages quote maths symbols
    only, skip, summary, paths = set(), set(), False, []
    args = iter(argv)
    for arg in args:
        if arg == "--only":
            only = set(next(args).upper().split(","))
        elif arg == "--skip":
            skip = set(next(args).upper().split(","))
        elif arg == "--summary":
            summary = True
        else:
            paths.append(arg)
    if not paths:
        sys.exit(__doc__)
    hits = [h for arg in paths for f in expand(arg) for h in scan(f, only, skip)]
    if not summary:
        for path, number, name, word, context in hits:
            print(f"{path}:{number}: {name:8} {word!r:24} {context}")
    by_name = Counter(h[2] for h in hits)
    by_file = Counter(str(h[0]) for h in hits)
    print(f"\n{len(hits)} hits: " + ", ".join(f"{k} {v}" for k, v in by_name.most_common()))
    if summary:
        for name, count in by_file.most_common():
            print(f"  {count:4}  {name}")


if __name__ == "__main__":
    main(sys.argv[1:])
