# Worked example: assignment 07 of the TrueType workbook

This folder holds a complete assignment from the first workbook built with this skill, from
"Writing a tiny TrueType parser and renderer from scratch" (yayo1.com). The files are at the paths
they have in a workbook; copy their shape.

| File | What to notice |
|---|---|
| `workbook-excerpt.json` | How the assignment is registered: its program the checker runs (`solution`), the project files it creates (`files`), the earlier ones it can use (`buildsOn`), the learner's job in every file it touches (`jobs`), and each file's purpose (`project.purposes`). Jobs and purposes become the starters' headers and the book's Start here card. Assignments 10 and 12 show a file one assignment creates and a later one adds to (`extends`) |
| `problems/07-simple-glyph.md` | Every section of the page template; "The problem" opens with one plain paragraph on what the program does (the files and jobs are on the Start here card); key terms defined where they first appear; byte-layout tables; Example 1 walks through real bytes; requirements R1-R8; four hints that each give away more |
| `starters/blank/` | What the learner gets by default: every file starts with a header (the assignment, why the file exists, your job, how to start) and nothing else, plus an empty `main` in the program (all written by `tools/blank_starters.py`) |
| `starters/boilerplate/` | The default start: the same kind of header, the program's input/output done, the project files' declarations, and TODO bodies that throw `not implemented: <name>` (the program turns that into exit 99) |
| `_spoilers/project/` | The reference project's files for this assignment, at the same paths, written from the spec, not the blog. The entry program is the boilerplate's, and the boilerplate headers are these headers |
| `_spoilers/project/src/utils/Geometry.h` | A file several assignments add to (10, then 12, 13 and 15): each addition sits under a `// ---- Assignment NN ----` marker, so `-Ref` and the Editorial for assignment 10 see the file without the later answers |
| `tools/gen_p07.py` | Expected values from fontTools; hand-made byte strings checked by fontTools before use; real-font cases; random glyphs per seed; `explain` mapping output locations to requirements |
| `tests/07/cases-excerpt.txt` | The case-file format the checker reads |

At build time, the assignment had 151 tests. The reference passed, the boilerplate stopped
with "Not implemented yet: readGlyph", and five planted bugs failed (the blog's own repeat-flag bug
fails 81 tests). An independent solver working from the page alone passed all 151, and the whole
series built and passed in order, assignment by assignment.
