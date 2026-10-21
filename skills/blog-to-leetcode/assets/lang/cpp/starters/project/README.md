# {{NAME}}

<!-- One or two sentences: what the program does, in the learner's terms. -->

Built step by step with the workbook "{{TITLE}}", following {{AUTHOR}}'s post
[{{SOURCE_TITLE}}]({{SOURCE_URL}}).

## Build and run

Needs CMake 3.20 or newer and a C++20 compiler.

```
cmake -S . -B build
cmake --build build
./build/{{NAME}} <!-- arguments -->
```

## How it's organised

| Where | What |
|---|---|
<!-- One row per folder of src/, in the post's terms. -->
| `assignments/` | One small program per step, which the workbook's checker runs on that step's test cases |
