#!/usr/bin/env python3
"""Read a camera-generated V380 update_record locally without uploading its ID."""
import argparse
from pathlib import Path
import re

parser = argparse.ArgumentParser(description="Print the last_id field from a V380 update_record file")
parser.add_argument("path", type=Path, help="Path to update_record file or its parent SD-card directory")
args = parser.parse_args()
path = args.path / "update_record" if args.path.is_dir() else args.path
try:
    data = path.read_bytes().decode("utf-8", errors="replace")
except (OSError, ValueError) as exc:
    parser.exit(2, f"Unable to read {path}: {exc}\n")
found = re.search(r"(?im)^\s*last_id\s*=\s*([0-9]{6,20})\s*$", data)
if found:
    print("Possible V380 Device ID:", found.group(1))
    print("Verify manually in V380 Pro. Do not post this number in public.")
else:
    print("No numeric last_id found. File headings/keys:")
    for line in data.splitlines():
        if line.startswith("[") or "=" in line:
            print("  ", line.split("=", 1)[0].strip())
    raise SystemExit(1)
