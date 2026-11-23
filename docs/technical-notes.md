# Technical notes: how the local update works

What is proven on the tested camera, and what is still a hypothesis.

## Confirmed layout

```text
/sdcard/
  local_update.conf
  patch_reuse                  # empty, 0 bytes
  updatepatch/
    288032472d4d508105188fadf5a3ae8e.patch
```

`local_update.conf`:

```ini
[PATCH]
patchmd5=288032472d4d508105188fadf5a3ae8e
```

The MD5 matches the file stem and the `patchmd5` value. The header carries `V380E6_G1`. Inside the patch: a header, one entry record and a plaintext shell script `exshell_bfu.sh`. The 16-bit checksum field is **inferred** (byte sum modulo 65536), not confirmed by disassembly. These exact bytes produced `update_record` on one camera; the format is not fully reverse engineered.

**Naming trap:** some V380 firmware looks for `localupdate.conf`. This payload uses `local_update.conf` with an underscore. Do not rename it.

## Likely execution path (not proven end to end)

1. The camera boots with a FAT32 card.
2. The update handler reads `local_update.conf`, and possibly `patch_reuse`.
3. It may check the patch name or MD5 and parse the model header.
4. It may write `update_record` and run the pre-update script.
5. On the tested camera `update_record` appeared; the script output did not.

So the supported claim is: **the local-update trigger made the camera write `update_record`, and the `last_id` inside was accepted by the app**. Not: "the script extracted the ID".

## Packaging and wording

- **WiFi Smart Net Camera** - generic box wording, not a model number.
- **Easy to achieve real-time remote viewing** - a marketing slogan.
- **4G Smart Camera** and **WiFi Smart Camera** - separate setup categories in the V380 Pro manual; one camera does not necessarily have both radios.
- A "V380" sticker says nothing about the board, firmware or updater inside.

Do not call this tool universal or official firmware.

## Why the first card experiment failed

`AutoTestFile/release/autotest_init.sh` came from other V380 firmware. A file on the card is not enough: the firmware needs a matching hook and permission to run it. The camera only recorded video into `RecFiles/`.

## Security limits

- This uses the update system, not a vendor export feature.
- A package without kernel images is not automatically safe: the updater can still rewrite metadata, flash or reboot.
- Never reuse IDs from other people's reports. Every number in the docs is fictional.
- The `V380E6_G1` header is not confirmed as this board's `Hwname`.
- Reading the ID does not fix 4G SIM detection or a dead Ethernet link.

## The embedded script

[`source/exshell_bfu.sh`](../source/exshell_bfu.sh) is the exact script inside the patch. It tries to read Linux settings and write `V380_ID_RESULT/00_RESULT.txt` to the card. That file never appeared. Copying the `.sh` to the card root does not run it.

## Reproducing the package

- `python tools/check_payload.py` - hashes, patch structure, release ZIP, plus a rebuild compared byte for byte.
- `python tools/rebuild_patch.py` - rebuilds the patch from `source/` and repacks `releases/microSD-files-only.zip`.

Both run locally, need only Python 3 and never touch a camera.
