"""Creates a new workbook folder from the skill's template.

    python new_workbook.py --dest ../log-workbook --title "The Log Workbook" \
        --source-url https://... --source-title "The Log: ..." --author "Jay Kreps" --lang python

Copies assets/workbook-template (checker, image comparison, case-file library, book
builder, check scripts, README, authoring guide) and the language's files from
assets/lang/<lang>, then writes workbook.json with the book's metadata and an empty
checkpoint list. Register checkpoints in workbook.json before writing them.
"""

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL / "assets" / "workbook-template"
LANGS = SKILL / "assets" / "lang"
PY = "py -P" if sys.platform == "win32" else "python3 -P"

RUN = {
    "cpp": {
        "setup": {"command": "cmake -S . -B build -G Ninja -DCMAKE_CXX_COMPILER=g++", "creates": "build/build.ninja"},
        "build": "cmake --build build --target p{id}",
        "run": "build/p{id}" + (".exe" if sys.platform == "win32" else "") + " {input} {output}",
        "reference": {"build": "cmake --build build --target ref_p{id}",
                      "run": "build/ref_p{id}" + (".exe" if sys.platform == "win32" else "") + " {input} {output}"},
    },
    "python": {
        "build": "",
        "run": f"{PY} solutions/p{{id}}.py {{input}} {{output}}",
        "reference": {"build": "", "run": f"{PY} _spoilers/reference/p{{id}}.py {{input}} {{output}}"},
    },
    "javascript": {
        "build": "",
        "run": "node solutions/p{id}.mjs {input} {output}",
        "reference": {"build": "", "run": "node _spoilers/reference/p{id}.mjs {input} {output}"},
    },
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dest", type=Path, required=True)
    ap.add_argument("--title", required=True, help="the workbook's name, e.g. 'The Log Workbook'")
    ap.add_argument("--source-url", required=True)
    ap.add_argument("--source-title", required=True)
    ap.add_argument("--author", required=True)
    ap.add_argument("--lang", choices=sorted(RUN), default="cpp")
    ap.add_argument("--headline", default="", help="one line for the book's overview, e.g. 'Build a log-based store yourself'")
    ap.add_argument("--lede", default="")
    ap.add_argument("--credits", default="Expected outputs come from independent sources. Progress is saved in this browser only.")
    ap.add_argument("--force", action="store_true", help="write into a folder that isn't empty")
    args = ap.parse_args()

    dest = args.dest.resolve()
    if dest.exists() and any(dest.iterdir()) and not args.force:
        sys.exit(f"{dest} isn't empty; pass --force to write into it anyway")
    shutil.copytree(TEMPLATE, dest, dirs_exist_ok=True)
    if (LANGS / args.lang).exists():
        shutil.copytree(LANGS / args.lang, dest, dirs_exist_ok=True)
    for folder in ("problems", "solutions", "solutions/common", "starters/blank", "starters/boilerplate",
                   "tests", "_spoilers/reference", "_source", "book"):
        (dest / folder).mkdir(parents=True, exist_ok=True)

    config = dict(RUN[args.lang])
    config["timeoutSeconds"] = 10
    config["book"] = {
        "title": args.title, "sourceUrl": args.source_url, "sourceTitle": args.source_title, "author": args.author,
        "headline": args.headline or f"Build it yourself: {args.source_title}",
        "lede": args.lede or ("Each checkpoint asks you to write the program that one part of the post builds. A checker "
                              "feeds your program inputs and compares what it writes with answers worked out "
                              "independently. How you structure the code is up to you."),
        "credits": args.credits,
        # What the book tells the learner to run, and where.
        "checkCommand": r".\check {id}" if os.name == "nt" else "./check.sh {id}",
        "shell": "PowerShell" if os.name == "nt" else "a terminal",
    }
    config["checkpoints"] = {}
    (dest / "workbook.json").write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    readme = (dest / "README.md").read_text(encoding="utf-8")
    for key, value in (("TITLE", args.title), ("SOURCE_URL", args.source_url), ("SOURCE_TITLE", args.source_title),
                       ("AUTHOR", args.author)):
        readme = readme.replace("{{" + key + "}}", value)
    (dest / "README.md").write_text(readme, encoding="utf-8")
    print(f"created {dest} ({args.lang}). Next: register checkpoints in workbook.json"
          + (" and add_checkpoint() lines in CMakeLists.txt" if args.lang == "cpp" else "") + ".")


if __name__ == "__main__":
    main()
