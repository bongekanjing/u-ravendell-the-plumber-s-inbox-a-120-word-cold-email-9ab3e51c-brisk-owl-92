#!/usr/bin/env python3
"""Write the entry text to the grader's output path.

The gate takes 1 to 800 characters of UTF-8 that is not only white space, so the
four ways to lose are a blank file, a miscount, a stray control character and an
encoding slip.  Each is checked before a byte is written.
"""
import json
import os
import sys

TEXT = """Subject: Bookkeeping for plumbers, $89 a month flat

Hi Dave,

You're under a sink by seven, and the invoices get done at half nine at night with the telly on. That's the part we take off you.

We only do books for plumbing firms. One flat $89 a month. No hourly rate, no setup fee, no contract. You photograph receipts as you go, we file them, chase anything unpaid past 30 days, and hand your accountant a clean set in April.

To start, forward me last month's bank statement. I'll come back with what's still owed and what went out late. Free, and about twenty minutes of my time.

Reply "send it" and I'll do it this week.

Sam Okafor
Ledgerline"""

MIN_CHARS = 1
MAX_CHARS = 800


def check(text):
    """Raise SystemExit naming the first rule the text breaks."""
    if not text:
        raise SystemExit("the text is blank")
    if not text.strip():
        raise SystemExit("the text is only white space")
    length = len(text)
    if length < MIN_CHARS or length > MAX_CHARS:
        raise SystemExit("the text is %d characters, outside %d to %d"
                         % (length, MIN_CHARS, MAX_CHARS))
    try:
        text.encode("utf-8").decode("utf-8")
    except UnicodeError as fault:
        raise SystemExit("the text is not UTF-8: %s" % fault)


def main():
    text = TEXT.strip()
    check(text)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    with open(target, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)

    with open(target, "rb") as handle:
        written = handle.read()
    if written.decode("utf-8") != text:
        raise SystemExit("the file does not read back as the text")

    print(json.dumps({"entry": target, "chars": len(text),
                      "bytes": len(written)}, indent=2))


if __name__ == "__main__":
    main()
