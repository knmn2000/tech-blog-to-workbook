---
name: blog-to-leetcode
description: Turns a technical blog post, tutorial or article (given as a URL) into a LeetCode-style learn-by-doing workbook - a series of implementation assignments where the learner writes a program whose output is checked against independently computed answers, with full problem pages, tiered hints, starter code, reference solutions, a checker that supports disputes and fresh test sets, and a web problem book. Use this whenever someone wants to learn from a blog or article by building it themselves, turn a post's code snippets or ideas into exercises, problems, challenges or "leetcode questions", practise implementing what a write-up describes, or make a hands-on course or workbook from an article - even if they never say "leetcode" or "workbook", and even if the post has little or no code. Also use it to open, set up or continue an existing workbook (one made earlier, or cloned from a shared collection), e.g. "open my workbook", "set up this workbook", "I cloned the TrueType workbook", and for "review my disputes".
compatibility: Claude Code. Needs a shell, Python 3.11+ (plus whatever independent libraries the chosen test oracles need), a compiler or runtime for the learner's language, and a way to read the blog (the desktop app's browser pane or WebFetch).
---

# Blog to LeetCode-style workbook

You turn one blog post into a workbook of assignments. Each assignment is a small program the
learner writes: it reads an input file and writes an output file, and a checker compares that
output with answers from a source independent of any reference solution. The learner gets a
problem page (description, requirements, tags, examples, sources, four hints that open in order),
a blank starter file (with a boilerplate version as an optional easier start), and one command to
check their work.

The learner should finish feeling they built the thing themselves instead of copying snippets from
the post, and each principle and step below serves that goal.

## Principles (why the workbook is shaped this way)

1. Every assignment is the same kind of exercise: implement something, and match the output. Don't
   write quizzes or find-the-bug exercises. Even a blog with no code has a testable kernel for
   each idea (see `references/mapping.md`).
2. Tests see only the output. The program runs as `<program> <input-file> <output-file>`, and any
   structure, language or library passes if the output is right. Never test internal functions:
   that forces the author's design on the learner. The learner picks the project's language when
   they set the workbook up, and you set up only that language (`references/languages.md`). The
   starters, the boilerplate and the reference are in the workbook's own language.
3. An assignment built from a code snippet asks for the same task: what the snippet accomplishes,
   with its scope and simplifications. The author's structure appears only in a hint and in "After
   you pass". If the snippet is wrong, the tests follow the spec, and the page says so in a
   neutral tone.
4. The learner builds a real project, one assignment at a time. They do the assignments in order,
   and each one's work goes into a file named for its module, at its place in a project layout
   planned with the map: the author's module and folder names where they published code, and
   otherwise the language's usual layout. Later assignments import earlier files instead of
   copying them, and the capstone is the project's real `main`. The finished `solutions/` should
   read like an implementation of the post, and someone who knows the author's code should
   recognise its shape. Each assignment also has a small entry program, the one the checker runs:
   it reads a test input, calls the project's code and writes the output. Inputs still carry what
   earlier assignments would produce (an offset, a parsed record), so an assignment's tests depend
   only on the earlier files it chooses to import.
5. By default the learner writes every line. Each assignment starts with blank files at their
   places in the project (a comment saying what belongs there, and an empty `main` in the entry
   program): imports, the module's API, input parsing and output are part of the exercise. A
   boilerplate version (the entry program done, the module's declarations named as the author
   names them) is available to anyone who wants it, and it stays optional.
6. A wrong test must never block a correct solution. Expected outputs come from an independent
   source, every test traces to a requirement, you check the checks themselves, and the learner
   can dispute a test and keep going (see `references/test-trust.md`).
7. Never reproduce the blog. Link to its sections (text fragments: `url#:~:text=Heading`),
   summarise in your own words, and don't paste its prose or code into the workbook. Don't
   download or run the author's repository; write your own reference solutions.

## Workflow

Work in stages, and keep the user in the loop at the two decision points marked (ask).

### 1. Set up (ask)

Ask which language to write the workbook in (default: the blog's own language; the template has
project skeletons for C++ and Python, and `references/languages.md` says what a project looks like
in the others) and where the workbook should go (default: a new folder next to the current one,
named after the post). Check that the toolchain exists (`g++`/`cmake`, `python`, `node`, ...).
Mention anything you'll need to download (an oracle library, a sample data file, a header) with
its source and size, and get a yes before downloading.

### 2. Read the blog

