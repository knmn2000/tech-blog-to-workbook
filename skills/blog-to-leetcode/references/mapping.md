# Mapping a blog to checkpoints

A checkpoint is one step of a real project: a properly named file the learner writes, plus a
small entry program with one input/output contract that the checker runs. This file covers how to
find the checkpoints in a post, how to lay out the project they add up to, how to design each
contract, and how to present the map to the user.

## Contents
1. What makes a good checkpoint
2. Posts with code
3. Posts with pseudocode
4. Posts with no code
5. Designing the contract
6. The project layout
7. The map you show the user
8. Sketches: three kinds of post

## 1. What makes a good checkpoint

- **One idea.** It teaches one thing the post explains: a format, an algorithm, a rule, a
  mechanism. The learner writes roughly 20-150 lines.
- **Observable.** Its result can be written as text (or a picture) and compared exactly or within
  a stated tolerance.
- **Independent oracle exists.** Something other than your own reference can produce the expected
  output: an established library, exact arithmetic, a brute-force method, a simulation written
  differently, a hand calculation for small cases. If nothing does, see section 4.
- **Standalone tests.** Its input includes whatever earlier checkpoints would have produced, so
  its tests only depend on the earlier files the learner chooses to import.
- **A home in the project.** Its logic lives in a named file of the project layout (section 6),
  where later checkpoints can import it.

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

- **Text, line based.** Input lines start with a keyword (`file <path>`, `record <offset>
  <length>`, `get user:42`); output lines too. One output record per input request, in order.
  Canonical formatting (integers plainly, words not symbols), and the checker normalises
  whitespace.
- **Include what earlier checkpoints produce.** E.g. "decode the record at this offset" rather than
  "find the record for this key", when finding it is an earlier checkpoint's job.
- **Make each output detailed enough to localise mistakes.** Separate lines for separate concerns
  (header, list, items), named tuple fields (`items=key,value,flag`) so the checker can say exactly
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

## 6. The project layout

The learner should finish with a project, not a folder of exercises. Before writing the map,
sketch the file tree a real implementation of the post would have, and give every checkpoint a
place in it.

- **Mirror the author.** If the post or the author's repository shows file and folder names, use
  them. Looking at a repository's list of files is fine; never read or copy its code. Where the
  author keeps several steps in one big file, either give each step its own file in a folder named
  after it (a `font/` folder for a `FontParser`, holding `cmap`, `loca`, ...), or let later
  checkpoints extend the earlier file when that's how the code really grows (another method on the
  same type, a fix).
- **No layout to mirror?** Use the language's usual conventions, and name files after the post's
  own terms, so the tree reads as a summary of the post.
- **One home per checkpoint.** Each checkpoint names the file(s) it creates or extends. A
  checkpoint that fixes an earlier one extends that file.
- **Imports run one way.** Later files import earlier ones, never the reverse, so the project
  builds at every point in the series. Small helpers that several steps use (byte reading, a
  canvas, geometry) get their own early files.
- **Entry programs stay thin.** Each checkpoint's entry program (`solutions/pNN_slug.<ext>`) reads
  the test input, calls the project and writes the output. It's test scaffolding, like a real
  project's tests or examples, so nothing later should need to import it.
- **The capstone is the real program**: the project's `main`, doing what the post's finished
  program does.
- **Aim for recognisable.** Someone who knows the author's repository should see its shape in the
  learner's: the main modules and folders, if not every file. Other languages keep the same
  module names in their own naming conventions (`references/languages.md`).

## 7. The map you show the user

A table, one row per checkpoint:

| # | Checkpoint | Built from | File(s) | Contract (one line) | Oracle | Difficulty |
|---|---|---|---|---|---|---|

Beside it, the project tree the learner ends up with, and the author's tree when there is one
(file names only). Below them: what you merged or dropped and why, the blog's bugs you found and
how the tests treat them, and anything you need to download. Get approval before authoring.

## 8. Sketches: three kinds of post

These show the shape of a map, not a finished one. A real map has every checkpoint, the bugs
found in the snippets, and the downloads needed.

**A post with code** (e.g. building a log-structured key-value store, Go):

| # | Checkpoint | Built from | File(s) | Contract | Oracle |
|---|---|---|---|---|---|
| 01 | Encode a record | record struct + `encode` | `record.go` | key, value -> bytes (hex) | Python `struct` |
| 02 | Replay the log | `Open` + read loop | `log.go` | log file -> final key/value pairs | a dict replaying the same writes |
| 03 | Build the hash index | index snippet | `index.go` | log file -> key -> offset | offsets computed while writing the test log |
| 04 | Compact | compaction snippet + its fix (merged) | `compact.go` | log -> compacted log contents | the dict from 02 |
| 05 | Recover from a torn write | recovery snippet | extends `log.go` | log with a truncated tail -> pairs kept | hand-made cases, checked by 02's oracle |
| 06 | The store end to end (capstone) | the post's goal | `cmd/kv/main.go` | operations -> results | a dict |

The learner's tree at the end: `record.go`, `log.go`, `index.go`, `compact.go` and `cmd/kv/main.go`,
plus one thin entry program per checkpoint.

**A post with pseudocode** (e.g. a consensus algorithm's leader election): one checkpoint per
procedure (handle a vote request, handle a vote reply, the election timer), each in its own file
of a `raft/` package and each as events in -> state after each event out, with a brute-force or
library simulation as the oracle, and a capstone that runs a small cluster from a scripted event
list.

**A post with no code** (e.g. how rate limiters work): one kernel per mechanism (fixed window,
sliding log, token bucket), each a file in a `limiter/` folder sharing one interface, and each as
capacity + request times in -> allowed/denied per request out, with a direct simulation of the
post's definition as the oracle; the capstone compares all three on the same traffic.

`assets/example-checkpoint/` has one finished checkpoint from a past run, for the shape of the
files (page, starters, reference, generator, cases); its subject doesn't matter.
