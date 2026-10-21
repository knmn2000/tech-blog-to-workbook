# tech-blog-to-workbook

Turn a technical blog post into a LeetCode-style workbook, so you learn what the post teaches by
building it yourself.

This is a [Claude Code](https://claude.com/claude-code) plugin. Give Claude a link to a post: it
reads the post, turns each idea or code snippet into an assignment, and builds a workbook with
problem pages, starter files, a checker whose answers come from an independent source, and a
problem book that works like a coding-practice site. You write the code, and the checker tells
you when your output is right. By the last assignment you've rebuilt what the post builds, and you
know why it works.

![An assignment in the problem book: the statement on the left, the editor and test cases on the right](docs/screenshots/problem-view.png)

[techblog-workbooks](https://github.com/knmn2000/techblog-workbooks) collects the workbooks made
with this plugin. The first one is an 18-assignment TrueType font renderer, built on Yohei
Yamasaki's post
[Writing a tiny TrueType parser and renderer from scratch](https://yayo1.com/en/blog/tiny-truetype-renderer/).

## What a workbook gives you

- Every assignment is the same kind of exercise: you write a program, and the checker compares its
  output with the expected answer. There are no quizzes and no find-the-bug exercises. Even a post
  with no code has an idea you can implement and test.
- You choose the language. The checker reads only the output: each assignment's program runs as
  `<program> <input-file> <output-file>`. If the post has code, an assignment asks for what that
  snippet accomplishes, and the tests don't depend on the author's design. Claude asks which
  language you want when you set a workbook up (C, C++, Go, Rust, Python, JavaScript, TypeScript or
  Lua), shows which ones you have installed and how to install the rest, and sets up only the one
  you pick.
- Each file starts as the Boilerplate, with the input and output code written, declarations named
  as the author names them, and TODOs for the rest. Choose From scratch instead and each file
  starts as a comment saying what belongs in it (and an empty `main` in the assignment's program),
  so working out the imports, the API and the input parsing becomes part of the exercise.
- You go through the assignments in order, and each one adds named source files, such as
  `GlyphParser.cpp`, to a project laid out like the author's own. Later assignments import your
  earlier files, and the last one is the project's `main`, so the finished code reads like an
  implementation of the post. Each test input still carries what the earlier assignments would
  produce, so an assignment's tests depend only on the earlier files you choose to use.
- Each problem page has a description, numbered requirements, worked examples, constraints,
  sources and tags (language features, libraries, concepts), four hints that open in order, and an
  Editorial with a complete solution proven to pass every test, followed by a comparison with the
  author's code. The Editorial opens when you pass, and before that it's one click away.
- The workbook takes expected answers from an independent source (a library, a specification, a
  hand calculation), never from the reference solution. Every test traces to a requirement, and
  Claude checks the checks before an assignment ships:
  - the reference solution passes;
  - planted bugs fail, including any bug in the post's own code;
  - different-but-correct solutions pass;
  - a separate solver passes using only the problem page.
- If you think a test is wrong, `-Dispute` sets it aside so you can carry on, and `-Fresh`
  generates new tests you haven't seen. Ask Claude to "review my disputes" and it fixes the test or
  shows you the evidence.
- The problem book has a problem list with progress and topic filters, and a split view with the
  statement, an editor and the test cases. Double-click `study.cmd` in the workbook (or ask Claude
  to "open my workbook"), and Run and Submit build and check your code in the book. It shows the
  verdict, the failing tests and, for pictures, the expected image, yours and the difference side
  by side. The book saves your code to the workbook as you type, and edits you make in your own
  editor show up too.
- Ask Claude to "set up my workbook" and it checks the tools the workbook needs, asks which
  language you want, offers to install anything missing, creates your project and opens the book.
  Later you reopen it with a double-click, and the book's Exit button stops it when you're done.

| Problem list | Test result |
|---|---|
| ![The problem list with progress by difficulty](docs/screenshots/problem-list.png) | ![An Accepted verdict with a pass bar for each requirement](docs/screenshots/test-result.png) |

## Install

In Claude Code:

```
/plugin marketplace add knmn2000/tech-blog-to-workbook
/plugin install tech-blog-to-workbook@tech-blog-to-workbook
```

Then ask for a workbook in your own words, for example:

```
Turn https://example.com/some-post into a workbook I can learn from, in C++.
```

You need Claude Code (the desktop app's browser pane reads posts best, and elsewhere Claude falls
back to WebFetch), Python 3, and a compiler or runtime for your language. C++ (g++, CMake and
Ninja) has the most complete templates. Learners can still solve any workbook in any of the eight
built-in languages, and the checker tells them how to install a missing one. Some workbooks need a
library to compute expected answers (the TrueType one uses fontTools); Claude asks before
downloading anything.

## How it builds a workbook

1. Claude reads the post and extracts the headings, text and code blocks. That copy stays on your
   machine, and Claude leaves it out of the workbook.
2. It maps the post to assignments. Each snippet or idea becomes an assignment with an
   input/output contract, an independent source of expected answers, a difficulty, and its file in
   the project layout (modelled on the author's, when they published code). You approve the map
   and the layout before Claude writes anything.
3. It scaffolds the workbook: the checker, image comparison, the problem book builder, check
   scripts and the README.
4. Claude writes one complete model assignment first, then the rest (in parallel, for long posts).
   Each gets a problem page, a boilerplate starter, a reference solution written from scratch, and
   a test generator.
5. It checks the checks (see above) and folds the independent solver's feedback into the pages.
6. To hand the workbook over, Claude writes the blank starters and builds the problem book. The
   workbook ships without `solutions/`: `tools/project.py` creates your project when you choose a
   language.

## Roadmap

- Textbook chapters as input, alongside blog posts.
- Ready-made boilerplate templates for more languages.
- More workbooks in [techblog-workbooks](https://github.com/knmn2000/techblog-workbooks).

## Contributing

Issues and pull requests are welcome: bugs in the checker or the book, ideas for the workflow, or
posts that broke it. To share a workbook you made, open a pull request on
[techblog-workbooks](https://github.com/knmn2000/techblog-workbooks).

## Repository layout

```
.claude-plugin/              plugin and marketplace manifests
skills/blog-to-leetcode/
  SKILL.md                   the workflow Claude follows
  references/                mapping a post to assignments, test trust, authoring guide, languages
  scripts/                   reading the post, scaffolding a workbook, stripping hints
  assets/workbook-template/  checker, image comparison, book builder and template, check scripts
  assets/lang/cpp/           the learner's project skeleton (CMake, README), an optional canvas
  assets/example-assignment/ a complete worked assignment, laid out as in a workbook
docs/screenshots/
```

## Respecting authors

Workbooks link to the post's sections and explain the ideas in their own words. They don't copy
the post's text or code, and Claude writes the reference solutions from the specification rather
than the author's repository.

## Licence

[Apache License 2.0](LICENSE). Copyright 2026 knmn2000.
