# {{TITLE}}

LeetCode-style assignments for [{{SOURCE_TITLE}}]({{SOURCE_URL}}) by {{AUTHOR}}. In each assignment
you build what one part of the post builds, and add its files, named after what they hold, to a
project of your own. After the last one, `solutions/` holds a working {{PROJECT_LABEL}}
implementation of the post that you can put on GitHub as it is.

The problems are in `problems/` and, nicer to read, in the web problem book
(`book/problem-book.html`). The book has a problem list with your progress, and for each
assignment the statement, what it adds to your project, hints that open in order, an Editorial
with a solution proven to pass every test, an editor with the assignment's files, and the example
test cases.

<!-- The assignment list: one row per assignment, filled in when the workbook is built. -->

## Start here

Ask your coding assistant to "set up my workbook": it checks the tools, asks which language you'd like (this
workbook's project is {{PROJECT_LABEL}}), creates the project and opens the book. Or open the book
yourself: double-click `study.cmd` on Windows or `study.command` on macOS, or run `.\study`
(PowerShell) or `./study.sh` from this folder. Run and Submit work in the book opened this way, and
it offers to create the {{PROJECT_LABEL}} project if there isn't one yet. The study script runs in
a window: leave it open while you work, and use the book's Exit button when you're done.

## Your project

<!-- The project's layout: its folders and which assignment adds each file, filled in when the
workbook is built. -->

Do the assignments in order. Opening an assignment (in the book, or with `.\check NN` or
`./check.sh NN`) creates its files, each with a comment saying why the file exists and what your
job in it is. It doesn't overwrite anything you've written. You write an assignment's real work in `src/`, where later
assignments use it. The assignment's program in `assignments/` reads a test input, calls your code
and writes the answer, and the checker runs that program.

Each test input carries what earlier assignments would produce, so an assignment's tests depend
only on the earlier files it uses. The checker builds the whole project at once, though, and if a
file from another assignment doesn't build, it tells you which one. The book's Re-check solved
button runs every solved assignment again, so you see at once when a change breaks an earlier one
(the book marks it with a red `!`). The Files panel shows the project as it grows, and once every
assignment passes, the problem list shows your project next to the author's.

## Doing an assignment

1. Read the problem (book or `problems/NN-*.md`). In the book, its Start here card lists the files
   to complete, your job in each and the earlier files you can use.
2. Write the files. Each one starts as the Boilerplate, which gives you the input/output code and
   the declarations, and you fill in the parts marked `TODO`. To write all of it yourself, choose
   From scratch above the editor: each file then starts empty apart from its comment.
3. Check it from this folder (`./check.sh` instead of `.\check` on macOS or Linux), or with Run
   and Submit in the book:

```
.\check 01                         run every test
.\check 01 -Case <test-id>         one test in full: input, expected output, your output
.\check 01 -Fresh                  a newly generated set of tests (new random seed)
.\check 01 -Dispute <test-id> "why"    set aside a test you believe is wrong
```

The verdict is `Accepted`, `Wrong Answer`, `Compile Error`, `Runtime Error` or
`Time Limit Exceeded`. The checker compares text output word by word, so line endings and extra
spaces don't matter, except inside quoted strings. For each failure it shows its best guess at the
requirement behind it, where the expected value came from, and the command that reproduces it. For
picture assignments it also writes a diff image (red: extra pixels, blue: missing, yellow:
forgiven), and it lets edges move by one pixel.

## If you think a test is wrong

Run `.\check 01 -Dispute <test-id> "your reason"`. That test stops counting and you can carry on;
the verdict reads `Accepted (1 disputed)`. Then ask your coding assistant to "review my disputes". It
rechecks the expected value against its independent source and either fixes the test or shows
you why it's right. The checker keeps disputes in `disputes.json`.

## Another language

The checker reads only your program's output, so you can write the project in any language. This
workbook's project, its starters and its reference are {{PROJECT_LABEL}}.

To work in another language, ask your coding assistant. It shows which languages you have installed
(`py -P tools/langs.py` lists them; `python3` in place of `py` on macOS or Linux) and how to
install the others, keeps your current project in a folder of its own, and sets up a project in
the new language, with its own build file and the same layout in that language's style. It
creates nothing for languages you don't choose.

To check a one-off program without changing anything, run
`.\check 01 -Run "path/to/program {input} {output}"`.

## What's in here

| Path | What it is |
|---|---|
| `problems/` | Problem statements (`tools/build_book.py` makes the book from these) |
| `primer/` | The primer: every term, library and tool the assignments use, explained, with links to learn more (the book's Primer view) |
| `solutions/` | Your project, created when you set the workbook up |
| `starters/project/` | What your project starts with: its build file, README and `.gitignore` |
| `starters/blank/`, `starters/boilerplate/` | Each assignment's files, blank and with the input/output done |
| `tests/NN/` | Test inputs and expected outputs |
| `study.cmd`, `study.command`, `study.ps1`, `study.sh` | Open the book with Run and Submit working (they start `tools/serve.py`) |
| `tools/serve.py` | The study server: only reachable from this computer; loads and saves your project's files and runs the checker |
| `tools/check.py` | The checker (`check.ps1`, `check.cmd` and `check.sh` call it) |
| `tools/project.py` | Sets up your project and starts assignments (`setup`, `start NN`, `status`) |
| `tools/langs.py` | The languages a project can be in, and how to install them |
| `tools/gen_pNN.py` | Each assignment's test generator (used by `-Fresh`) |
| `tools/build_book.py` | Builds `book/problem-book.html` (the page design is `tools/book_template.html`) |
| `tools/primer_check.py` | Checks that the primer covers what each assignment uses (`--links` also tests its links) |
| `docs/authoring-guide.md` | How to write the assignments and their tests |
| `_spoilers/` | The reference project. Don't open it until you've passed. |

The tools work on Windows, macOS and Linux. Program names in `workbook.json` end in `{exe}`,
which the tools turn into `.exe` on Windows and leave out on macOS and Linux, so the same file
works on all three.
