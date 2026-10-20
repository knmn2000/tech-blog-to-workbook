"""Makes the copy of a problem page that the independent solver gets: no hints, and no
"After you pass" section (it names the author's approach and the snippet's bugs).

    python strip_hints.py problems/07-simple-glyph.md <solver-folder>/problem.md
"""

import re
import sys
from pathlib import Path


def strip(markdown: str) -> str:
    text = re.sub(r"<details>.*?</details>\s*", "", markdown, flags=re.S)
    text = re.sub(r"^## Hints\s*$.*?(?=^## |\Z)", "", text, flags=re.S | re.M)
    text = re.sub(r"^## After you pass.*?(?=^## |\Z)", "", text, flags=re.S | re.M)
    return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    source, target = Path(sys.argv[1]), Path(sys.argv[2])
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(strip(source.read_text(encoding="utf-8")), encoding="utf-8")
    print(f"wrote {target}")
