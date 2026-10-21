# Worked example: checkpoint 07 of the TrueType workbook

A complete checkpoint from the first workbook built with this skill, from
"Writing a tiny TrueType parser and renderer from scratch" (yayo1.com). The files sit where they
sit in a workbook; copy their shape.

| File | What to notice |
|---|---|
| `workbook-excerpt.json` | How the checkpoint is registered: its entry program (`solution`), the project files it creates (`files`), the earlier ones it can use (`buildsOn`), and each file's one-line purpose. Checkpoints 10 and 12 show a file one checkpoint creates and a later one adds to (`extends`) |
| `problems/07-simple-glyph.md` | Every section of the page template; the paragraph under "The problem" names the checkpoint's files and what the boilerplate leaves to write; byte-layout tables; Example 1 walks through real bytes; requirements R1-R8; four hints that each give away more |
| `starters/blank/` | What the learner gets by default: comment-only project files and an entry program with an empty `main` (all written by `tools/blank_starters.py`) |
| `starters/boilerplate/` | The optional start: the entry program's input/output done, the project files' declarations in the author's names, and TODO bodies that throw `not implemented: <name>` (the entry program turns that into exit 99) |
| `_spoilers/project/` | The reference project's files for this checkpoint, at the same paths, written from the spec, not the blog. The entry program is the boilerplate's, and the boilerplate headers are these headers |
| `_spoilers/project/src/utils/Geometry.h` | A file several checkpoints add to (10, then 12, 13 and 15): each addition sits under a `// ---- Checkpoint NN ----` marker, so `-Ref` and the Editorial for checkpoint 10 see the file without the later answers |
| `tools/gen_p07.py` | Expected values from fontTools; hand-made byte strings checked by fontTools before use; real-font cases; random glyphs per seed; `explain` mapping output locations to requirements |
| `tests/07/cases-excerpt.txt` | The case-file format the checker reads |

Results when it was built: 151 tests; the reference passed, the boilerplate stopped with "Not
implemented yet: readGlyph", five planted bugs failed (the blog's own repeat-flag bug fails 81
tests), an independent solver working from the page alone passed all 151, and the whole series
built and passed in order, checkpoint by checkpoint.
