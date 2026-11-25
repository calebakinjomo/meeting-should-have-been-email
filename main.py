#!/usr/bin/env python3
"""The Meeting That Should Have Been an Email — make.fun entry program.

Writes a single one-line joke (max 200 characters) about a meeting that
should have been an email to /output/entry.txt, the deliverable the
program/v1 harness scores. The joke lives in one constant so the entry
text is byte-identical on every run, and the program re-reads what it
wrote to prove the file on disk matches that constant exactly.
"""

import os
import sys

# The entry: one line, plain text, no second line, no setup needed.
# The turn lands on the last word — the calendar invite itself gives up.
ENTRY = "The meeting was so unnecessary even the calendar invite tried to decline itself."

MAX_CHARS = 200


def validate_entry(text: str) -> None:
    """Guard the gate: 1-200 UTF-8 chars, a single non-blank line."""
    if not text or text.isspace():
        raise ValueError("entry must not be blank")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if len(text) > MAX_CHARS:
        raise ValueError(f"entry is {len(text)} chars, over the {MAX_CHARS} limit")
    text.encode("utf-8")  # raises if not valid UTF-8


def resolve_output_path() -> str:
    """Prefer the harness path /output/entry.txt; fall back locally."""
    harness_path = "/output/entry.txt"
    try:
        os.makedirs("/output", exist_ok=True)
        with open(harness_path, "a", encoding="utf-8"):
            pass
        return harness_path
    except OSError:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.txt")


def main() -> int:
    validate_entry(ENTRY)
    out_path = resolve_output_path()
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(ENTRY)
    # Round-trip guard: the file on disk must match the entry exactly,
    # so a partial write or encoding slip can never ship silently.
    with open(out_path, "r", encoding="utf-8") as fh:
        written = fh.read()
    if written != ENTRY:
        raise ValueError(f"round-trip mismatch in {out_path}: wrote {len(written)} chars, expected {len(ENTRY)}")
    print(f"Wrote {len(ENTRY)}-char entry to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
