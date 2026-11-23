#!/usr/bin/env python3
"""Small offline validation of the V380 payload tooling (never touches a camera)."""
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

subprocess.run([sys.executable, str(ROOT / "tools" / "verify_payload.py")], check=True)

with tempfile.TemporaryDirectory() as tmp:
    rebuilt = Path(tmp) / "sdcard.zip"
    subprocess.run(
        [sys.executable, str(ROOT / "tools" / "rebuild_patch.py"), "--output", str(rebuilt)],
        check=True,
    )
    assert rebuilt.is_file()
    published = ROOT / "releases" / "microSD-files-only.zip"
    with zipfile.ZipFile(rebuilt) as fresh, zipfile.ZipFile(published) as shipped:
        assert sorted(fresh.namelist()) == sorted(shipped.namelist()), "ZIP file lists differ"
        for name in fresh.namelist():
            assert fresh.read(name) == shipped.read(name), f"{name} differs from the published ZIP"

print("Offline self-tests passed")
