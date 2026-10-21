---
name: blog-to-leetcode
description: Turns a technical blog post, tutorial or article (given as a URL) into a LeetCode-style learn-by-doing workbook - a series of implementation checkpoints where the learner writes a program whose output is checked against independently computed answers, with full problem pages, tiered hints, starter code, reference solutions, a checker that supports disputes and fresh test sets, and a web problem book. Use this whenever someone wants to learn from a blog or article by building it themselves, turn a post's code snippets or ideas into exercises, problems, challenges or "leetcode questions", practise implementing what a write-up describes, or make a hands-on course or workbook from an article - even if they never say "leetcode" or "workbook", and even if the post has little or no code. Also use it to open, set up or continue an existing workbook (one made earlier, or cloned from a shared collection), e.g. "open my workbook", "set up this workbook", "I cloned the TrueType workbook", and for "review my disputes".
compatibility: Claude Code. Needs a shell, Python 3.11+ (plus whatever independent libraries the chosen test oracles need), a compiler or runtime for the learner's language, and a way to read the blog (the desktop app's browser pane or WebFetch).
---

# Blog to LeetCode-style workbook

You turn one blog post into a workbook of **checkpoints**. Each checkpoint is a small program the
learner writes: it reads an input file, writes an output file, and a checker compares that output
with answers computed independently of any reference solution. The learner gets a problem page
(description, requirements, tags, examples, sources, four hints that open in order), a blank
starter file (with a boilerplate version as an optional easier start), and one command to check
their work.

The point is that the learner ends up feeling they built the thing themselves, rather than having
copied snippets from the post. Everything below serves that.

## Principles (why the workbook is shaped this way)

1. **One kind of exercise: implement, and match the output.** No quizzes, no find-the-bug. Even a
   blog with no code has a testable kernel for each idea (see `references/mapping.md`).
2. **Tests see output only.** The program runs as `<program> <input-file> <output-file>`. Any
   structure, language or library passes if the output is right. Never test internal functions;
   that forces the author's design on the learner. `tools/langs.py` lets the checker (`-Lang`) and
   the book build and run eight languages without build files; the boilerplate and the reference
   stay in the workbook's own language.
3. **Same task as the snippet.** A checkpoint built from a code snippet asks for what the snippet
   accomplishes, with its scope and simplifications. The author's structure appears only in a hint
   and in "After you pass". Where the snippet is wrong, the tests follow the spec, and the page
   says so neutrally.
4. **Checkpoints stand alone, and can still build on each other.** Each input carries what
   earlier checkpoints would produce (an offset, a parsed record, an intermediate result), so any checkpoint
   can be done first. Code the learner keeps in `solutions/common/` is shared by every
   checkpoint, so a final capstone can call their own earlier work.
5. **The learner writes everything by default.** The starter they get is blank (a comment and an
   empty `main`): imports, input parsing and output are part of the exercise. A boilerplate
   starter with the input/output done is there for anyone who wants it, never forced.
6. **A wrong test must never block a correct solution.** Expected outputs come from an independent
   source, every test traces to a requirement, the checks themselves are checked, and the learner
   can dispute a test and keep going (see `references/test-trust.md`).
7. **Never reproduce the blog.** Link to its sections (text fragments: `url#:~:text=Heading`),
   summarise in your own words, and never paste its prose or code into the workbook. Don't
   download or run the author's repository; write your own reference solutions.

## Workflow

Work in stages and keep the user in the loop at the two decision points marked **(ask)**.

### 1. Set up (ask)