Open the post in the browser pane and run `scripts/extract_blog.js` with the JavaScript tool; it
returns the headings, paragraphs and code blocks in order, with captions. (WebFetch is the
fallback, and it often drops code blocks.) Save the result as `_source/blocks.json` in the
workbook. It stays local: you map from it, and you never republish it.

Read every code block in full. Note what each one does in your own words, its bugs, and which
parts are demos, data structures or glue rather than logic.

### 3. Map the blog to assignments (ask)

Follow `references/mapping.md` to turn the post into an assignment map: for each assignment its
title, what it's built from (snippet, pseudocode or idea), the project file(s) it creates or
extends, the input/output contract in one line, the independent oracle, and a difficulty. With it,
show the project layout the learner will end up with as a file tree, beside the author's layout
when they published one (file names only). Present both and get the user's approval before
writing anything. This is the cheapest moment to change scope, and the only cheap moment to
change the layout: every starter, reference and page depends on it.

### 4. Scaffold the workbook

Run `scripts/new_workbook.py --dest <folder> --title ... --name <program> --source-url ...
--source-title ... --author ... --lang cpp` (or `--lang python`). It copies
`assets/workbook-template/` (checker, project tool, image comparison, case-file library, book
builder, study server, check scripts, README, authoring guide) and the language's project skeleton
into `starters/project/`, makes an empty reference project in `_spoilers/project/`, and writes
`workbook.json`.

Then, before anyone writes assignment files (so parallel authors never edit shared files), put the
approved layout in `workbook.json`:
- every assignment from the map: title, entry program, the project files it creates and adds to,
  the earlier files it builds on, problem, cases, generator;
- each project file's purpose (why it exists);
- each assignment's job in every file it touches (`jobs`);
- the author's own file names, for the finish card.

The purposes and jobs keep the learner oriented: they become the header of every starter file and
the "Start here" card at the top of each assignment. Fill in the project skeleton's README (what
the program does, and its layout).

### 5. Author the assignments

Follow `references/authoring-guide.md` (also copied into the workbook as
`docs/authoring-guide.md`); `assets/example-assignment/` is a complete worked assignment, laid out
as in a workbook, to copy the shape of. Build one whole assignment first, the most representative
one, and show it to the user: fixing the template costs least at that point. Then do the rest, in
order. Each assignment's reference files go in the reference project, where later ones include
them, and a file that later assignments add to gets a `// ---- Assignment NN ----` marker before
each addition. Write the boilerplate from the reference (TODO bodies); the blank starters come from
`py -P tools/blank_starters.py`.

For picture assignments, `tools/imageio.py` reads and compares images and `tools/inkcheck.py`
validates a reference picture against ideal geometry. `assets/lang/cpp/optional/Canvas.h` gives
the project a small framebuffer with PNG output for posts where drawing isn't one of the steps
(needs stb_image_write; ask before downloading it).

For more than a handful of assignments, split them into independent groups and give each group to
a subagent, in parallel. Each brief must contain: the authoring guide's path, the finished model
assignment's files, the exact contracts for its assignments, and a description in your own words
of what each relevant snippet does (subagents must not copy the blog either). Tell them not to
edit shared files and not to use the shared build directory: they compile into their own folder
and check with `-Run`. Keep shared infrastructure (checker, comparison, libraries) to yourself.

### 6. Check the checks

Before any assignment counts as done, every condition in `references/test-trust.md` must hold:
- `-Ref` gives the reference Accepted. It builds the reference project as it stands after the
  assignment, which also proves the project builds at that point in the series.
- The boilerplate says "Not implemented yet" and the blank starter "Not started yet".
- At least three planted bugs, including the blog's own, fail with useful messages.
- For picture or numeric assignments, at least one different but correct variant passes.
- Fresh seeds pass.
- An independent solver, a separate subagent given only the hint-stripped page
  (`scripts/strip_hints.py`), passes the full suite. Fold its feedback into the page.

The learner must be able to see a working solution at any point. Each Editorial shows the
reference in full (with the files it includes from `_spoilers/`), and it may claim "Passes all N
tests" only for code identical to what passed. An Accepted `check NN -Ref` run on the committed
tests records that code's fingerprint in `_spoilers/verified.json`. Run it last, after every
change to a reference.

### 7. Publish

First run `py -P tools/blank_starters.py --force`: it writes every blank starter and refreshes the
header of every boilerplate file (assignment, why the file exists, your job, how to start), so they
match the final titles, files, purposes and jobs. Then, in a copy of the workbook, run
`py -P tools/project.py setup` and check that `.\check 01` creates assignment 01's files and then
says "Not implemented yet" (the Boilerplate leaves the work as TODOs). The workbook itself ships
without `solutions/`: `tools/project.py` creates the learner's project when they choose a
language.

