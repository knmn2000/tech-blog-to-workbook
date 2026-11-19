# {{NAME}}

<!-- One or two sentences: what the program does, in the learner's terms. -->

Built step by step with the workbook "{{TITLE}}", following {{AUTHOR}}'s post
[{{SOURCE_TITLE}}]({{SOURCE_URL}}).

## Run it

Needs Node.js 22 or newer (`node --version`). The project is plain ES modules: nothing to
install and nothing to build.

```
node src/main.js <!-- arguments -->
```

## How it's organised

| Where | What |
|---|---|
<!-- One row per folder of src/, in the post's terms. -->
| `assignments/` | One small program per step, which the workbook's checker runs on that step's test cases |
