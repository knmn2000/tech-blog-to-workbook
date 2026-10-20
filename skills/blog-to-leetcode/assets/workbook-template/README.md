# {{TITLE}}

LeetCode-style checkpoints for [{{SOURCE_TITLE}}]({{SOURCE_URL}}) by {{AUTHOR}}. Each checkpoint asks
you to build what one part of the post builds. Your program is checked by its output only, so you
can structure it your own way, in any language, with any library.

The problems are in `problems/` and, nicer to read, in the web problem book
(`book/problem-book.html`). The book has a problem list with your progress, and for each
checkpoint the statement, hints that open in order, an Editorial with a solution proven to pass every test, an editor preloaded with the starter, and the
example test cases. Its Submit button copies your code and shows the command to run; paste the
checker's output back into Test Result to record the verdict.

<!-- The checkpoint list: one row per checkpoint, filled in when the workbook is built. -->

Checkpoints don't depend on each other: each input carries what earlier checkpoints would
produce. The last checkpoint is where your own pieces come together; keep the parts you'll reuse
in `solutions/common/` and it can call them directly.

## Doing a checkpoint

1. Read the problem (book or `problems/NN-*.md`).
2. Write your solution in `solutions/pNN_*`. It starts as a comment and an empty `main`: the
   imports, reading the input and writing the output are yours. If you'd rather start from
   ready-made input/output code, copy `starters/boilerplate/pNN_*` over it (or pick Boilerplate
   in the book's editor) and fill in the functions marked `TODO`. Code you want to reuse in later
   checkpoints can go in `solutions/common/` (in C++, every `.cpp` there is compiled into every
   checkpoint; in Python or JavaScript, import it from there).
3. Check it from this folder (`./check.sh` instead of `.\check` on macOS or Linux):

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

## Using another language or library

The checker runs `<run> <input-file> <output-file>` from this folder and compares the output file.
Change `build` and `run` in `workbook.json`; `{id}` becomes the checkpoint number. To check a
one-off program without changing the config: `.\check 01 -Run "path/to/program {input} {output}"`.

## What's in here

| Path | What it is |
|---|---|
| `problems/` | Problem statements (the book is built from these) |
| `solutions/` | Your code: one file per checkpoint, blank to begin with |
| `solutions/common/` | Code shared by your checkpoints |
| `starters/blank/` | The blank starters. Copy one over `solutions/` to start again. |
| `starters/boilerplate/` | Starters with the input/output code done, if you want them |
| `tools/blank_starters.py` | Writes the blank starters and puts them in `solutions/` (never over your own code) |
| `tests/NN/` | Test inputs and expected outputs |
| `tools/check.py` | The checker (`check.ps1`, `check.cmd` and `check.sh` call it) |
| `tools/gen_pNN.py` | Each checkpoint's test generator (used by `-Fresh`) |
| `tools/build_book.py` | Builds `book/problem-book.html` from `problems/` and `starters/` (the page design is `tools/book_template.html`) |
| `docs/authoring-guide.md` | How the checkpoints and their tests are made |
| `_spoilers/` | Reference solutions. Don't open these until you've passed. |
