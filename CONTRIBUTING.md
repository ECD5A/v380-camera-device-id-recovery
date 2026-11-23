# Contributing / Вклад в проект

Reports of **new confirmed camera models** are especially valuable. Please verify that the camera is yours and avoid publishing unique identifiers.

Before opening a pull request, run the offline checks on your computer:

```bash
python tools/verify_payload.py
python tools/test_tools.py
```

The files in [`sdcard/`](sdcard/) must stay byte-identical to the verified payload — `patch_reuse` is intentionally a 0-byte file, so never open and save it in an editor.

When opening an issue, share: V380 app name/version, Wi-Fi vs. 4G vs. Ethernet (if known), the **mainboard** model/firmware `Hwname` if actually observed, whether `update_record` appeared, and whether the **owner's** app accepted `last_id`. **Redact the ID**. Do not attach live-camera video, QR payloads, IMEIs, serial numbers, or internal configuration backups.

Clearly label your results **confirmed**, **partially confirmed**, or **untested**. Do not claim broad compatibility from package design or generic product names.
