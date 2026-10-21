"""Creates a new workbook folder from the skill's template.

    python new_workbook.py --dest ../log-workbook --title "The Log Workbook" --name logkv \
        --source-url https://... --source-title "The Log: ..." --author "Jay Kreps" --lang cpp

Copies assets/workbook-template (checker, project tool, image comparison, case-file library,
book builder, study server, check scripts, README, authoring guide) and the language's project
skeleton from assets/lang/<lang>/starters, makes an empty reference project in
_spoilers/project/, and writes workbook.json: the book's metadata, the project's settings and an
empty assignment list. Then design the layout (references/mapping.md, section 6) and register
every assignment with its files before writing any of them.

The learner's project (solutions/) isn't created here: tools/project.py setup makes it when the
learner chooses a language.
"""

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL / "assets" / "workbook-template"
LANGS = SKILL / "assets" / "lang"
EXE = ".exe" if sys.platform == "win32" else ""

# How each language's project is built and run. C++ and Python have templates so far; for
# another language, follow references/languages.md and add its skeleton under assets/lang/<lang>.
# "python" in a command runs the Python that runs the checker (tools/check.py, to_args).
PROJECTS = {
    "python": {
        "label": "Python", "aliases": ["py", "python3"],
        "setup": None,  # nothing to configure
        "build": "python -P tools/run_py.py --compile solutions",  # a syntax check of every file
        "run": "python -P tools/run_py.py solutions {id} {input} {output}",
        "reference": {
            "snapshot": "build/ref-src",
            "build": "python -P tools/run_py.py --compile build/ref-src",
            "run": "python -P tools/run_py.py build/ref-src {id} {input} {output}"},
        "finish": {"build": "", "run": "python -P tools/run_py.py solutions -m {name}"},
    },
    "cpp": {
        "label": "C++", "aliases": ["c++", "cxx"],
        "setup": {"command": "cmake -S solutions -B build/solutions -G Ninja -DCMAKE_CXX_COMPILER=g++",
                  "creates": "build/solutions/build.ninja"},
        "build": "cmake --build build/solutions --target assignment_{id}",
        "run": "build/solutions/assignment_{id}" + EXE + " {input} {output}",
        "reference": {
            "snapshot": "build/ref-src",
            "setup": {"command": "cmake -S build/ref-src -B build/ref -G Ninja -DCMAKE_CXX_COMPILER=g++",
                      "creates": "build/ref/build.ninja"},
            "build": "cmake --build build/ref --target assignment_{id}",
            "run": "build/ref/assignment_{id}" + EXE + " {input} {output}"},
        "finish": {"build": "cmake --build build/solutions --target {name}", "run": "build/solutions/{name}" + EXE},
    },
}