Ask which language the learner wants (default: the blog's own language) and where the workbook
should go (default: a new folder next to the current one, named after the post). Check the
toolchain exists (`g++`/`cmake`, `python`, `node`, ...). Mention anything you'll need to download
(an oracle library, a sample data file, a header) with its source and size, and get a yes before downloading.

### 2. Read the blog

Open the post in the browser pane and run `scripts/extract_blog.js` with the JavaScript tool; it
returns the headings, paragraphs and code blocks in order, with captions. (WebFetch is a fallback,
but it often drops code blocks.) Save the result as `_source/blocks.json` in the workbook. It
stays local: it's for you to map from, never to republish.

Read every code block in full. Note what each one does in your own words, its bugs, and which
parts are demos, data structures or glue rather than logic.

### 3. Map the blog to checkpoints (ask)

Follow `references/mapping.md` to turn the post into a checkpoint map: for each checkpoint its
title, what it's built from (snippet, pseudocode or idea), the input/output contract in one line,
the independent oracle, and a difficulty. Present the map as a table and get the user's approval
before writing anything. This is the cheapest moment to change scope.

### 4. Scaffold the workbook

Run `scripts/new_workbook.py --dest <folder> --title ... --source-url ... --source-title ...
--author ... --lang <cpp|python|...>`. It copies `assets/workbook-template/` (checker, image
comparison, case-file library, book builder, check scripts, README, authoring guide) and writes
`workbook.json` with the book's metadata. Then register every checkpoint from the map in
`workbook.json` (title, solution, problem, cases, generator) before anyone writes checkpoint files,
so parallel authors never edit shared files.

### 5. Author the checkpoints

Follow `references/authoring-guide.md` (also copied into the workbook as
`docs/authoring-guide.md`); `assets/example-checkpoint/` is a complete worked checkpoint to copy
the shape of. Build **one checkpoint completely first**, the most representative one, and show it
to the user; the template is cheapest to fix then. Then do the rest.

Picture checkpoints: `tools/imageio.py` reads and compares images, `tools/inkcheck.py` validates a
reference picture against ideal geometry, and for C++ `include/provided/Canvas.h` is a small
framebuffer with PNG output (needs stb_image_write; ask before downloading it).

For more than a handful of checkpoints, split them into independent groups and give each group to
a subagent, in parallel. Each brief must contain: the authoring guide's path, the finished model
checkpoint's files, the exact contracts for its checkpoints, and a description in your own words
of what each relevant snippet does (subagents must not copy the blog either). Tell them not to
edit shared files and not to use the shared build directory: they compile into their own folder
and check with `-Run`. Keep shared infrastructure (checker, comparison, libraries) to yourself.

### 6. Check the checks

Before any checkpoint counts as done, everything in `references/test-trust.md` must hold:
the reference is Accepted; the boilerplate stub says "Not implemented yet"; at least three planted bugs
(including the blog's own) fail with useful messages; for picture or numeric checkpoints, at least
one *different but correct* variant passes; fresh seeds pass; and an independent solver, a separate
subagent given only the hint-stripped page (`scripts/strip_hints.py`), passes the full suite.
Fold the solver's feedback into the page.

The learner must always be able to see a solution that works. Each Editorial shows the reference
in full (with the files it includes from `_spoilers/`), and it may only claim "Passes all N tests"
for exactly the code that passed. An Accepted `check NN -Ref` run on the committed tests records
that code's fingerprint in `_spoilers/verified.json`. Run it last, after every change to a
reference.

### 7. Publish

First run `py -P tools/blank_starters.py`: it moves each boilerplate into `starters/boilerplate/`,
writes the blank starters into `starters/blank/` and installs them in `solutions/`. Check that
`.\check NN` on a blank starter says "Not started yet".

Then run `py -P tools/build_book.py` to build `book/problem-book.html` from the problem pages. It
exits with warnings if any reference is unchecked or has changed since it passed; fix those (rerun
`check NN -Ref`) before going on, because the Editorial would otherwise show a solution nobody has
proven. Look at the book once in the browser pane (desktop and phone width), and publish it with the
Artifact tool as a private page. The book looks and works like a coding-practice site: a problem
list with progress and topic filters, then per checkpoint a split view with the statement, hints
that open in order, an Editorial tab (a solution proven to pass, then the comparison with the
author's code; it opens by itself on Accepted and is one click away before that), an editor that opens on the blank starter with a
Blank / Boilerplate switch (drafts stay in the browser), and the examples as test cases. Submit
copies the code and shows the command to run; pasting the checker's output back shows the verdict
and records Accepted. The template is generic: everything comes from the problem pages' sections,
`starters/` and `workbook.json`, so keep the section headings exact. Update the README.

The published page can't run code (it uses copy mode: Submit copies the code and shows the
command). The learner's real workspace is the **study server**, so finish by opening the workbook
for them as in the next section. Report: what was built, per checkpoint the verification results,
any judgement calls, the link, and how to come back later (double-click `study.cmd`, or ask you to
"open my workbook").

## When the learner wants to open, set up or continue a workbook

This is also the whole setup for someone who cloned a workbook. The learner should never have to
run more than one thing, so you do the setup.

1. **Find the workbook**: the folder with `workbook.json` (the current folder, a folder they
   name, or a `workbooks/<name>/` folder inside a cloned collection).
2. **Check it can build**: `py -P tools/serve.py --check` (`python3` on macOS or Linux). It names
   any missing tool (compiler, CMake, Ninja), does the first-time build setup, and exits 0 when
   ready. Python itself must be 3.11 or newer.
3. **Install what's missing, with consent.** Say what you'd install, from where and roughly how
   big (e.g. `winget install BrechtSanders.WinLibs.POSIX.UCRT`, `winget install Kitware.CMake`,
   `brew install cmake ninja`), and get a yes first. Then run the check again.
4. **Open the book.** In the Claude desktop app, start the workbook's `study` entry from
   `.claude/launch.json` with the browser pane's preview tool, so the book sits next to the chat.
   Elsewhere, run the study server in the background and give the learner its address
   (`http://127.0.0.1:8787/`). Tell them they can come back by double-clicking `study.cmd`
   (`study.command` on macOS) or by asking you again.

In the book they write code, Run (one example) and Submit (all tests), and see the verdict, the
failing tests (their output and the expected output with the differing words highlighted, judged
the way the checker judges them) and, for pictures, expected/theirs/difference side by side. Their
code is saved to `solutions/` as they type (Ctrl+S, or `:w` with the editor's Vim toggle on), and
edits made in another editor show up in the book. The Files panel shows their project as it grows
(`solutions/common/` plus each checkpoint's file); after each Accepted the book suggests moving
reusable code into `common/`, and **Re-check solved** reruns every solved checkpoint so a change to
shared code that breaks an earlier one shows at once. Inputs stay independent, so nothing blocks
unless they choose to share code. You stay available for hints, explanations and disputes.

## When the learner says "review my disputes"

Read `disputes.json` in the workbook. For each open dispute: rerun that case with `.\check NN -Case
<id>`, recompute the expected value from its recorded source (the generator and its oracle), and
re-read the requirement and the spec. Then either fix the test (change the generator, regenerate,
and rerun every check in step 6) or show the learner the evidence that it's right (the spec text,
the oracle's own output, a hand calculation). Close the dispute with a note (`"status": "closed"`,
`"resolution": "..."`) either way.

## Hard-won lessons

These came from building the first workbook; they apply broadly.

- Tolerances need two kinds of evidence: planted bugs that must fail **and** correct alternatives
  that must pass. Tuning against only one makes the checker either useless or unfair.
- For pictures, forgive differences asymmetrically: extra ink only if the expected image has ink
  within a pixel, missing ink only if the learner's image does. A symmetric rule either rejects
  closed slivers or forgives stray lines.
- Validate generated expected values against the independent source, and treat exact boundary ties
  (a sample point exactly on an edge) as either answer.
- Real data hides edge cases. Count them (e.g. "42 of 90 records use the tricky encoding") and make
  sure tests cover them; hand-made inputs cover the rest, checked by the oracle before use.
- Keep generated pictures small (the checker decodes them in pure Python) and make thin features at
  least ~2 pixels wide, or different correct samplings disagree.
- Print only ASCII from tools on Windows consoles, or reconfigure stdout to UTF-8.
