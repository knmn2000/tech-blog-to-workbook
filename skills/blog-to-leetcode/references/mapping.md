# Mapping a blog to checkpoints

A checkpoint is one program with one input/output contract. This file covers how to find the
checkpoints in a post, how to design each contract, and how to present the map to the user.

## Contents
1. What makes a good checkpoint
2. Posts with code
3. Posts with pseudocode
4. Posts with no code
5. Designing the contract
6. The map you show the user
7. A worked map (TrueType renderer, 22 snippets -> 18 checkpoints)

## 1. What makes a good checkpoint

- **One idea.** It teaches one thing the post explains: a format, an algorithm, a rule, a
  mechanism. The learner writes roughly 20-150 lines.
- **Observable.** Its result can be written as text (or a picture) and compared exactly or within
  a stated tolerance.
- **Independent oracle exists.** Something other than your own reference can produce the expected
  output: an established library, exact arithmetic, a brute-force method, a simulation written
  differently, a hand calculation for small cases. If nothing does, see section 4.
- **Standalone.** Its input includes whatever earlier checkpoints would have produced.

Aim for one checkpoint per substantive section of the post, plus a capstone that runs the whole
pipeline. 6-20 checkpoints is typical.

## 2. Posts with code

Go through every code block and label it:

| Label | Meaning | What happens to it |
|---|---|---|
| logic | Does real work: parsing, an algorithm, a transform | Becomes a checkpoint (or part of one) |
| data | Struct/class declarations, constants | Becomes types in the starter, or the output format |
| demo | A `main` that calls things | Becomes example input; nothing to implement |
| fix | Changes an earlier block | Merge with the block it fixes **if the output is the same**; a separate "Part II" checkpoint only if the observable result differs (e.g. lines-only vs curves) |
| glue | Build files, imports, I/O helpers | Provided in the starter |

Then for each checkpoint:
- **Scope = the snippet's scope.** If the snippet supports one format, one platform or one case,
  so does the checkpoint. Say what's out of scope in Constraints.
- **Bugs: follow the spec.** Note every place the snippet is wrong (read it carefully: off-by-one,
  sign handling, lost state across recursion, typos comparing x with y). The tests require correct
  behaviour, and "After you pass" mentions the difference neutrally ("something to look for").
  Check how often the bug would matter on real data; that's a good fact for the page.
- **Two blocks with the same output become one checkpoint.** Output-only tests can't tell a first
  version from its fix if both produce the right answer. Make the fix's subject (the trap it
  handles) a requirement and a hint instead.

## 3. Posts with pseudocode

Treat the pseudocode as the snippet: same scope, same steps. The contract's input is the
pseudocode's input (as text lines) and its output the pseudocode's result. Your reference is a
faithful transcription in the learner's language. The oracle is usually a brute-force or library
implementation of the same mathematical task, or small cases worked by hand.

## 4. Posts with no code

The post explains how something works (a protocol, a storage engine, a scheduler, a cache
policy) without code. Every such idea still has a **testable kernel**: a function that captures
the mechanism with clear inputs and outputs. Look for these, in roughly this order:

| Kernel | Example post content | Contract |
|---|---|---|
| A state machine | "a follower that hears a higher term steps down" | input: initial state + event list; output: state after each event |
| A computation | "the offset is the base plus the record's position" | input: parameters; output: the number |
| A data-structure operation | "compaction keeps the latest value for each key" | input: operations; output: resulting contents |
| A policy decision | "evict the least recently used entry" | input: capacity + access sequence; output: hits/misses and evictions |
| A protocol step | "the leader commits once a majority acknowledges" | input: acknowledgements over time; output: commit index after each |
| An encoding | "varints use 7 bits per byte" | input: values; output: bytes (and back) |
| A simulation | "requests are routed to the node owning the hash range" | input: nodes + keys; output: owner of each key |

For each kernel:
- **Cite the passage.** Every requirement says which part of the post it comes from, since there is
  no snippet to stay true to. If the post is vague, choose the simplest reading that agrees with
  every sentence, state it as a requirement, and say so on the page.
- **Oracle.** Prefer an established library that implements the same thing. Otherwise write the
  oracle in a different style from your reference (e.g. brute force or a direct simulation of the
  definition) and require both to agree on every case, plus property checks (invariants the post
  states).