Then run `py -P tools/build_book.py` to build `book/problem-book.html` from the problem pages. It
exits with warnings if any reference hasn't passed `-Ref` or has changed since it passed. Fix those
(rerun `check NN -Ref`) before going on, or the Editorial will show an unproven solution. View the
book once in the browser pane (desktop and phone width), and publish it with the Artifact tool as
a private page.

The book looks and works like a coding-practice site. It opens on a problem list with progress and
topic filters, and each assignment has a split view with:
- the statement, with a "Start here" card: the files to write, the job in each, the earlier files
  it can use, and the two ways to start;
- hints that open in order;
- an Editorial tab: the reference's files as they stand after the assignment, proven to pass, then
  the comparison with the author's code. It opens by itself on Accepted and is one click away
  before that;
- an editor with the assignment's files as tabs and a Boilerplate / From scratch switch (drafts
  stay in the browser);
- a Files panel with the planned project;
- the examples as test cases.

Submit copies the open file and shows the command to run; pasting the checker's output back shows
the verdict and records Accepted. The template is generic: it builds every page from the problem
pages' sections, `starters/` and `workbook.json`, so keep the section headings exact. Fill in the
README's assignment list and project layout.

For a collection with a site (like `techblog-workbooks`, whose `site/` publishes to GitHub Pages
on every push), give `workbook.json` a `site` block with what the site shows and the tools don't
need: `language`, `requires` and a `launch` entry per system, plus `caveat` and `promptNote` if
you want them (`new_workbook.py` writes a first version). The site serves the workbook's own book
in hosted mode (`window.WORKBOOK_HOST`): the editor is read-only, and typing in it, Run and Submit
all open the "Run this workbook on your computer" dialog, so a learner who tries to start coding
there learns where to do it. Commit the workbook into `workbooks/<slug>/`, push, and check its
page and book on the site once the workflow has run.

The published page can't run code (it uses copy mode: Submit copies the code and shows the
command). The learner's real workspace is the study server, so finish by opening the workbook for
them as in the next section. Report what you built, the verification results per assignment,
any judgement calls, the link, and how to come back later (double-click `study.cmd`, or ask you to
"open my workbook").

## When the learner wants to open, set up or continue a workbook

These steps are also the whole setup for someone who cloned a workbook. You do the setup, so the
learner runs one thing at most.

1. Find the workbook: the folder with `workbook.json` (the current folder, a folder they name, or
   a `workbooks/<name>/` folder inside a cloned collection).
2. Check that it can build: `py -P tools/serve.py --check` (`python3` on macOS or Linux). It
   names any missing tool (compiler, CMake, Ninja), does the first-time build setup, and exits 0
   when ready. Python itself must be 3.11 or newer.
3. Install what's missing, with consent. Say what you'd install, from where and about how big
   (e.g. `winget install BrechtSanders.WinLibs.POSIX.UCRT`, `winget install Kitware.CMake`,
   `brew install cmake ninja`), and get a yes first. Then run the check again.
