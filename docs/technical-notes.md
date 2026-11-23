# Technical notes: V380 local-update probe

This document distinguishes **actual test evidence** from **firmware-mechanism hypotheses**.

## Confirmed artifact layout

```text
/sdcard/
  local_update.conf
  patch_reuse                  # empty, 0 bytes
  updatepatch/
    288032472d4d508105188fadf5a3ae8e.patch
```

`local_update.conf` contents:

```ini
[PATCH]
patchmd5=288032472d4d508105188fadf5a3ae8e
```

The `.patch` MD5 is identical to the `patchmd5` value and its file stem. The header includes `V380E6_G1`. The patch contains a plaintext shell script named `exshell_bfu.sh`; **the embedded script's expected output was not observed on the tested camera**. The patch also has an **inferred**, not independently verified, 16-bit checksum field (byte sum modulo 65536). While the exact bytes yielded a successful `update_record` result on one camera, we do not claim a fully reverse-engineered patch format or a guaranteed harmless parser path.

**Naming trap:** some V380 firmware variants look for `localupdate.conf`. This tested payload uses **`local_update.conf`** (with underscore). **Do not rename the file.**

## Likely execution model (not proven end-to-end)

1. The camera boots with a FAT32 microSD card.
2. A firmware-specific update handler examines `local_update.conf` and possibly `patch_reuse`.
3. The handler may validate the patch filename / MD5 and parse its model-specific header.
4. The handler may record patch status/ID by creating `update_record` and might run a pre-update script (`exshell_bfu.sh`).
5. On this camera, `update_record` was created and `last_id` was accepted by V380 Pro. The diagnostic script's separate output was **absent**.

Therefore, **do not claim that the embedded script recovered the ID**. The supported claim is **the local-update trigger caused the camera to create `update_record`, which exposed an app-accepted Device ID**.

## Why the first microSD experiment was not sufficient

The previously tried directory structure:

```text
AutoTestFile/release/autotest_init.sh
```

was documented for **some other V380 firmware**. A file sitting on the card is not enough; the camera must have a matching startup hook and permission to execute it. The user observed only normal video recording (`RecFiles/`). On this one camera, the hook did not yield a result.

## Security limitations

- This is an **update-system** experiment, not a factory-authorized export feature.
- A package without kernel images is **not automatically safe**. The updater can still update metadata, write flash or reboot, depending on firmware.
- Never use the sample device identifiers from other people's issue reports. All numbers used in tutorials are fictional.
- The payload's `V380E6_G1` header is **not confirmed** as the actual board's `Hwname`.
- Reading ID is **not** the same as repairing 4G SIM detection or establishing an Ethernet link.

## Script for auditing

[`source/exshell_bfu.sh`](../source/exshell_bfu.sh) is exactly the script embedded inside the binary test patch. It attempts to read Linux settings and write a summary to `V380_ID_RESULT/00_RESULT.txt` on microSD. That output was **not found**. Its presence in the patch is useful for transparency, but copying this `.sh` to the root of microSD **does not execute it**.

## Independently reproducing the package

- Run `python tools/verify_payload.py` to check the included files, the known MD5, SHA-256, header, embedded script, and that `releases/microSD-files-only.zip` matches `sdcard/`.
- Run `python tools/rebuild_patch.py` to reconstruct the binary package from the checked-in source and repack `releases/microSD-files-only.zip`. It must match the published `.patch` byte for byte.
- `sdcard/patch_reuse` must stay a 0-byte file. An editor that adds text to it changes the verified payload layout.

These operations run **on your own computer**, require only standard Python 3, and never connect to the camera or change its memory.
