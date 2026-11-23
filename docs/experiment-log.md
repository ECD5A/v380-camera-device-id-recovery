# Experiment log / Журнал экспериментов

**Observed on:** 2026-11-23, one V380 Pro **4G/LTE security camera**. Identifying values have been deliberately withheld. This is a retrospective log, **not** a claim of multi-device validation.

| Stage | Observation | Result |
| --- | --- | --- |
| Initial setup | Camera pairing label / unique QR absent. Box QR opens app download. | Could not initially add the camera. |
| Identification | LTE module labelled **ZXInfoTek ZX800-VG**; other board/holder manufacturing markings present. | LTE model identified; mainboard hardware ID remained unknown. |
| Mobile networking | Camera spoke about cellular-network connection but then reported no SIM detected. | Network connectivity problem remained independent of ID recovery. |
| Wired networking | Router Ethernet link LED did not indicate a connection with camera, although router/cable worked with other devices. | No Ethernet link, so UDP/LAN scanner could not be used. |
| First microSD trial | `AutoTestFile/release/autotest_init.sh` copied to FAT32 card. | Camera recorded AVI video; `v380-id-result.txt` not created. Autotest execution **not demonstrated**. |
| Follow-up card snapshot | `RecFiles/record.ini` and AVI/.idx files appeared. | Confirmed SD read/write only, **not** remote access or script execution. |
| Read-only dump concept | A separate shell script was prepared to read settings. | **Never confirmed to execute** on camera; no dump file recovered. |
| Local patch experiment | Three-file update package, exactly as shipped in `sdcard/`, on card; camera booted with it. | New **`update_record`** appeared. No `V380_ID_RESULT/00_RESULT.txt`. |
| App verification | The value read from `update_record` as `last_id` was entered in V380 Pro. | **User confirmed that the number was accepted.** |

## What the camera actually wrote

```ini
[PATCH]
last_id=<redacted device-specific digits>
```

This file **was not included in the original SD payload**, and the final number was **not present in the payload**. That is stronger evidence that the ID originated from the camera/update process rather than being hardcoded. It does not prove which internal file supplied it. Do not conflate this with `record.ini` from the AVI recorder.

## What did **not** work

- The first `AutoTestFile` startup-script probe did not create its expected result.
- The Ethernet cable did not establish a physical link to the router. No successful network scan is reported.
- The camera was still reporting a SIM-card detection problem; this project is **not** a solution for the cellular-network fault.
- Neither UART reading nor SPI Flash programming was performed or shown necessary.
- No complete QR payload was recovered; numeric Device ID was sufficient in the observed app flow.

## Untested assumptions

- Firmware compatibility across other V380/Pro cameras.
- A genuinely functioning `exshell_bfu.sh` script execution (rather than only the updater's bookkeeping).
- Identification of exact mainboard SoC, bootloader and firmware version.
- How update handler validates `patch_reuse`, inner checksum and hardware identifier.
- Whether additional startup scripts or other patch layouts work on this model.

## Release integrity

The file `updatepatch/288032472d4d508105188fadf5a3ae8e.patch` in the successful SD snapshot matched the previously prepared package **byte for byte**; this repository preserves it unmodified. See `MANIFEST.md` for checksums.
