#!/usr/bin/env python3
"""Copy entry.png to the output directory the harness provides.

The copy is unconditional; only a structurally broken source file is an error,
so the entrypoint exits non-zero for a corrupt PNG and for nothing else.
"""

import os
import shutil
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
DST = os.path.join(OUT_DIR, "entry.png")

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def check_source(path):
    """Return (width, height) or raise ValueError if the file is not a usable PNG."""
    with open(path, "rb") as fh:
        head = fh.read(24)
    if len(head) < 24 or head[:8] != PNG_MAGIC:
        raise ValueError("entry.png is not a PNG (bad magic)")
    if head[12:16] != b"IHDR":
        raise ValueError("entry.png has no leading IHDR chunk")
    width, height = struct.unpack(">II", head[16:24])
    if width < 1 or height < 1 or width > 4096 or height > 4096:
        raise ValueError("entry.png has implausible dimensions %dx%d" % (width, height))
    if os.path.getsize(path) < 100:
        raise ValueError("entry.png is truncated")
    return width, height


def main():
    try:
        width, height = check_source(SRC)
    except (OSError, ValueError) as exc:
        raise SystemExit("broken entry.png: %s" % exc)
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, DST)
    print("copied %s (%dx%d) -> %s" % (SRC, width, height, DST))


if __name__ == "__main__":
    main()
