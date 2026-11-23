# Contributing

Reports about **other camera models** are the most useful thing here. Make sure the camera is yours and keep unique identifiers out.

Before a pull request, run:

```bash
python tools/check_payload.py
```

`patch_reuse` must stay a 0-byte file, and everything in [`sdcard/`](sdcard/) must stay byte-identical to the tested payload. If you never opened those files in an editor, they are fine.

In an issue write: app name and version, connection type (4G / Wi-Fi / Ethernet), mainboard or `Hwname` if you actually saw it, whether `update_record` appeared, and whether the app accepted the ID. **Mask the ID.** No camera video, QR payloads, IMEIs, serials or config backups.

Label your result **confirmed**, **partially confirmed** or **untested**. A generic "V380" box says nothing about compatibility.
