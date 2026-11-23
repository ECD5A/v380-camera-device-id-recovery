# V380 / V380 Pro IP Security Camera — Device ID Recovery

[Русский](README.md) · **English**

[![MIT License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)
[![Tested on one 4G/LTE camera](https://img.shields.io/badge/4G_LTE-1%20camera-2E7D32)](MANIFEST.md)
[![Payload check](https://github.com/ECD5A/v380-camera-device-id-recovery/actions/workflows/verify.yml/badge.svg)](https://github.com/ECD5A/v380-camera-device-id-recovery/actions/workflows/verify.yml)

Recover the **Device ID of a V380 / V380 Pro IP security camera** using a microSD card when the pairing QR sticker is missing or damaged. V380 Pro accepts manual Device ID entry. The QR code on the box may lead to the app download page.

[Instructions](#instructions) · [Download the 3 files](releases/microSD-files-only.zip) · [Troubleshooting](docs/troubleshooting.md) · [Experiment log](docs/experiment-log.md) · [Technical notes](docs/technical-notes.md) · [Support](#support)

## Quick start

1. Download [`microSD-files-only.zip`](releases/microSD-files-only.zip) and extract it **into the card root** (FAT32). There is no wrapper folder: the card must contain exactly `local_update.conf`, `patch_reuse` and the `updatepatch/` folder.
2. Power the camera off, insert the card, power it on. Do not press Reset, and never cut power while the camera announces an update.
3. After about 3 minutes power the camera off, take the card out and open `update_record` in Notepad. The `last_id=` line is the Device ID.
4. In V380 Pro tap **+** → **Enter manually** and type the number.

No `update_record`? Then your firmware does not process this package — stop experimenting on that camera.

## Test results

| Item | Observation |
| --- | --- |
| Camera | One 4G/LTE IP camera with a **ZXInfoTek ZX800-VG** module. The mainboard model and processor are unknown. |
| ID recovery | The camera wrote `last_id` to `update_record` on the microSD card. V380 Pro accepted the number when entered manually. The owner confirmed that the camera connected and worked. |
| Diagnostic script | `V380_ID_RESULT/00_RESULT.txt` did not appear. Script execution remains unconfirmed. |

Compatibility with other 4G/LTE, Wi-Fi and Ethernet cameras remains unverified. `V380E6_G1` appears in the patch header. The camera's actual `Hwname` is unknown. [Manifest](MANIFEST.md)

![Front of the V380 box showing a dual-lens camera and the WiFi Smart Net Camera label](docs/images/v380-camera-box.jpg)

*Box from the tested camera. Photo by ECD5A.*

The box reads **“WiFi Smart Net Camera”** and **“Easy to achieve real-time remote viewing.”** The V380 Pro manual lists **WiFi Smart Camera** and **4G Smart Camera** as separate setup categories. [Packaging and terminology](docs/keywords-and-packaging.md)

> [!WARNING]
> The camera processes this package through its firmware updater. On incompatible hardware, it can change internal state, cause the camera to hang, or damage the firmware. Use it only on a camera you own and at your own risk.

## Instructions

1. Back up files already on the microSD; format it **FAT32** if needed. The ready-made three-file set is in [`releases/microSD-files-only.zip`](releases/microSD-files-only.zip).
2. Copy **only** the contents of [`sdcard/`](sdcard/) to the microSD **root**:

   ```text
   microSD/
   ├── local_update.conf
   ├── patch_reuse                 # intentionally empty
   └── updatepatch/
       └── 288032472d4d508105188fadf5a3ae8e.patch
   ```

3. **Power off** the camera, insert the card, and power it back on. **Do not press Reset**.
4. Allow the camera to boot for approximately **3 minutes**. **If a firmware-update message is announced, never interrupt power while it is updating**; let it finish completely.
5. Power off normally once the camera is back to normal operation (or after a quiet boot with no update activity), remove the card and check it on a computer.
6. Look for an **exactly named** file `update_record` (no extension) at the root. A successful observed example looked like this, with **fictional digits**:

   ```ini
   [PATCH]
   last_id=123456789
   ```

7. If the number is present, tap **+** in V380 Pro and select **Enter manually** to enter the Device ID. Menu labels can vary by app version.
8. Remove the update files from the card after the experiment to avoid repeated processing. Preserve a backup for your records.

If you only see `RecFiles/record.ini`, or if the app accepts the ID and the camera stays offline, see [troubleshooting](docs/troubleshooting.md).

### Reading the resulting file

`update_record` is a plain text file: open it in Notepad, Notepad++ or TextEdit and look at the `last_id=` line. Nothing has to be installed. Do not rename the file, and never paste the value into a public issue — it identifies your camera.

## Files and folders

```text
.
├── README.md / README.en.md      # Russian / English instructions
├── sdcard/                       # ONLY these 3 operational files go on the card
├── source/exshell_bfu.sh         # Embedded script source (for audit, NOT for card root)
├── tools/                        # Offline payload check and deterministic rebuild
├── docs/                         # Experiment history, technical notes, FAQ
├── MANIFEST.md                   # Checksums and verification status
└── LICENSE                       # MIT license for the repository's original text and code
```

### How the process appears to work

A compatible camera's boot/update service checks the card for a local patch. It may read `local_update.conf`, load `updatepatch/<md5>.patch`, and write its own `update_record`. In the observed test, `last_id` became available and matched the app-accepted camera ID. **The precise internal path used to generate `last_id` has not been independently demonstrated on this mainboard**. Details and format references are in [technical notes](docs/technical-notes.md).

## Verify the payload before you use it

These commands run on your computer only; they never access the camera.

```bash
python tools/verify_payload.py   # SHA-256 of the three files, patch MD5, header, embedded script
python tools/test_tools.py       # offline rebuild compared with releases/microSD-files-only.zip
```

`patch_reuse` must stay a **0-byte file**. If an editor or archiver adds text to it, the payload no longer matches the verified bytes — download the ZIP again.

## Public reports / privacy

If you test on your own equipment, share **only** redacted: connection type (4G/Wi-Fi/Ethernet), main board model if known, app version, whether `update_record` appeared, and whether the app accepted the ID. **Do not publish your ID, QR pairing payload, IMEI, serial numbers, SIM identifiers, MAC address, Wi-Fi credentials, photos of private scenes, or raw config dumps**.

## Support

The project is free and maintained in spare time. If this guide helped you bring a camera back online and you want to support further experiments:

- TON: `pointoncurve.ton`
- Bitcoin (BTC): `1ECDSA1b4d5TcZHtqNpcxmY8pBH1GgHntN`
- USDT (TRC20): `TUF4vPdB6QkjCvZq18rBL4Qj4dK5ihCN75`

Donations do not change what gets published: results stay as they are, including failures. The only authoritative source for these addresses is this file in the main repository; forks and copies may contain substituted ones.

## Contact

Questions about recovery, reports for other models and pull requests:

<p>
  <a href="mailto:stelmak159@gmail.com" aria-label="Email"><img alt="Email" height="24" src="https://cdn.simpleicons.org/gmail/EA4335"></a>
  &nbsp;
  <a href="https://t.me/ECDS4" aria-label="Telegram"><img alt="Telegram" height="24" src="https://cdn.simpleicons.org/telegram/26A5E4"></a>
  &nbsp;
  <a href="https://github.com/ECD5A/v380-camera-device-id-recovery" aria-label="GitHub repository"><picture><source media="(prefers-color-scheme: dark)" srcset="https://cdn.simpleicons.org/github/FFFFFF"><img alt="GitHub repository" height="24" src="https://cdn.simpleicons.org/github/181717"></picture></a>
</p>

Keep personal data out of reports: no Device ID, IMEI, serial numbers, MAC address or recordings. Camera model, connection type and app version are enough.

**Unofficial community project.** Not affiliated with or endorsed by V380, V380 Pro, Macro-Video or camera manufacturers. It does not contain proprietary firmware images. Project materials are under the [MIT License](LICENSE).
