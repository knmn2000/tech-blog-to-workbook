# Worked example: checkpoint 07 of the TrueType workbook

A complete checkpoint from the first workbook built with this skill, from
"Writing a tiny TrueType parser and renderer from scratch" (yayo1.com). Copy its shape.

| File | What to notice |
|---|---|
| `problem-07-simple-glyph.md` | Every section of the page template; the byte-layout tables; Example 1 walks through real bytes; requirements R1-R8; four hints that each give away more |
| `blank-p07_simple_glyph.cpp` | What the learner gets by default: the header comment and an empty `main` (made by `tools/blank_starters.py`) |
| `boilerplate-p07_simple_glyph.cpp` | The optional starter: input/output code provided; one function to write; exit 99 on NotImplemented. Authors write this one as `solutions/p07_simple_glyph.cpp` |
| `reference-p07_simple_glyph.cpp` | Same I/O code; written from the spec, not the blog |
| `gen_p07.py` | Expected values from fontTools; hand-made byte strings checked by fontTools before use; real-font cases; random glyphs per seed; `explain` mapping output locations to requirements |
| `cases-excerpt.txt` | The case-file format the checker reads |

Results when it was built: 151 tests; the reference passed, the stub stopped with "Not implemented
yet", five planted bugs failed (the blog's own repeat-flag bug fails 81 tests), and an independent
solver working from the page alone passed all 151.
