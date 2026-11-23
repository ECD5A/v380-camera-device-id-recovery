# Troubleshooting

## Nothing happens

The updater may not support this layout, the card may not be FAT32, or the board is different. **Stop. Do not try random packages, do not reset or flash the camera.** A "V380" sticker proves nothing. If the camera is updating, do not cut power.

## Only `RecFiles/record.ini` and video, no `update_record`

Recording works, but that says nothing about the updater running. Check the three-file root layout and the **underscore** in `local_update.conf`. `record.ini` is not `update_record`.

## `update_record` exists, but there is no `last_id`

Format may differ per firmware. Share the structure, not the whole file, if it holds identifiers. Never paste someone else's ID.

## `patch_reuse` is not empty

That breaks the tested package: the file must be **0 bytes**. Usually it happens when the file is opened in an editor and saved. Download [`releases/microSD-files-only.zip`](../releases/microSD-files-only.zip) again and unpack it without edits.

## The ID has 9 digits, not 8

Nine can be valid. The observed value was accepted by V380 Pro as is. Try the **whole** number in your own app instead of trimming digits.

## The app accepts the ID, the camera stays offline

Pairing and networking are different things. A 4G camera that cannot see its SIM still needs the SIM problem solved. A router port LED that never lights up is a physical-layer problem; scanning the LAN will not help.

## `V380_ID_RESULT/00_RESULT.txt` is missing

Expected in the one successful run: the updater wrote `update_record`, the embedded script never visibly executed. Nobody got a diagnostic dump from this package.

## Is the QR on the box the pairing QR?

Not always. Many box codes just open the app download page. A pairing QR may encode the ID plus other fields. Do not invent a "factory" QR; type the ID manually when the app allows it.

## Will it work on Wi-Fi models?

**Unknown.** The manual lists *WiFi Smart Camera* and *4G Smart Camera* separately, and a box saying *WiFi Smart Net Camera* tells you nothing about the radio or firmware.

## Can I share the whole `update_record`?

Better not: `last_id` identifies your camera. Replace the value with `last_id=<redacted>` before reporting.
