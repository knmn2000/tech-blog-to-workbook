# Languages: choosing one, and switching

A workbook is authored in one language: its starters, boilerplate and reference project are in
it, and `assets/lang/<lang>/` has its project skeleton (only C++ so far). The learner can still
build the project in any language, because the checker only reads output. Set up only the
language the learner picks: nothing is created for the others.

## Contents
1. Asking which language
2. What a project looks like in each language
3. Setting up a project in another language
4. Switching later

## 1. Asking which language

When the learner opens or sets up a workbook with no project yet, run `py -P tools/langs.py` (it
lists the eight languages, which are installed, and the install command for the rest) and ask
which one they want, as a question with options:

- the workbook's own language first, saying it comes with the boilerplate and the Editorial's
  solutions, and whether it's installed;
- the other installed languages;
- languages that aren't installed, with what installing them takes.

For the workbook's language, run `py -P tools/project.py setup`. For another one, follow
section 3. If a tool is missing, say what you'd install, from where and roughly how big, and get
a yes first.

## 2. What a project looks like in each language

The layout is the same in every language: the same folders and module names, in the language's
own file naming. Checkpoint programs stay in `checkpoints/` so they're easy to tell from the
project.

| Language | Build file | Project code (example) | The finished program | Checkpoint programs | Build and run one checkpoint |
|---|---|---|---|---|---|
| C++ | `CMakeLists.txt` | `src/font/Cmap.h`, `src/font/Cmap.cpp` | `src/main.cpp` | `checkpoints/p03_cmap.cpp` | `cmake --build build/solutions --target p03`, then `build/solutions/p03` |
| C | `CMakeLists.txt` | `src/font/cmap.h`, `src/font/cmap.c` | `src/main.c` | `checkpoints/p03_cmap.c` | as C++ |
| Python | `pyproject.toml` | `<package>/font/cmap.py` | `<package>/__main__.py` (`python -m <package>`) | `checkpoints/p03_cmap.py` | none; run with the project folder on `PYTHONPATH` |
| JavaScript | `package.json` (`"type": "module"`) | `src/font/cmap.js` | `src/main.js` | `checkpoints/p03_cmap.js` (imports `../src/...`) | `node solutions/checkpoints/p03_cmap.js` |
| TypeScript | `package.json` | `src/font/cmap.ts` | `src/main.ts` | `checkpoints/p03_cmap.ts` | `node --experimental-strip-types ...` (Node 22.6+) |
| Go | `go.mod` | `font/cmap.go` (package `font`) | `cmd/<name>/main.go` | `checkpoints/p03/main.go` | `go build -o build/solutions/p03 ./checkpoints/p03` |
| Rust | `Cargo.toml` | `src/font/cmap.rs` (with `mod` lines in `src/lib.rs` and `src/font/mod.rs`) | `src/main.rs` | `src/bin/p03_cmap.rs` | `cargo build --bin p03_cmap`, then `target/debug/p03_cmap` |
| Lua | none | `<package>/font/cmap.lua` | `main.lua` | `checkpoints/p03_cmap.lua` | `lua` with `LUA_PATH` including `solutions/?.lua` |

Module names keep the post's terms. File names follow each language's habit: C++ keeps the
author's (`FontParser.cpp`), Python, Rust, Lua, C and Go use snake_case (`font_parser.py`), and
JavaScript and TypeScript use camelCase (`fontParser.js`). Third-party code the workbook gives the
project (`project.copy`) needs an equivalent in the new language, or a note that the learner
writes that part too (for example a PNG writer, or a binary PPM, which the checker also reads).

## 3. Setting up a project in another language

1. **Install what's missing**, with consent (section 1).
2. **Make the skeleton** in `solutions/` from the table: the build file, a README like the
   workbook's own project README (what the program does, how to build and run it, how it's
   organised, the post it follows), a `.gitignore` for its build output, and the folders.
3. **Point the workbook at it.** The tools read `workbook.json`, so keep the authored version as
   `workbook.<language>.json` (for example `workbook.cpp.json`) and change the copy the tools
   read: `project.language` and `languageLabel`; `setup`, `build` and `run` (one checkpoint, from
   the table; `{id}` is the checkpoint number); `project.build` and `project.run` (the finished
   program); and each checkpoint's `solution`, `files`, `extends` and `buildsOn` in the new
   language's names. Leave `project.reference` and `reference` alone.
4. **Write the blank starters** for the new paths with `py -P tools/blank_starters.py` (the
   purposes in `project.purposes` need the new paths as keys too). Opening a checkpoint then
   creates its files as usual.
5. **Tell the learner what changes:** the Boilerplate button and the Editorial's solution stay in
   the workbook's language (still useful to read), and `-Ref` proves the workbook's own reference.
   Everything else works the same: Run, Submit, Re-check solved, the Files panel and the finish
   card.
6. **Check it:** run `.\check 01` on the blank starter ("Not started yet"), then build one
   checkpoint end to end with a quick throwaway solution in a copy of the workbook, so the
   commands are known to work before the learner starts.

## 4. Switching later

The learner asks you; the book has no language menu, so nothing switches by accident.

1. Ask which language (section 1), and say what happens to the current project.
2. **Never delete the current project.** With the learner's yes, rename `solutions/` to
   `solutions-<language>/` (for example `solutions-cpp/`). It stays a complete repository they can
   keep, push or come back to, and the book's "Solved" marks stay in the browser.
3. Set up the new language as in section 3. If they switch back, restore the matching
   `workbook.<language>.json` and rename the folders back.
