#!/usr/bin/env python3
"""Audit the three published microSD payload files against the observed successful run."""
import hashlib
import struct
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

# 1. The card folder must hold exactly the three shipped files and nothing else.
present = sorted(p.relative_to(SD).as_posix() for p in SD.rglob("*") if p.is_file())
if present != sorted(EXPECTED):
    extra = [p for p in present if p not in EXPECTED]
    missing = [p for p in EXPECTED if p not in present]
    raise SystemExit(f"Unexpected sdcard/ contents.\nExtra: {extra}\nMissing: {missing}")

# 2. Byte-for-byte identity with the payload of the successful run.
payload = {}
for rel, sha in EXPECTED.items():
    data = (SD / rel).read_bytes()
    payload[rel] = data
    actual = hashlib.sha256(data).hexdigest()
    if actual != sha:
        raise SystemExit(f"MISMATCH {rel}\nExpected {sha}\nFound {actual}")
    print(f"OK {rel} ({len(data)} bytes)")

if payload["patch_reuse"] != b"":
    raise SystemExit("patch_reuse must stay a 0-byte file, as in the successful attempt")

patch = payload[PATCH_REL]
script = (ROOT / "source" / "exshell_bfu.sh").read_bytes()
if hashlib.md5(patch).hexdigest() != "288032472d4d508105188fadf5a3ae8e":
    raise SystemExit("Patch MD5 mismatch")
if b"V380E6_G1" not in patch[:0x80] or patch[0x80:0x80+len(b"exshell_bfu.sh")] != b"exshell_bfu.sh":
    raise SystemExit("Unexpected patch header")
if patch[0xc0:] != script:
    raise SystemExit("Embedded script differs from source")
if struct.unpack_from("<I", patch, 0xb8)[0] != len(script):
    raise SystemExit("Embedded script size mismatch")
print("OK MD5, patch header, script bytes and length")

# 3. The downloadable ZIP must contain the same three files with the same bytes.
if RELEASE_ZIP.is_file():
    with zipfile.ZipFile(RELEASE_ZIP) as archive:
        names = archive.namelist()
        if sorted(names) != sorted(EXPECTED) or any(archive.read(n) != payload[n] for n in names):
            raise SystemExit(f"{RELEASE_ZIP.name} does not match sdcard/")
    print(f"OK {RELEASE_ZIP.relative_to(ROOT).as_posix()} matches sdcard/")
else:
    print(f"SKIP {RELEASE_ZIP.relative_to(ROOT).as_posix()} is not present")

print("NOTE: these checks do NOT prove camera compatibility or safety.")
