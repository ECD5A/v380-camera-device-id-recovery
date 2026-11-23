<!--
  V380 / V380 Pro - Device ID recovery through microSD.
  Copyright (c) 2026 ECD5A
  Licensed under the MIT License.
  https://github.com/ECD5A/v380-camera-device-id-recovery
  SPDX-License-Identifier: MIT
-->

# Experiment log

**Date:** 2026-11-23. **Hardware:** one V380 Pro 4G/LTE camera. Identifying values are withheld on purpose. This is a retro log of one unit, not a multi-device test.

| Stage | Observation | Result |
| --- | --- | --- |
| Start | Pairing sticker with the unique QR missing. The QR on the box opens the app download. | Camera could not be added. |
| Identification | LTE module labelled **ZXInfoTek ZX800-VG**, other manufacturing markings on the board and holder. | LTE module known, board ID unknown. |
| Cellular | Camera announced a network connection, then reported no SIM. | Separate problem, not solved by this method. |
| Ethernet | Router link LED never came up, while router and cable worked with other devices. | No link, so LAN scanning was pointless. |
| First card try | `AutoTestFile/release/autotest_init.sh` on a FAT32 card. | Camera recorded AVI video; `v380-id-result.txt` never appeared. |
| Card snapshot | `RecFiles/record.ini` plus AVI and .idx files. | Confirms read/write only, not code execution. |
| Read-only dump | A separate shell script prepared to dump settings. | Never observed running; no dump recovered. |
| Local patch | The three files in [`sdcard/`](../sdcard/) on the card, camera booted with it. | `update_record` appeared. No `V380_ID_RESULT/00_RESULT.txt`. |
| App check | `last_id` read from `update_record`, typed into V380 Pro. | **Owner confirmed the number was accepted.** |

## What the camera wrote

```ini
[PATCH]
last_id=<redacted>
```

This file was **not** in the payload, and the number was **not** in the payload either. The ID came from the camera, not from the files. Which internal file supplied it is still unknown. Do not confuse this with `record.ini`, which belongs to the video recorder.

## What did not work

- The `AutoTestFile` startup script produced nothing.
- The Ethernet cable never linked up, so no network scan is reported.
- The camera still complained about the SIM. This project does not fix that.
- No UART access and no SPI flashing were needed or attempted.
- The full QR payload was never recovered. The numeric ID was enough for this app flow.

## Untested

- Firmware compatibility with other V380 and V380 Pro cameras.
- Real execution of `exshell_bfu.sh` instead of just updater bookkeeping.
- The exact SoC, bootloader and firmware version.
- How the handler validates `patch_reuse`, the inner checksum and the hardware ID.
- Whether other startup scripts or payload layouts work on this unit.
