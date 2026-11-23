# Troubleshooting / Проблемы и решения

## Nothing happens / Ничего не произошло

The update handler may not support this file layout, the card may not be FAT32, or the camera may have a different mainboard / firmware. **Stop; do not keep trying random packages or reset/flash the device.** A generic "V380" box label does not prove compatibility. If the camera is updating, **do not remove power**.

## `RecFiles/record.ini` and video are created, but no `update_record`

Normal recording has worked, but it does **not** demonstrate execution of update or autotest scripts. Verify the three-file root layout, including the **underscore** in `local_update.conf`. Do not mistake `record.ini` for `update_record`.

## `update_record` exists but no `last_id`

The format may differ by firmware. Please collect non-sensitive structure information only, **not** the full file in a public GitHub issue if it contains identifiers. Do not substitute someone else's ID.

## `patch_reuse` не пустой / содержит текст

Это ломает проверенный пакет: файл должен быть **0 байт**. Обычно так выходит, если открыть его в редакторе и сохранить. Скачайте [`releases/microSD-files-only.zip`](../releases/microSD-files-only.zip) заново и распакуйте без правок.

## `last_id` has 9 digits, not 8 / ID из 9 цифр, а не 8

Nine digits can be legitimate. In the observed case the numerical value in `last_id` was accepted by V380 Pro. Validate the **complete** number through your own app; do not arbitrarily remove digits.

## App accepts ID, camera still offline

Pairing identity and network connection are separate. A 4G camera saying it cannot detect the SIM still needs its own SIM/network issue resolved. Likewise, a router's Ethernet link light not turning on is a physical-layer problem; an IP scan cannot solve that.

## `V380_ID_RESULT/00_RESULT.txt` is missing

This is expected in the one successful experiment: the local-update bookkeeping created `update_record`, but there was no demonstrated execution of the embedded script. **Do not tell people they have obtained a complete diagnostic dump.**

## Is the box QR the same as pairing QR?

Not necessarily. Some box QR codes lead to an app download page. A device pairing QR may encode a numeric ID and other fields. Do not fabricate a "factory" QR from a guessed format; use manual ID entry if the app allows it.

## Will this work on Wi-Fi models?

**Unknown.** Official manuals explicitly distinguish *WiFi Smart Camera* and *4G Smart Camera*. The phrase *WiFi Smart Net Camera* on the carton is not proof of the underlying radio hardware or firmware.

## Can I share the complete `update_record`?

Prefer not. The `last_id` can be a unique identifier for your security camera. Mask the value as `last_id=<redacted>` before reporting a test result.
