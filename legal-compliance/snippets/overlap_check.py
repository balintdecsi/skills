"""Measure textual overlap between a source you learned from and work you wrote.

Use before claiming "written from scratch" in a README, a licence audit, or a courtesy
email to an author. A measured result is evidence; an assumption is how false statements
get published.

    python overlap_check.py <source_dir> <derived_dir>

Reports, separately for prose and code:
  - exact shared lines (set intersection after normalisation)
  - near-matches above a similarity threshold (difflib ratio)

Interpreting the output: bare imports, single standard-library calls and canonical
one-liners are *expected* to match and are not copying — there is only one way to write
them (merger / scenes a faire). Shared *prose*, shared comments, or matching multi-line
logic are the real signals. Read every hit; the count alone proves nothing.
"""

import json
import sys
from difflib import SequenceMatcher, get_close_matches
from pathlib import Path

SOURCE_GLOBS = ("*.py", "*.md", "*.ipynb", "*.R", "*.sql")
MIN_CHARS = 20  # ignore lines too short to carry protectable expression
NEAR_MATCH_RATIO = 0.90

# Vendored and generated trees are not the author's expression, and walking a .venv
# turns a two-second check into an unusable one.
SKIP_DIRS = {
    ".git", ".venv", "venv", "env", "node_modules", "site-packages", "__pycache__",
    ".ipynb_checkpoints", ".mypy_cache", ".pytest_cache", "build", "dist", ".tox",
}


def _normalise(text: str) -> list[str]:
    """Whitespace-collapsed lines long enough to carry protectable expression."""
    out = []
    for line in text.splitlines():
        stripped = " ".join(line.split())  # collapse indentation and internal whitespace
        if len(stripped) >= MIN_CHARS:
            out.append(stripped)
    return out


def _add_notebook(path: Path, buckets: dict[str, set[str]]) -> None:
    """Notebooks must be parsed, not read as text — raw JSON never matches a .py line."""
    try:
        nb = json.loads(path.read_text(encoding="utf-8", errors="ignore"))
    except (OSError, ValueError):
        return
    for cell in nb.get("cells", []):
        bucket = "prose" if cell.get("cell_type") == "markdown" else "code"
        buckets[bucket].update(_normalise("".join(cell.get("source", []))))


def _collect(root: Path) -> dict[str, set[str]]:
    """Split a directory's lines into prose and code buckets."""
    buckets: dict[str, set[str]] = {"prose": set(), "code": set()}
    for pattern in SOURCE_GLOBS:
        for path in root.rglob(pattern):
            if SKIP_DIRS & set(path.parts):
                continue
            if path.suffix == ".ipynb":
                _add_notebook(path, buckets)
            else:
                bucket = "prose" if path.suffix == ".md" else "code"
                buckets[bucket].update(_normalise(path.read_text(encoding="utf-8", errors="ignore")))
    return buckets


def _near_matches(source: set[str], derived: set[str]) -> list[tuple[float, str, str]]:
    """Pairs above the ratio threshold, excluding the exact matches already reported.

    `get_close_matches` prefilters on length and character overlap before running the full
    comparison, which keeps this tractable on a whole repository.
    """
    candidates = sorted(source)
    hits = []
    for d in derived - source:
        match = get_close_matches(d, candidates, n=1, cutoff=NEAR_MATCH_RATIO)
        if match:
            hits.append((SequenceMatcher(None, d, match[0]).ratio(), d, match[0]))
    return sorted(hits, reverse=True)


def main(source_dir: str, derived_dir: str) -> None:
    source = _collect(Path(source_dir))
    derived = _collect(Path(derived_dir))

    for bucket in ("prose", "code"):
        exact = source[bucket] & derived[bucket]
        total = len(derived[bucket])
        print(f"\n=== {bucket}: {len(exact)} exact / {total} lines in derived work ===")
        for line in sorted(exact):
            print(f"  EXACT  {line[:110]}")

        for ratio, d, s in _near_matches(source[bucket], derived[bucket]):
            print(f"  ~{ratio:.2f}  {d[:100]}")
            print(f"         vs {s[:100]}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