- **The capstone** is usually a small end-to-end simulation of the system the post describes.

## 5. Designing the contract

- **Text, line based.** Input lines start with a keyword (`font <path>`, `glyph <id> <offset>
  <length>`, `lookup U+0041`); output lines too. One output record per input request, in order.
  Canonical formatting (integers plainly, words not symbols), and the checker normalises
  whitespace.
- **Include what earlier checkpoints produce.** E.g. "decode the record at this offset" rather than
  "find the glyph for this character".
- **Make each output detailed enough to localise mistakes.** Separate lines for separate concerns
  (header, list, points), named tuple fields (`points=x,y,curve`) so the checker can say exactly
  which field differs, and an `explain` mapping from output location to likely requirement.
- **Pick the comparison:** `records` (line by line, named tuples, optional numeric tolerance),
  `unordered` (same lines, any order: map/set outputs), `image band=1 allow=...` (pictures, edges
  may move one pixel).
- **Pictures:** PNG (or binary PPM) at an output path ending in `.png`. Define the rule precisely
  (e.g. "a pixel is filled when its centre is inside"), allow 1-pixel edge movement, and keep
  canvases under about 600 x 600 pixels.
- **Floating point:** state the tolerance in the requirement and print enough digits.
- **Errors:** if a case can't be done (unsupported format, end of data), the output is a defined
  line (`unsupported`, `eof`), not a crash.

## 6. The map you show the user

A table, one row per checkpoint:

| # | Checkpoint | Built from | Contract (one line) | Oracle | Difficulty |
|---|---|---|---|---|---|

Below it: what you merged or dropped and why, the blog's bugs you found and how the tests treat
them, and anything you need to download. Get approval before authoring.

## 7. A worked map

*Writing a tiny TrueType parser and renderer from scratch* (C++, 22 code blocks):

| # | Checkpoint | Built from | Contract | Oracle |
|---|---|---|---|---|
| 01 | Read big-endian numbers | byte readers | file + read ops -> values | Python struct |
| 02 | Read the table directory | constructor | font -> table records (any order) | struct + fontTools |
| 03 | Map characters to glyphs | cmap snippet | font + code points -> glyph ids | fontTools cmap |
| 04 | Locate glyph records | loca snippet | font + glyph ids -> offset, length | fontTools loca |
| 05 | Read the horizontal metrics | hhea/hmtx snippet | font + glyph ids -> advance, lsb | fontTools hmtx |
| 06 | Draw on a framebuffer | canvas snippet + demo | draw commands -> PNG | reference validated geometrically |
| 07 | Decode simple glyphs | glyph structs + parser | record offset -> contours and points | fontTools glyf |
| 08 | Draw an outline with lines | outline renderer + demo | outline -> PNG | reference validated against points |
| 09 | Resolve compound glyphs | compound parser | records -> transformed outlines | fontTools getCoordinates |
| 10 | Lerp and Bezier | geometry helper | params -> point | exact fractions |
| 11 | Draw an outline with curves | curve renderer | outline -> PNG | fontTools pen decomposition |
| 12 | Intersect two segments | geometry helper | segments -> point or none | exact fractions |
| 13 | Line x quadratic curve | geometry helper | curve + line -> points | exact arithmetic |
| 14 | Even-odd fill | even-odd v1 + its vertex fix (merged) | outline -> PNG | fontTools PointInsidePen |
| 15 | Lowest point of a curve | geometry helper | curve -> min y | exact fractions |
| 16 | Non-zero fill, lines | non-zero for lines | polygon -> PNG | PointInsidePen |
| 17 | Non-zero fill, curves | non-zero with curves | outline -> PNG | PointInsidePen |
| 18 | Render a line of text | the post's goal (capstone) | font + text -> PNG | fontTools cmap/hmtx/outlines + PointInsidePen |

Bugs found and tested against: on-curve flag lost for repeated points (42 of 90 ASCII glyphs
affected), last glyph never checked for emptiness, glyphs past numberOfHMetrics without metrics,
1-byte component offsets read unsigned, nested compound transforms dropped, a scanline compared
with an x coordinate, non-zero filling only counts above zero.
