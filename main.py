"""make.fun bounty entry: Worst Superpower.

Writes the single entry line to entry.txt inside MAKEFUN_OUTPUT_DIR
(fallback /output). Python stdlib only, no network, no clock, no local
imports, no hardcoded paths. Deterministic and byte-identical across runs.
"""

import os

ENTRY = (
    "I can sense exactly when a stranger somewhere on Earth is "
    "thinking about me \u2014 I just never find out who, or what "
    "they thought."
)


def gate(line):
    """Refuse any line that would fail the bounty gate."""
    if not line:
        raise ValueError("entry is blank")
    if line != line.strip():
        raise ValueError("entry has leading/trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if not 1 <= len(line) <= 140:
        raise ValueError("entry must be 1-140 characters, got %d" % len(line))


def main():
    gate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # No trailing newline: write the exact bytes of the line.
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    # Verify the round-trip: what landed on disk must be byte-identical
    # to the gated line, otherwise fail loudly instead of shipping a
    # subtly different entry.
    with open(path, "rb") as f:
        written = f.read()
    if written != ENTRY.encode("utf-8"):
        raise RuntimeError("entry.txt round-trip mismatch")


if __name__ == "__main__":
    main()
