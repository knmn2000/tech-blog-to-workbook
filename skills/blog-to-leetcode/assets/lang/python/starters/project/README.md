# {{NAME}}

<!-- One or two sentences: what the program does, in the learner's terms. -->

Built step by step with the workbook "{{TITLE}}", following {{AUTHOR}}'s post
[{{SOURCE_TITLE}}]({{SOURCE_URL}}).

## Install and run

Needs Python 3.10 or newer. Install the package in editable mode, so your changes take effect
without reinstalling:

```
pip install -e .
{{NAME}} <!-- arguments -->
```

To run it without installing, put `src/` on the import path:

```
PYTHONPATH=src python -m {{NAME}} <!-- arguments -->
```

In PowerShell, set the path with `$env:PYTHONPATH = "src"` first.

## How it's organised

| Where | What |
|---|---|
<!-- One row per subpackage of src/{{NAME}}/, in the post's terms. -->
| `assignments/` | One small program per step, which the workbook's checker runs on that step's test cases |