def fill(path: Path, values: dict):
    text = path.read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    path.write_text(text, encoding="utf-8", newline="\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dest", type=Path, required=True)
    ap.add_argument("--title", required=True, help="the workbook's name, e.g. 'The Log Workbook'")
    ap.add_argument("--name", default="", help="the finished program's name, e.g. logkv (default: from the title)")
    ap.add_argument("--source-url", required=True)
    ap.add_argument("--source-title", required=True)
    ap.add_argument("--author", required=True)
    ap.add_argument("--lang", choices=sorted(PROJECTS), default="cpp")
    ap.add_argument("--headline", default="", help="one line for the book's overview, e.g. 'Build a log-based store yourself'")
    ap.add_argument("--lede", default="")
    ap.add_argument("--credits", default="Expected outputs come from independent sources. The book keeps your progress in this browser only.")
    ap.add_argument("--force", action="store_true", help="write into a folder that isn't empty")
    args = ap.parse_args()

    dest = args.dest.resolve()
    if dest.exists() and any(dest.iterdir()) and not args.force:
        sys.exit(f"{dest} isn't empty; pass --force to write into it anyway")
    spec = PROJECTS[args.lang]
    name = args.name or re.sub(r"[^a-z0-9]+", "_", args.title.lower().removesuffix(" workbook")).strip("_") or "project"

    shutil.copytree(TEMPLATE, dest, dirs_exist_ok=True)
    shutil.copytree(LANGS / args.lang / "starters", dest / "starters", dirs_exist_ok=True)
    for folder in ("problems", "starters/blank", "starters/boilerplate", "tests", "_spoilers/project/src",
                   "_spoilers/project/assignments", "_source", "book", "third_party"):
        (dest / folder).mkdir(parents=True, exist_ok=True)
    values = {"NAME": name, "TITLE": args.title, "SOURCE_URL": args.source_url, "SOURCE_TITLE": args.source_title,
              "AUTHOR": args.author, "PROJECT_LABEL": spec["label"]}
    skeleton = dest / "starters" / "project"
    # Folders named after the program (a Python package: src/{{NAME}}/) take its name.
    for p in sorted(skeleton.rglob("*{{NAME}}*"), key=lambda p: len(p.parts), reverse=True):
        p.rename(p.with_name(p.name.replace("{{NAME}}", name)))
    for p in skeleton.rglob("*"):
        if p.is_file():
            fill(p, values)
    fill(dest / "README.md", values)
    # The reference project starts as the same skeleton (build file, package __init__.py files),
    # without the README the learner's copy explains itself with.
    for p in skeleton.rglob("*"):
        if p.is_file() and p.name != "README.md":
            target = dest / "_spoilers" / "project" / p.relative_to(skeleton)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(p, target)

    finish = {k: v.replace("{name}", name) for k, v in spec["finish"].items()}
    config = {
        "project": {
            "dir": "solutions", "language": args.lang, "languageLabel": spec["label"], "aliases": spec["aliases"],
            "name": name, "reference": "_spoilers/project",
            "starter": "boilerplate",  # what opening an assignment starts from: "boilerplate" or "blank"
            "copy": {},  # e.g. {"third_party/stb_image_write.h": "third_party/stb/stb_image_write.h"}
            "build": finish["build"], "run": finish["run"],
            # Filled in with the map: the author's own files to compare with, and each project file's purpose.
            "author": None, "purposes": {},
        },
        "setup": spec["setup"], "build": spec["build"], "run": spec["run"], "reference": spec["reference"],
        "timeoutSeconds": 10,
        "book": {
            "title": args.title, "sourceUrl": args.source_url, "sourceTitle": args.source_title, "author": args.author,
            "headline": args.headline or f"Build it yourself: {args.source_title}",
            "lede": args.lede or ("Each assignment has you write what one part of the post builds, as files in a "
                                  "project of your own. The checker feeds your program test inputs and compares what it "
                                  "writes with answers from independent sources."),
            "credits": args.credits,
            # What the book tells the learner to run, and where.
            "checkCommand": r".\check {id}" if os.name == "nt" else "./check.sh {id}",
            "shell": "PowerShell" if os.name == "nt" else "a terminal",
        },
        "checkpoints": {},
    }
    if not config["setup"]:
        del config["setup"]
    (dest / "workbook.json").write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # Lets the Claude desktop app open the book (with Run and Submit working) in its browser pane.
    launch = {"version": "0.0.1", "configurations": [{
        "name": "study", "runtimeExecutable": "py" if os.name == "nt" else "python3",
        "runtimeArgs": ["-P", "tools/serve.py", "--no-browser", "--port", "8787"], "port": 8787}]}
    (dest / ".claude").mkdir(exist_ok=True)
    (dest / ".claude" / "launch.json").write_text(json.dumps(launch, indent=2) + "\n", encoding="utf-8")
    print(f"created {dest} ({spec['label']}, program `{name}`). Next: design the project layout, then register "
          "every assignment in workbook.json with its solution, files, extends and buildsOn.")


if __name__ == "__main__":
    main()
