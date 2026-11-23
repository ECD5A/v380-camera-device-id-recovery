#!/usr/bin/env python3
# Copyright (c) 2026 Vladimir Stelmak.
# SPDX-License-Identifier: MIT
#
# V380 Device ID Recovery
# Pulls a V380 / V380 Pro camera Device ID out through a microSD card.
#
# Author: Vladimir Stelmak
# GitHub: https://github.com/ECD5A
#
# Module: tools.check_payload
# Purpose: проверяет хеши пакета, структуру патча, релизный ZIP и пересборку.
#
# Сам пакет только читается: ни один файл карты здесь не перезаписывается.
#
"""Offline payload check: hashes, patch structure, release ZIP and rebuild equality."""
import hashlib
import struct
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SD = ROOT / "sdcard"
RELEASE_ZIP = ROOT / "releases" / "microSD-files-only.zip"
PATCH_REL = "updatepatch/288032472d4d508105188fadf5a3ae8e.patch"
EXPECTED = {
    "local_update.conf": "4d0443f75449d080eb967a80320087f254acf0927ad973998f8f1b9a441d7295",
    "patch_reuse": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    PATCH_REL: "ba254a416b540e841860220e2edfa0061113147d40c3bcdf9a5e4e6317e91ca2",
}


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def main():
    # The card folder holds exactly the three shipped files, nothing else.
    present = sorted(p.relative_to(SD).as_posix() for p in SD.rglob("*") if p.is_file())
    if present != sorted(EXPECTED):
        extra = [p for p in present if p not in EXPECTED]
        missing = [p for p in EXPECTED if p not in present]
        raise SystemExit(f"Unexpected sdcard/ contents\nExtra: {extra}\nMissing: {missing}")

    payload = {}
    for rel, expected_hash in EXPECTED.items():
        data = (SD / rel).read_bytes()
        payload[rel] = data
        actual = sha256(data)
        if actual != expected_hash:
            raise SystemExit(f"MISMATCH {rel}\nExpected {expected_hash}\nFound {actual}")
        print(f"OK {rel} ({len(data)} bytes)")

    if payload["patch_reuse"]:
        raise SystemExit("patch_reuse must stay a 0-byte file")

    patch = payload[PATCH_REL]
    script = (ROOT / "source" / "exshell_bfu.sh").read_bytes()
    if hashlib.md5(patch).hexdigest() != "288032472d4d508105188fadf5a3ae8e":
        raise SystemExit("patch MD5 mismatch")
    if b"V380E6_G1" not in patch[:0x80] or patch[0x80:0x80 + len(b"exshell_bfu.sh")] != b"exshell_bfu.sh":
        raise SystemExit("unexpected patch header")
    if patch[0xc0:] != script:
        raise SystemExit("embedded script differs from source/exshell_bfu.sh")
    if struct.unpack_from("<I", patch, 0xb8)[0] != len(script):
        raise SystemExit("embedded script length mismatch")
    print("OK patch MD5, header, embedded script")

    with zipfile.ZipFile(RELEASE_ZIP) as archive:
        names = archive.namelist()
        if sorted(names) != sorted(EXPECTED) or any(archive.read(n) != payload[n] for n in names):
            raise SystemExit(f"{RELEASE_ZIP.name} does not match sdcard/")
    print(f"OK {RELEASE_ZIP.relative_to(ROOT).as_posix()} matches sdcard/")

    with tempfile.TemporaryDirectory() as tmp:
        rebuilt = Path(tmp) / "sdcard.zip"
        subprocess.run(
            [sys.executable, str(ROOT / "tools" / "rebuild_patch.py"), "--output", str(rebuilt)],
            check=True,
        )
        with zipfile.ZipFile(rebuilt) as fresh, zipfile.ZipFile(RELEASE_ZIP) as shipped:
            if sorted(fresh.namelist()) != sorted(shipped.namelist()):
                raise SystemExit("rebuilt ZIP file list differs")
            for name in fresh.namelist():
                if fresh.read(name) != shipped.read(name):
                    raise SystemExit(f"rebuilt {name} differs from the published ZIP")
    print("OK rebuild from source/ matches the published ZIP")
    print("Checks passed. This does not prove camera compatibility or safety.")


if __name__ == "__main__":
    main()
