"""Runs the avoid-ai-writing skill's detector over a workbook's prose and prints one line per file:
score, label and its findings. Needs that skill installed (~/.claude/skills/avoid-ai-writing) and
Node.js. A finding is a prompt to look, as with slop_scan.py.

    py -P aiw_scan.py <workbook-folder>          the problem pages and READMEs
    py -P aiw_scan.py FILE... [--quiet]          --quiet: scores only
"""

import json
import subprocess
import sys
from pathlib import Path

CLI = Path.home() / ".claude" / "skills" / "avoid-ai-writing" / "bin" / "avoid-ai-writing.js"


def files_of(arg: str):
    path = Path(arg)
    if path.is_dir() and (path / "workbook.json").exists():
        return sorted((path / "problems").glob("*.md")) + [p for p in (path / "README.md",
                                                                       path / "starters" / "project" / "README.md") if p.exists()]
    if path.is_dir():
        return sorted(p for p in path.rglob("*.md") if "node_modules" not in p.parts)
    return [path]


def scan(path: Path) -> dict:
    mode = "rendered-markdown" if path.suffix.lower() == ".md" else "plain"
    out = subprocess.run(["node", str(CLI), "--source-mode", mode, "--context", "technical", str(path)],
                         capture_output=True, text=True, encoding="utf-8")
    if out.returncode != 0:
        return {"score": None, "label": out.stderr.strip()[:80], "issues": []}
    return json.loads(out.stdout)


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if not CLI.exists():
        sys.exit(f"The avoid-ai-writing skill isn't installed: {CLI} is missing.")
    quiet = "--quiet" in argv
    paths = [p for a in argv if a != "--quiet" for p in files_of(a)]
    if not paths:
        sys.exit(__doc__)
    total = 0
    for p in paths:
        d = scan(p)
        total += d["score"] or 0
        print(f"{d['score']!s:>4}  {d['label']:<24} {p}")
        if not quiet:
            for issue in d["issues"]:
                print(f"        {issue['severity']:<7} {issue['type']}: {issue['text'][:110]}")
    print(f"\n{len(paths)} files, total score {total}")


if __name__ == "__main__":
    main(sys.argv[1:])
