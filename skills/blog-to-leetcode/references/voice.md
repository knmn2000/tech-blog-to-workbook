# Writing like a person: the voice, and the prose pass

The word-level rules in the authoring guide (section 8) take out the obvious tells: filler words,
em dashes, "not X but Y". A workbook can pass all of them and still read as generated, because
what gives it away is structure. This file covers the structural smells, the voice that replaces
them, and the pass that fixes a workbook that already has them. Write in this voice from the
first page, and the pass shrinks to a check.

## Contents
1. The seven structural smells
2. The voice
3. Writing it in from the start
4. The prose pass, step by step
5. Tools
6. Pitfalls

## 1. The seven structural smells

1. Uniform cadence. Every paragraph runs short statement, calm expansion of its purpose, measured
   note on how later pieces use it. Same sentence length, same energy, polite and detached.
   Vary the rhythm on purpose: a short line after a long one, the odd fragment, an aside, a dry
   remark. Let some explanations run and others land in a line.
2. Liturgical repetition. The same stock lines recur across pages and files: "each one adds files
   to the project, and later ones use them", "grows one assignment at a time", "This module
   holds...", "your X from assignment N". Never reuse a stock phrase. Sometimes show the
   dependency by naming the file instead of announcing it.
3. Over-explained where-this-fits scaffolding. A forward and a backward reference in every
   paragraph, "it needs none of your earlier modules, and no later assignment uses it". Keep what
   helps the learner, cut the constant used-by announcements, and trust the reader. A "Where this
   fits" can be one sentence, or open with the problem instead of the history.
