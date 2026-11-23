#!/usr/bin/env python3
# V380 / V380 Pro - Device ID recovery through microSD.
# Copyright (c) 2026 ECD5A
# Licensed under the MIT License.
# https://github.com/ECD5A/v380-camera-device-id-recovery
# SPDX-License-Identifier: MIT
"""Rebuild the archived V380 experimental patch deterministically (offline)."""

from pathlib import Path
import argparse
import hashlib
import struct
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ZIP_TIMESTAMP = (2026, 11, 23, 0, 0, 0)

parser = argparse.ArgumentParser(description="Rebuild a local-update package for auditing only")
parser.add_argument("--output", type=Path, default=ROOT / "releases" / "microSD-files-only.zip")
args = parser.parse_args()

source = (ROOT / "source" / "exshell_bfu.sh").read_bytes()
name = b"V380E6_G1"  # From original experimental package; actual tested board unknown
header = bytearray(0x80)
struct.pack_into("<I", header, 0, 10)
header[4:4+len(name)] = name
struct.pack_into("<I", header, 0x14, 0x1f4b59)
struct.pack_into("<I", header, 0x18, 1)
entry = bytearray(0x40)
entry[:len(b"exshell_bfu.sh")] = b"exshell_bfu.sh"
struct.pack_into("<I", entry, 0x38, len(source))
struct.pack_into("<I", entry, 0x3c, sum(source) & 0xFFFF)  # Experimental/inferred checksum
patch = bytes(header) + bytes(entry) + source
patch_md5 = hashlib.md5(patch).hexdigest()
filename = f"updatepatch/{patch_md5}.patch"
conf = f"[PATCH]\npatchmd5={patch_md5}\n".encode("utf-8")

original = ROOT / "sdcard" / "updatepatch" / "288032472d4d508105188fadf5a3ae8e.patch"
if patch != original.read_bytes():
    parser.exit(2, "Rebuilt patch differs from observed success payload; refusing to publish.\n")
if conf != (ROOT / "sdcard" / "local_update.conf").read_bytes():
    parser.exit(2, "local_update.conf does not match reconstructed patch.\n")

args.output.parent.mkdir(parents=True, exist_ok=True)
# Fixed timestamps keep the archive reproducible; only the three card files are packed.
with zipfile.ZipFile(args.output, "w", zipfile.ZIP_DEFLATED) as archive:
    for arcname, data in (("local_update.conf", conf), ("patch_reuse", b""), (filename, patch)):
        info = zipfile.ZipInfo(arcname, date_time=ZIP_TIMESTAMP)
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o644 << 16
        archive.writestr(info, data)

print("Saved only the three card files:", args.output)
print("Patch MD5:", patch_md5)
print("Patch SHA-256:", hashlib.sha256(patch).hexdigest())
print("ZIP SHA-256:", hashlib.sha256(args.output.read_bytes()).hexdigest())
