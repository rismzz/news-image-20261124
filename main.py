#!/usr/bin/env python3
"""Entry point for news-image-20261124 (program/v1).

Verifies the pre-rendered broadsheet entry.png (PNG magic, IHDR 1024x1024,
at most 1 MiB) and copies it byte-for-byte to $MAKEFUN_OUTPUT_DIR/entry.png
(default /output). Stdlib only, no network, deterministic.
"""
import hashlib
import os
import struct
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
MAX_BYTES = 1024 * 1024


def main():
    with open(SRC, "rb") as fh:
        data = fh.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        sys.exit("entry.png is not a PNG file")
    if len(data) > MAX_BYTES:
        sys.exit(f"entry.png is {len(data)} bytes, over the 1 MiB cap")
    if data[12:16] != b"IHDR":
        sys.exit("entry.png has no IHDR chunk where one is expected")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        sys.exit(f"entry.png is {width}x{height}, expected 1024x1024")
    # The sealed runner executes this file twice and requires both runs to
    # write identical bytes; copying the checked PNG guarantees that.
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    with open(out_path, "wb") as fh:
        fh.write(data)
    with open(out_path, "rb") as fh:
        written = fh.read()
    if written != data:
        sys.exit("output differs from entry.png")
    if len(written) > MAX_BYTES:
        sys.exit(f"output is {len(written)} bytes, over the 1 MiB cap")
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {out_path}: {len(data)} bytes sha256={digest}")


if __name__ == "__main__":
    main()
