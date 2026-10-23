"""Runs the avoid-ai-writing detector over a workbook's prose and prints one line per file:
score, label and its findings. A finding is a prompt to look, as with slop_scan.py.

It finds the detector in this order: the folder in AVOID_AI_WRITING_DIR, the avoid-ai-writing
skill in a skills folder under your home directory (Node.js runs its bin/avoid-ai-writing.js),
then an `avoid-ai-writing` command on your PATH (npm install -g avoid-ai-writing-detector).

    py -P aiw_scan.py <workbook-folder>          the problem pages and READMEs
    py -P aiw_scan.py FILE... [--quiet]          --quiet: scores only
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Where coding agents keep user-level skills; the first that has avoid-ai-writing wins.
SKILL_HOMES = [".agents", ".codex", ".cursor", ".gemini", ".copilot", ".claude",
               ".config/opencode", ".config/goose"]
INSTALL_HELP = ("The avoid-ai-writing detector wasn't found. Install the avoid-ai-writing skill "
                "(https://github.com/conorbronsdon/avoid-ai-writing) for your agent, set "
                "AVOID_AI_WRITING_DIR to its folder, or install the detector with "
                "`npm install -g avoid-ai-writing-detector`.")


def find_detector():
    """The command that runs the detector, as a list, or None."""
    dirs = [Path(os.environ["AVOID_AI_WRITING_DIR"])] if os.environ.get("AVOID_AI_WRITING_DIR") else []
    dirs += [Path.home() / home / "skills" / "avoid-ai-writing" for home in SKILL_HOMES]
    for d in dirs:
        script = d / "bin" / "avoid-ai-writing.js"
        if script.exists():
            return ["node", str(script)]
    command = shutil.which("avoid-ai-writing")
    return [command] if command else None


CLI = find_detector()


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
    out = subprocess.run(CLI + ["--source-mode", mode, "--context", "technical", str(path)],
                         capture_output=True, text=True, encoding="utf-8")
    if out.returncode != 0:
        return {"score": None, "label": out.stderr.strip()[:80], "issues": []}
    return json.loads(out.stdout)


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if not CLI:
        sys.exit(INSTALL_HELP)
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