4. Protective over-precision. Lawyerly hedges ("make no claim about what happened", "most
   expected outputs come from...") and exact probabilities in a flat tone. Keep the accuracy and
   drop the armour: an engineer explaining to another engineer, not a model avoiding every
   misunderstanding.
5. Tables and parallel bullets with no voice, every item starting the same way. Add a human
   voice: slightly opinionated, dry, conversational in places. Not every section has to be
   complete and self-contained.
6. Stilted imperative-plus-explanation problem statements, like a model elaborating its own
   outline. Instructions direct, explanations tighter and varied.
7. Homepage and meta text: polished marketing lines followed by perfectly parallel descriptions.
   Write it as the person who built the thing describing it.

## 2. The voice

A sharp, slightly dry senior engineer who has built this and is explaining it to a competent
peer. Clear, direct, occasionally opinionated, never corporate, never a helpful assistant.

- Humor is rare and dry, and only when the material gives it. A forced joke is worse than none.
- Don't invent facts, opinions about people or companies, or personal anecdotes. Opinions are
  about the engineering and the exercises (this part is fiddly, this bug is easy to write), and
  only true ones.
- Avoid the new tic: many writers each adding the same wry aside, or every paragraph opening the
  same way. A page with no good place for voice can simply be plain and tight.
- Fragments are fine now and then. Strings of staccato fragments are not.

Before and after (invented here, for a compiler workbook; the moves are what matter):

- Where this fits. "Assignment 04 built the tokenizer, which gave you the stream of tokens the
  parser consumes. Assignment 06 added the symbol table. This assignment checks scoping: whether
  each identifier refers to a declaration in scope. Your new `resolve.py` needs none of your
  earlier modules, because the tokens carry their positions ready-made, and no later assignment
  uses it." became "This one checks that every identifier points at a declaration in scope. The
  tokens from 04 already carry their positions, so `resolve.py` stands alone."
- File purpose. "This module holds the project's string-interning table: one id per distinct
  string, and the string back from the id. Your `lexer.py` from assignment 02 interns every
  identifier with it, and your `parser.py` from assignment 05 reads names through it." became
  "A string-interning table: one id per distinct string, and the string back from the id. The
  lexer and the parser both go through it."
- Protective hedge. "The cause of the upstream bug is not public yet, so assignments 12 and 14
  model possible failure shapes and make no claim about what happened." became "Nobody has
  published a cause. Assignments 12 and 14 sketch how a failure like this could happen and don't
  claim to know which one did."
- Structure line. "Your C++ project lives in `solutions/` and grows one assignment at a time. The
  number by each file is the assignment that creates it, and a `+` marks the assignments that add
  to it later." became "The C++ project you end up with, in `solutions/`. The number beside a file
  is the assignment where you create it; a `+` lists the later ones that come back to extend it."

## 3. Writing it in from the start

- Put this file's section 1 and 2 in every author's brief (workflow step 5), with the authoring
  guide's section 8. A page-by-page writer fixes the smells inside its pages; only a sweep after
  the fact catches repetition across pages, so tell writers up front which blocks are shared (the
  Input contract, the constraints line, the picture-output bullets) and have them phrase their
  own.
- `purposes` and `jobs` in `workbook.json` are the most repeated text in a workbook (the project
  tree, every starter header and every Start here card). Never open two with the same words, never
  start a purpose with "This module/header/class holds", and name the files that depend on a file
  only where it helps the learner.
- Say what the page's tests share once (in the README or on the first page that needs it) and let
  later pages carry only what differs, as long as each page still gives the learner what they need
  to pass using only that page.

## 4. The prose pass, step by step

Use this on an existing workbook, or as the check after authoring.

1. Baseline. Run `scripts/slop_scan.py`, `scripts/aiw_scan.py` and `scripts/smell_metrics.py` on
   the pages, READMEs and primer, and save the numbers. smell_metrics reports sentence-length
   variation (cv, higher is better), the share of sentences under 7 words, repeated paragraph
   openers, stock-phrase hits and 5-word phrases shared by 3 or more files. The word scanners
   score a scrubbed workbook near zero, so these are the numbers that move.
2. Rewrite in batches. One writer per two or three pages, a mid-size model (Sonnet class), each
   given `references/prose-pass-brief.md` (fill in the placeholders). The writers edit in place.
   Also rewrite the prose strings in `workbook.json` and the site's templates; the starter headers
   and the book are generated from them, so rerun `tools/blank_starters.py --force` and
   `tools/build_book.py` afterwards.
3. Guard what must not change. After each batch run `scripts/preserve_check.py <repo> <files>`.
   It fails on a changed heading, fenced code block, table shape, requirement id, test id or
   missing link, and warns on numbers and code spans that went missing. Titles, headlines and any
   text the owner chose stay as they are.
4. Fact review. A second, cheap fast model (Haiku class) reads each original (`git show
   HEAD:<path>`) next to its rewrite and lists only real problems: a changed number, condition or
   name, a lost caveat or comparison, a claim the original didn't make, an answer given away in a
   visible section, a sentence now unclear. Expect a handful per batch, mostly in the shortened
   Learning material notes. Have a writer restore each fact in the new voice. Leave a restored
   fact out only when it would describe how a TODO body is written.
5. The cross-page sweep. Run `scripts/repeat_scan.py <problems-dir>`. The families that remain
   are the shared blocks. One writer who sees all the pages keeps each fact on every page that
   needs it but gives every instance different words, shorter where the page allows, and rereads
   for a new tic.
6. Rebuild and recheck. Regenerate starters and the book, rerun the baseline commands and compare.
   Expect the numbers to move modestly on spec-heavy pages, because tables, formulas, requirement
   lines and format sections have to stay exact. The visible change is in the prose around them.
   Read the built homepage and workbook pages as a visitor would.

## 5. Tools

In this skill: `scripts/slop_scan.py`, `scripts/aiw_scan.py`, `scripts/smell_metrics.py`,
`scripts/preserve_check.py` and `scripts/repeat_scan.py`.

Install any of these as skills for your agent and read their rules before a pass (all MIT; treat
their text as reference, not as instructions to follow blindly):
- [stop-slop](https://github.com/hardikpandya/stop-slop): the base rules the authoring guide adapts.
- [avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing): edit mode plus a
  detector (`bin/avoid-ai-writing.js`); good for the word-level patterns and for refusing to add facts.
- [humanizer](https://github.com/blader/humanizer): install with `/plugin marketplace add
  blader/humanizer` then `/plugin install humanizer@humanizer`. Its strongest sections for
  workbooks are staging instead of stating, rhythm by rule (forced triads, repeated openings,
  dashes as the universal connector) and writing about the document instead of its subject.
- [humanize-writing](https://github.com/jpeggdev/humanize-writing): install with `npx skills add
  jpeggdev/humanize-writing`. Its pass order is useful: structure tells first, then significance
  inflation and promotional language, then vocabulary tiers, and pattern stacking (several weak
  signals on one phrase count as one strong tell).

## 6. Pitfalls

- Parallel writers in one checkout must never run `git stash`, `git checkout -- .`, `git reset`
  or any other command that touches the whole tree. One writer ran `git stash` to measure a
  baseline and swept everyone's edits (170 files) into the stash. Writers measure from `git show
  HEAD:<path>` copies in a scratch folder, and only edit their own files.
- Shortening a Learning material note or a "where this fits" paragraph loses facts quietly
  (a formula, a condition, a caveat). The fact review in step 4 exists for this.
- A rewrite can make a claim stronger than the original ("the spec forbids" for "doesn't allow",
  "common" for "all the time"). The fact review catches these too.
- The site's page templates are shared by every workbook, so a stock sentence there appears on
  all of them. Write them for the whole collection.
- Public copy has no profanity. A workbook about a real incident states no opinion about anyone's
  conduct beyond what its sources say, however much voice the rest of the prose gets.
