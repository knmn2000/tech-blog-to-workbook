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
   that forces the author's design on the learner. The learner picks the project's language when
   the workbook is set up, and only that language is set up (`references/languages.md`); the
   starters, the boilerplate and the reference are in the workbook's own language.
3. **Same task as the snippet.** A checkpoint built from a code snippet asks for what the snippet
   accomplishes, with its scope and simplifications. The author's structure appears only in a hint
   and in "After you pass". Where the snippet is wrong, the tests follow the spec, and the page
   says so neutrally.
4. **The learner builds a real project, one checkpoint at a time.** Checkpoints are done in
   order, and each one's work is saved as a properly named file at its place in a project layout
   planned with the map: the author's module and folder names where they published code,
   otherwise the language's usual layout. Later checkpoints import earlier files instead of
   copying them, and the capstone is the project's real `main`. The finished `solutions/` should
   read like an implementation of the post, and someone who knows the author's code should
   recognise its shape. Each checkpoint also has a small entry program, the one the checker runs:
   it reads a test input, calls the project's code and writes the output. Inputs still carry what
   earlier checkpoints would produce (an offset, a parsed record), so a checkpoint's tests only
   depend on the earlier files it chooses to import.
5. **The learner writes everything by default.** Each checkpoint starts with blank files at their
   places in the project (a comment saying what belongs there, and an empty `main` in the entry
   program): imports, the module's API, input parsing and output are part of the exercise. A
   boilerplate version (the entry program done, the module's declarations named as the author
   names them) is there for anyone who wants it, never forced.
6. **A wrong test must never block a correct solution.** Expected outputs come from an independent
   source, every test traces to a requirement, the checks themselves are checked, and the learner
   can dispute a test and keep going (see `references/test-trust.md`).
7. **Never reproduce the blog.** Link to its sections (text fragments: `url#:~:text=Heading`),
   summarise in your own words, and never paste its prose or code into the workbook. Don't
   download or run the author's repository; write your own reference solutions.

## Workflow

Work in stages and keep the user in the loop at the two decision points marked **(ask)**.

### 1. Set up (ask)

Ask which language the workbook should be written in (default: the blog's own language; the
template has a project skeleton for C++, and `references/languages.md` says what a project looks
like in the others) and where the workbook should go (default: a new folder next to the current
one, named after the post). Check the toolchain exists (`g++`/`cmake`, `python`, `node`, ...).
Mention anything you'll need to download (an oracle library, a sample data file, a header) with
its source and size, and get a yes before downloading.

### 2. Read the blog

Open the post in the browser pane and run `scripts/extract_blog.js` with the JavaScript tool; it
returns the headings, paragraphs and code blocks in order, with captions. (WebFetch is a fallback,
but it often drops code blocks.) Save the result as `_source/blocks.json` in the workbook. It
stays local: it's for you to map from, never to republish.

Read every code block in full. Note what each one does in your own words, its bugs, and which
parts are demos, data structures or glue rather than logic.

### 3. Map the blog to checkpoints (ask)

Follow `references/mapping.md` to turn the post into a checkpoint map: for each checkpoint its
title, what it's built from (snippet, pseudocode or idea), the project file(s) it creates or
extends, the input/output contract in one line, the independent oracle, and a difficulty. With it,
show the project layout the learner will end up with as a file tree, beside the author's layout
when they published one (file names only). Present both and get the user's approval before
writing anything. This is the cheapest moment to change scope, and the only cheap moment to
change the layout: every starter, reference and page depends on it.

### 4. Scaffold the workbook

Run `scripts/new_workbook.py --dest <folder> --title ... --name <program> --source-url ...
--source-title ... --author ... --lang cpp`. It copies `assets/workbook-template/` (checker,
project tool, image comparison, case-file library, book builder, study server, check scripts,
README, authoring guide) and the language's project skeleton into `starters/project/`, makes an
empty reference project in `_spoilers/project/`, and writes `workbook.json`. Then, before anyone
writes checkpoint files (so parallel authors never edit shared files), put the approved layout in
`workbook.json`: every checkpoint from the map (title, entry program, the project files it
creates and adds to, the earlier files it builds on, problem, cases, generator), each project
file's one-line purpose, and the author's own file names for the finish card. Fill in the
project skeleton's README (what the program does, how it's organised).

### 5. Author the checkpoints

Follow `references/authoring-guide.md` (also copied into the workbook as
`docs/authoring-guide.md`); `assets/example-checkpoint/` is a complete worked checkpoint, laid out
as in a workbook, to copy the shape of. Build **one checkpoint completely first**, the most
representative one, and show it to the user; the template is cheapest to fix then. Then do the
rest, in order: each checkpoint's reference files go in the reference project, where later ones
include them, and a file that later checkpoints add to gets a `// ---- Checkpoint NN ----` marker
before each addition. Write the boilerplate from the reference (TODO bodies); the blank starters
come from `py -P tools/blank_starters.py`.

