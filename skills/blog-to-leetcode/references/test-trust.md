# Making the tests trustworthy

A wrong test must never block a learner who writes correct code, and a learner with a real bug
must not pass. Either failure defeats the purpose of the workbook. Use this file to produce
expected values, check the checks, and handle a learner's dispute.

## Contents
1. Where expected values come from
2. Checking the checks (the gate before an assignment counts as done)
3. Tolerances: pictures and numbers
4. The independent solver
5. Messages that help
6. Disputes

## 1. Where expected values come from

Expected outputs must come from a source independent of your reference solution, recorded per test
(the case's `source` line, printed with every failure):

| Source | Use for |
|---|---|
| An established library (fontTools, Python's `struct`, `zlib`, `sqlite3`, a reference implementation published by the spec's authors) | Parsing, encoding, formats |
| Exact arithmetic (`fractions.Fraction`, `decimal` at high precision) | Geometry and numerics |
| A brute-force or definition-level method written in a different style | Algorithms, policies, simulations |
| Hand calculation, shown in the generator | Small worked examples |
| Your reference, validated against one of the above | Pictures (the reference draws, the oracle checks sampled pixels) |

Before the generator writes a hand-made input (special byte strings, edge cases), the oracle
decodes it and the generator compares the result with what you intended: if your hex encodes
something else, the generator stops.

Generators are deterministic for a given `--seed`, and you commit the default seed's output.
Random cases carry the seed in their id, so `-Fresh` produces new ones the learner hasn't seen.

## 2. Checking the checks

An assignment counts as done only when all of these hold:

1. The reference passes with Accepted on the committed cases and on at least two fresh seeds. `-Ref`
   checks the reference project as it stands after this assignment, so this also proves the
   project builds at this point in the series, with no file depending on a later one.
2. The boilerplate says "Not implemented yet" (exit code 99) instead of crashing, and the blank
   starter says "Not started yet".
3. At least three planted bugs fail, each with a message that points at the right place. Plant
   realistic mistakes: the blog's own bugs first, then off-by-one, sign, endianness, wrong rule,
   missing case. A planted bug that passes means a missing test: add a case instead of tightening
   a tolerance.
4. At least one different-but-correct variant passes wherever a tolerance exists (pictures,
   floats), e.g. sampling pixel rows at the top instead of the centre, or truncating instead of
   rounding. A correct variant that fails means the tolerance or the spec is too strict.
5. Every requirement has cases, and every case names one requirement.
6. The independent solver passes (section 4).
7. You measure real-data coverage, e.g. by running the reference over every record in the real
   data (every entry in a file, every row of a dataset), beyond the sample in the tests.

Build planted bugs and variants as text substitutions on copies of the reference, compiled into
your own build folder, and run them with `.\check NN -Run "<program> {input} {output}"`.

## 3. Tolerances: pictures and numbers

For pictures, `tools/imageio.py` classifies each pixel by the expected image's palette and
forgives a differing pixel only when it is an edge that moved by up to `band` pixels:
- extra ink (expected background) if the expected image has that ink within `band`;
- missing ink if the learner's image has that ink within `band`;
- a different colour if either image has the other's colour within `band`.

This accepts anti-aliasing, a different line or scanline algorithm, and slivers thinner than a
pixel closing up, while a stray line, a missing shape or a filled hole fails. An `allow` fraction
(e.g. 0.0002) absorbs a handful of isolated pixels. Make thin features at least ~2 pixels wide in
expected images, or different correct samplings will disagree.

If you validate a reference picture against an inside/outside oracle, a pixel centre that lies on
an edge can go either way (a validation tie). Detect it by nudging the point by 1e-6 in four
directions; if the answers differ, don't count a disagreement.

For numbers, state the tolerance in the requirement (`tolerance=0.001`) and design cases so the
exact answer isn't near a decision boundary unless the case is about that boundary (then use
exact integer data).

## 4. The independent solver

A separate agent solves the assignment using only what the learner gets. Use a subagent if your
tool has them, or a fresh session that has seen none of your work:
- the problem page with hints and "After you pass" removed (`scripts/strip_hints.py`);
- the starter file and provided headers;
- the data files the examples reference, and the input data files;
- no tests, no reference, no blog, no web.

It may compile and run the page's examples. Then you run the full suite against its program. If it
fails, the page is unclear or a test is wrong; fix whichever before shipping. Ask it to list every
ambiguity and assumption, and act on them. Use a smaller model than yours for this, if you can
choose one: it's closer to a learner who relies on the page.

## 5. Messages that help

For every failure the checker prints:
- the test id and its title (what the input is);
- the first difference in plain terms
  (`points[12]: expected (x=530, y=0, curve=on), got (x=530, y=0, curve=off) - differs in curve`);
- the requirement it points to (from the case file's `explain` line);
- where the expected value came from;
- the command that reproduces it.

For pictures it adds a diff image. A summary line names the requirement most failures point to.

Use `explain` only where output locations map to requirements; for pictures, any difference could
come from any requirement, so leave it out.

## 6. Disputes

`.\check NN -Dispute <test-id> "reason"` records the dispute in `disputes.json` and sets the test
aside, so the verdict reads "Accepted (1 disputed)" and the learner isn't blocked.

To review the learner's disputes:
1. Reproduce: `.\check NN -Case <test-id>` with their solution.
2. Recompute the expected value from its source (run the generator's oracle code for that case, or
   call the library yourself) and re-read the requirement and the spec section.
3. If the test is wrong: fix the generator (not the case file), regenerate, rerun every step of
   section 2, and tell the learner what was wrong.
4. If the test is right: show the evidence (the oracle's output, the spec's wording, a worked
   calculation) and point at the line of their output that differs and why.
5. Close it: set `"status": "closed"` and add `"resolution"`.
