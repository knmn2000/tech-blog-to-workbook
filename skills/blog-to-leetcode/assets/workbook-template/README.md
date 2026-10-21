# {{TITLE}}

LeetCode-style checkpoints for [{{SOURCE_TITLE}}]({{SOURCE_URL}}) by {{AUTHOR}}. Each checkpoint asks
you to build what one part of the post builds, and each one adds properly named files to a project
of your own. When you finish, `solutions/` is a working {{PROJECT_LABEL}} implementation of the post that
you can put on GitHub as it is.

The problems are in `problems/` and, nicer to read, in the web problem book
(`book/problem-book.html`). The book has a problem list with your progress, and for each
checkpoint the statement, what it adds to your project, hints that open in order, an Editorial
with a solution proven to pass every test, an editor with the checkpoint's files, and the example
test cases.

<!-- The checkpoint list: one row per checkpoint, filled in when the workbook is built. -->

## Start here

Ask Claude to "set up my workbook": it checks the tools, asks which language you'd like (this
workbook's project is {{PROJECT_LABEL}}), creates the project and opens the book. Or open the book
yourself: double-click `study.cmd` on Windows or `study.command` on macOS, or run `.\study`
(PowerShell) or `./study.sh` from this folder. Run and Submit work there, and it offers to create
the {{PROJECT_LABEL}} project if there isn't one yet. Leave its window open while you work, or use the
book's **Exit** button when you're done.

## Your project

<!-- The project's layout: its folders and which checkpoint adds each file, filled in when the
workbook is built. -->

Do the checkpoints in order. Opening a checkpoint (in the book, or `.\check NN`) creates its
files, each with a comment saying what belongs in it; nothing you've written is ever replaced. A
checkpoint's real work goes in `src/`, where later checkpoints use it. Its program in
`checkpoints/` reads a test input, calls your code and writes the answer; that's what the checker
runs.

Test inputs still carry what earlier checkpoints would produce, so a checkpoint's tests only
depend on the earlier files it uses. The whole project is built together, though: if a file of
another checkpoint doesn't build, the checker says which one. **Re-check solved** in the book runs
every solved checkpoint again, so a change that breaks an earlier one shows up at once (marked with
a red `!`). The **Files** panel shows the project as it grows, and when everything passes, the
problem list shows your project next to the author's.

## Doing a checkpoint

1. Read the problem (book or `problems/NN-*.md`). Its "In your project" box lists the files the
   checkpoint creates or adds to, and the earlier files it can build on.
2. Write them. They start blank: the imports, reading the input and writing the output are yours.
   If you'd rather start from ready-made input/output code, pick Boilerplate in the book's editor
   (or copy the checkpoint's files from `starters/boilerplate/`) and fill in what's marked `TODO`.
3. Check it from this folder (`./check.sh` instead of `.\check` on macOS or Linux), or with Run
   and Submit in the book:

```
.\check 01                         run every test
.\check 01 -Case <test-id>         one test in full: input, expected output, your output
.\check 01 -Fresh                  a newly generated set of tests (new random seed)
.\check 01 -Dispute <test-id> "why"    set aside a test you believe is wrong
```

The verdict is `Accepted`, `Wrong Answer`, `Compile Error`, `Runtime Error` or
`Time Limit Exceeded`. Text output is compared word by word, so line endings and extra spaces
don't matter, except inside quoted strings. Every failure shows the requirement it most likely
comes from, where the expected value came from, and the command to reproduce it. Picture
checkpoints also write a diff image (red: extra pixels, blue: missing, yellow: forgiven), and edges
may move by one pixel.

## If you think a test is wrong

Run `.\check 01 -Dispute <test-id> "your reason"`. That test stops counting and you can carry on;
the verdict reads `Accepted (1 disputed)`. Then ask Claude to "review my disputes". Claude
rechecks the expected value against its independent source and either fixes the test or shows
you why it's right. Disputes are kept in `disputes.json`.

## Another language

Only the output is checked, so the project can be in any language. This workbook's project, its
starters and its reference are {{PROJECT_LABEL}}. To work in another language, ask Claude: it shows
which languages are installed (`py -P tools/langs.py` lists them) and how to install the others,
keeps your current project in a folder of its own, and sets up a project in the new language, with
its own build file and the same layout in that language's style. Nothing is created for languages
you don't choose.

To check a one-off program without changing anything:
`.\check 01 -Run "path/to/program {input} {output}"`.

## What's in here

| Path | What it is |
|---|---|
| `problems/` | Problem statements (the book is built from these) |
| `solutions/` | Your project, created when you set the workbook up |
| `starters/project/` | What your project starts with: its build file, README and `.gitignore` |
| `starters/blank/`, `starters/boilerplate/` | Each checkpoint's files, blank and with the input/output done |
| `tests/NN/` | Test inputs and expected outputs |
| `study.cmd`, `study.command`, `study.ps1`, `study.sh` | Open the book with Run and Submit working (they start `tools/serve.py`) |
| `tools/serve.py` | The study server: only reachable from this computer; loads and saves your project's files and runs the checker |
| `tools/check.py` | The checker (`check.ps1`, `check.cmd` and `check.sh` call it) |
| `tools/project.py` | Sets up your project and starts checkpoints (`setup`, `start NN`, `status`) |
| `tools/langs.py` | The languages a project can be in, and how to install them |
| `tools/gen_pNN.py` | Each checkpoint's test generator (used by `-Fresh`) |
| `tools/build_book.py` | Builds `book/problem-book.html` (the page design is `tools/book_template.html`) |
| `docs/authoring-guide.md` | How the checkpoints and their tests are made |
| `_spoilers/` | The reference project. Don't open it until you've passed. |