Picture checkpoints: `tools/imageio.py` reads and compares images, `tools/inkcheck.py` validates a
reference picture against ideal geometry, and when drawing isn't one of the post's steps,
`assets/lang/cpp/optional/Canvas.h` gives the project a small framebuffer with PNG output (needs
stb_image_write; ask before downloading it).

For more than a handful of checkpoints, split them into independent groups and give each group to
a subagent, in parallel. Each brief must contain: the authoring guide's path, the finished model
checkpoint's files, the exact contracts for its checkpoints, and a description in your own words
of what each relevant snippet does (subagents must not copy the blog either). Tell them not to
edit shared files and not to use the shared build directory: they compile into their own folder
and check with `-Run`. Keep shared infrastructure (checker, comparison, libraries) to yourself.

### 6. Check the checks

Before any checkpoint counts as done, everything in `references/test-trust.md` must hold:
the reference is Accepted (`-Ref` builds the reference project as it stands after the checkpoint,
which also proves the project builds at that point in the series); the boilerplate says "Not
implemented yet" and the blank starter "Not started yet"; at least three planted bugs
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

First run `py -P tools/blank_starters.py --force` so every blank starter matches the final
titles, files and purposes. Then, in a copy of the workbook, run `py -P tools/project.py setup` and
check that `.\check 01` creates checkpoint 01's files and then says "Not started yet". The
workbook itself ships without `solutions/`: the learner's project is made when they choose a
language.

Then run `py -P tools/build_book.py` to build `book/problem-book.html` from the problem pages. It
exits with warnings if any reference is unchecked or has changed since it passed; fix those (rerun
`check NN -Ref`) before going on, because the Editorial would otherwise show a solution nobody has
proven. Look at the book once in the browser pane (desktop and phone width), and publish it with the
Artifact tool as a private page. The book looks and works like a coding-practice site: a problem
list with progress and topic filters, then per checkpoint a split view with the statement (and
an "In your project" box: the files it creates, adds to and builds on), hints that open in order,
an Editorial tab (the reference's files as they stand after the checkpoint, proven to pass, then
the comparison with the author's code; it opens by itself on Accepted and is one click away before
that), an editor with the checkpoint's files as tabs and a Blank / Boilerplate switch (drafts stay
in the browser), and the examples as test cases. Submit copies the open file and shows the command
to run; pasting the checker's output back shows the verdict and records Accepted. The template is
generic: everything comes from the problem pages' sections, `starters/` and `workbook.json`, so
keep the section headings exact. Fill in the README's checkpoint list and project layout.

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
4. **Set up their project**, if `solutions/` doesn't exist yet. Ask which language they want, as
   options showing which are installed (`py -P tools/langs.py`), with the workbook's own language
   first (it has the boilerplate and the Editorial's solutions). For that language run
   `py -P tools/project.py setup`; for another, follow `references/languages.md`. Only the chosen
   language is set up. Later, if they want to switch, they ask you: keep the old project in a
   folder of its own (`solutions-cpp/`) and set up the new one (same reference, section 4).
5. **Open the book.** In the Claude desktop app, start the workbook's `study` entry from
   `.claude/launch.json` with the browser pane's preview tool, so the book sits next to the chat.
   Elsewhere, run the study server in the background and give the learner its address
   (`http://127.0.0.1:8787/`). Tell them they can come back by double-clicking `study.cmd`
   (`study.command` on macOS) or by asking you again.

In the book they write code, Run (one example) and Submit (all tests), and see the verdict, the
failing tests (their output and the expected output with the differing words highlighted, judged
the way the checker judges them) and, for pictures, expected/theirs/difference side by side. Their
code is saved to `solutions/` as they type (Ctrl+S, or `:w` with the editor's Vim toggle on), and
edits made in another editor show up in the book. The Files panel shows their project growing
file by file, and **Re-check solved** reruns every solved checkpoint, so a change to an earlier file
that breaks an earlier checkpoint shows at once. When they finish, the book shows their project
tree next to the author's. **Exit** saves everything, stops the study server and closes the page.
You stay available for hints, explanations and disputes.

## When the learner says "review my disputes"

Read `disputes.json` in the workbook. For each open dispute: rerun that case with `.\check NN -Case
<id>`, recompute the expected value from its recorded source (the generator and its oracle), and
re-read the requirement and the spec. Then either fix the test (change the generator, regenerate,
and rerun every check in step 6) or show the learner the evidence that it's right (the spec text,
the oracle's own output, a hand calculation). Close the dispute with a note (`"status": "closed"`,
`"resolution": "..."`) either way.

## Hard-won lessons

These came from building the first workbook; they apply broadly.

- Plan the project layout with the map, not afterwards. Checkpoints written as separate one-file
  programs leave the learner with a pile of exercises instead of a project, and retrofitting a
  layout means rewriting every starter, reference and page.
- Prove the reference as it stands after each checkpoint, not only the finished one. In the first
  workbook, the finished outline renderer included the geometry file from a later checkpoint, so
  the series couldn't build at that step, and the finished geometry file would have shown the
  answers to three later checkpoints in an earlier Editorial. Section markers and per-checkpoint
  snapshots catch both.

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