4. Set up their project, if `solutions/` doesn't exist yet. Ask which language they want, as
   options showing which ones they have installed (`py -P tools/langs.py`), with the workbook's own
   language first (it has the boilerplate and the Editorial's solutions). For that language run
   `py -P tools/project.py setup`; for another, follow `references/languages.md`. Set up only the
   chosen language. If they later ask you to switch, keep the old project in a folder of its own
   (`solutions-cpp/`) and set up the new one (`references/languages.md`, section 4).
5. Open the book. In the Claude desktop app, start the workbook's `study` entry from
   `.claude/launch.json` with the browser pane's preview tool, so the book sits next to the chat.
   Elsewhere, run the study server in the background and give the learner its address
   (`http://127.0.0.1:8787/`). Tell them they can come back by double-clicking `study.cmd`
   (`study.command` on macOS) or by asking you again.

In the book they write code, Run (one example) and Submit (all tests), and see the verdict, the
failing tests (their output and the expected output with the differing words highlighted, judged
the way the checker judges them) and, for pictures, expected/theirs/difference side by side. The
book saves their code to `solutions/` as they type (Ctrl+S, or `:w` with the editor's Vim toggle
on), and edits they make in another editor show up in the book. The Files panel shows their
project growing file by file, and the Re-check solved button reruns every solved assignment, so a
change to an earlier file that breaks an earlier assignment shows at once. Once every assignment
passes, the book shows their project tree next to the author's. The Exit button saves their work,
stops the study server and closes the page. You stay available for hints, explanations and
disputes.

## When a workbook was made with an older version of this skill

Signs of an older workbook:
- `workbook.json` has no `project` block;
- each "checkpoint" is a single file `solutions/pNN_*`;
- a `common/` folder holds shared code that the learner never builds.

Bring it up to the current standard in this order, showing the user the layout (step 2) before you
build anything.

1. Update the tools. Copy `assets/workbook-template/tools/` over the workbook's `tools/`, keeping
   its own generators and data files, and update `docs/authoring-guide.md` and `.gitignore` (the
   learner's `solutions/` is never committed). If `solutions/` is tracked, untrack it with
   `git rm --cached`: the files stay on disk.
2. Plan the layout (ask). Map each checkpoint to the project files it creates or adds to, as in
   workflow step 3. Code that the old reference repeats across checkpoints becomes one module that
   later assignments import.
3. Rebuild the reference, `_spoilers/project/`, as one project:
   - section markers for later additions;
   - one program per assignment under `assignments/`;
   - each assignment's `files`, `extends` and `buildsOn` registered in `workbook.json`.

   Have one author write the whole reference, so the module interfaces agree. The tests don't
   change, and every assignment must pass `-Ref` again.
4. Write the Boilerplate starters from the reference: declarations, constants and the assignment
   program stay, and logic becomes a TODO that raises (`NotImplementedError`, or
   `throw std::logic_error("not implemented: ...")`). Test each one on a copy of the reference
   (`-Run`): it must say "Not implemented yet". Then write the `jobs` and `purposes`, and run
   `tools/blank_starters.py`.
5. Update the problem pages. Switch to assignment wording, remove the paragraphs about starter
   files, and point file references at the project's modules. Rewrite "Where this fits" and the
   Requirements opening, then do the readability pass in section 8 of the authoring guide, with
   `scripts/slop_scan.py` and `scripts/aiw_scan.py`.
6. Retire the old files. Move the old per-checkpoint starters, reference and `solutions/` files to
   the Recycle Bin, after confirming that the learner's copies still match the blank starters.
   Never discard a learner's own code. Rewrite the workbook's README for the project.
7. Verify, as in workflow step 6:
   - every `-Ref` passes;
   - a fresh set-up project opens, and Submit gives "Not implemented yet";
   - the book looks right in the browser pane;
   - you have checked every hit from both scanners.

## When the learner says "review my disputes"

Read `disputes.json` in the workbook. For each open dispute: rerun that case with `.\check NN -Case
<id>`, recompute the expected value from its recorded source (the generator and its oracle), and
re-read the requirement and the spec. Then either fix the test (change the generator, regenerate,
and rerun every check in step 6) or show the learner the evidence that it's right (the spec text,
the oracle's own output, a hand calculation). Close the dispute with a note (`"status": "closed"`,
`"resolution": "..."`) either way.

## Hard-won lessons

These came from building the first workbook, and they apply to other workbooks too.

- Plan the project layout together with the map. Assignments written as separate one-file
  programs leave the learner with a pile of exercises instead of a project, and retrofitting a
  layout means rewriting every starter, reference and page.
- Prove the reference as it stands after each assignment, as well as the finished one. In the
  first workbook, the finished outline renderer included the geometry file from a later
  assignment, so the series couldn't build at that step, and the finished geometry file would have
  shown the answers to three later assignments in an earlier Editorial. Section markers and
  per-assignment snapshots catch both.
- Tolerances need two kinds of evidence: planted bugs that must fail, and correct alternatives
  that must pass. Tuning against only one makes the checker either useless or unfair.
- For pictures, use an asymmetric rule to forgive differences: extra ink only if the expected
  image has ink within a pixel, missing ink only if the learner's image does. A symmetric rule
  either rejects closed slivers or forgives stray lines.
- Validate generated expected values against the independent source, and treat exact boundary ties
  (a sample point that lies on an edge) as either answer.
- Real data hides edge cases. Count them (e.g. "42 of 90 records use the tricky encoding") and make
  sure tests cover them; hand-made inputs, which the oracle checks before use, cover the rest.
- Keep generated pictures small (the checker decodes them in pure Python) and make thin features at
  least ~2 pixels wide, or different correct samplings disagree.
- Print only ASCII from tools on Windows consoles, or reconfigure stdout to UTF-8.
