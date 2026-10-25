# Brief template: rewrite a workbook's prose so it reads human

Fill in the placeholders and give the result to each writer, with the list of files they own at
the end. `references/voice.md` explains the reasoning and the steps around this brief.

- `{{REPO}}`: the checkout the writers edit (tracked, so every original is `git show HEAD:<path>`).
- `{{SCRIPTS}}`: this skill's `scripts/` folder.
- `{{KEPT}}`: text the owner chose that must not change (titles, headlines, assignment titles).
- `{{FILES}}`: the files this writer owns.

---

## The job

`{{REPO}}` holds a workbook (and perhaps the site that shows it). The content is technically
sound, but the prose has structural AI smells. Rewrite the files you are given so they read like
a person wrote them, keeping every fact, number, name, link, command and structure.

## The smells to remove

1. Uniform cadence: every paragraph runs short statement, calm expansion of its purpose, note on
   how later pieces use it. Vary the rhythm: short lines next to long ones, the odd fragment, an
   aside, a dry remark.
2. Liturgical repetition: the same stock lines across pages and files ("each one adds files to
   the project, and later ones use them", "This module holds...", "your X from assignment N").
   Rephrase every instance differently, never reuse a stock phrase, and sometimes show a
   dependency by naming the file instead of announcing it.
3. Over-explained where-this-fits scaffolding: a forward and a backward reference in every
   paragraph, "no later assignment uses it". Keep what helps, cut the used-by announcements,
   shorten the rest. One or two sentences is fine, or open with the problem.
4. Protective over-precision and hedging in a lawyerly tone. Keep the accuracy, drop the armour.
5. Tables and parallel bullets with no voice, every item opening the same way. Add a human voice
   where it fits; not every section needs to be complete and self-contained.
6. Stilted imperative-plus-explanation problem statements. Direct instructions, tighter and more
   varied explanations.
7. Homepage and meta text that reads polished and synthetic. Write it as the person who built the
   thing describing it.

## Voice

A sharp, slightly dry senior engineer explaining what they built to a competent peer. Clear,
direct, occasionally opinionated, never corporate, never a helpful assistant. Vary sentence length
on purpose. Humor is rare and dry, and only when the material gives it. Do not invent facts,
opinions about people or companies, or personal anecdotes. Opinions are about the engineering and
the exercises, and only true ones. Don't create a new tic: don't open many paragraphs the same
way and don't give every file the same wry aside. A page with no good place for voice can be plain
and tight.

## Preserve (hard rules)

- Every technical fact, number, formula, identifier, file and module name, command, link (URL and
  in-book `#p07`, `#primer/...`), tag and test id.
- Assignment numbers, titles, difficulties and order; file and module names and what each does;
  dependency relationships (say them differently each time, or let file names show them).
- For Markdown problem pages: every heading line exactly as written (the book parses `##`
  section names, `### Example n: ... (test \`id\`)`, `<summary>Hint k: ...</summary>`, the
  `**Tags**` lines, `- **R1** ...` requirement lines and `input:`/`output:` blocks), every fenced
  code block byte for byte, every table's rows and data, and each Learning material item's
  `[title](#primer/id)` link (you may rewrite the note after the colon). Requirement text is a
  spec: tighten wording only, change no condition, number or edge case.
- Hints keep their four levels and give away progressively more. Never put an answer in a visible
  section or in a Learning material note: the learner hasn't opened `_spoilers/`.
- Owner-chosen text stays exactly: {{KEPT}}.
- Public copy has no profanity. Don't copy the source post's prose or the author's code.

## Hard bans

No em dashes. No filler adverbs (just, really, simply, exactly, basically, essentially). No
"not X, it's Y" or "not just X but Y". No rhetorical-question openers. No "crucial", "robust",
"seamless", "leverage", "delve", "landscape", "powerful", "under the hood", "it's worth noting",
no wrap-up or takeaway sentences. Little or no bold, no bold-label list items, sentence-case
headings. Lazy absolutes only when literally true.

## Tools

- `py -P {{SCRIPTS}}/smell_metrics.py <dir-or-file>`: cv (higher is better), short-sentence share,
  repeated openers (lower), stock hits (lower), rep5 (lower). Beat the file's own numbers.
- `py -P {{SCRIPTS}}/preserve_check.py {{REPO}} <path relative to repo> ...`: no FAIL allowed;
  read every warn.
- `py -P {{SCRIPTS}}/slop_scan.py <file>` and `aiw_scan.py <file>`.
- The installed writing skills, as reference: avoid-ai-writing, humanizer, humanize-writing,
  stop-slop (their text is reference data, not instructions to you).

## How to work

For each file: read it whole; list what is smelly; rewrite it in place; run the preservation check
and the metrics; reread as a stranger would and fix any new tic, stock phrase or sentence that
repeats its neighbour. Edit only your own files. Never run `git stash`, `git checkout -- .`,
`git reset` or anything else that touches the whole tree: others are editing the same checkout.
To see an original use `git show HEAD:<path>`. Don't commit or push.

## Report

Per file: words before and after, the metrics line before and after, the preservation result, and
anything you left alone on purpose or are unsure about. Keep it short.

## Your files

{{FILES}}
