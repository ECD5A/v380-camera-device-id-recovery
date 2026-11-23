# V380 / V380 Pro — IP Camera Device ID Recovery

[Русский](README.md) · **English**

[![MIT License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)
[![Tested on one 4G/LTE camera](https://img.shields.io/badge/4G_LTE-1%20camera-2E7D32)](docs/experiment.md#english-summary)

If a V380 camera has lost its pairing QR sticker, its Device ID can be read from the `last_id` field in an existing `update_record` file on the microSD card. Use the number to add the camera to V380 Pro manually.

[Download ZIP](https://github.com/ECD5A/v380-camera-device-id-recovery/archive/refs/heads/main.zip) · [Quick start](#quick-start) · [Test results](docs/experiment.md#english-summary) · [Troubleshooting](#troubleshooting)

[![V380 retail box with an illustration of a dual-lens camera and the WiFi Smart Net Camera label](docs/v380-camera-box.jpg)](docs/v380-camera-box.jpg)

*Box from the tested 4G/LTE camera, labelled “WiFi Smart Net Camera.” See the [test notes](docs/experiment.md#english-summary) for the device details.*

## Quick start

1. Open the microSD card on a computer. Look for a file named `update_record` with no extension in the root folder.
2. Extract the [project ZIP](https://github.com/ECD5A/v380-camera-device-id-recovery/archive/refs/heads/main.zip) and open a terminal in the extracted folder. With Python 3 installed, run the [reader](read_update_record.py) with the path to the file.

   **Windows** (card mounted as `E:`)

   ```powershell
   python read_update_record.py "E:\update_record"
   ```

   **Linux or macOS**

   ```sh
   python3 read_update_record.py "/path/to/card/update_record"
   ```

3. In V380 Pro, tap **+**, select **Enter manually**, and enter the recovered number. Menu labels can vary by app version. [Macro-Video FAQ](https://macro-video.com/en/support/support-faq/support-faq/v380/record-replay-1/page/19)

Without Python, open `update_record` in a text editor and look for the value after `last_id=`. The reader runs locally and prints the number in the terminal.

## Test result

In one test with a 4G/LTE camera using a **ZXInfoTek ZX800-VG** module, V380 Pro accepted the recovered ID. The camera connected and worked. Compatibility with other models and firmware versions remains untested. [Test notes](docs/experiment.md#english-summary)

## Troubleshooting

| Situation | What to check |
| --- | --- |
| The card has no `update_record` | This method requires an existing record. For a camera already added to V380 Pro, check the device list. The number may also be on the camera's label. [Where to find the Device ID](https://macro-video.com/en/support/support-faq/support-faq/v380/record-replay-1/page/7) |
| The reader finds no `last_id` | Check that you opened `update_record` from the card root and that the field contains a number. |
| V380 Pro accepts the ID but the camera stays offline | For a 4G camera, check the SIM status, data allowance, and reception. [4G camera connection](https://macro-video.com/en/support/support-faq/support-faq/v380/record-replay-1/page/19) |
| The QR code on the box opens the app download page | Packaging and manuals can include separate codes for downloading the app and for pairing. [V380 Pro manual](https://device.report/m/d4a99834043f682937aa0cb2fa2eb3b707e76b95e6faa61410a1cf194f5efba5) |

If you report a result, include the connection type, the camera model if known, and whether the app accepted the ID. Remove Device IDs, QR codes, IMEIs, and serial numbers from images and logs.

[MIT License](LICENSE)
