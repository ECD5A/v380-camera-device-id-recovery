# Release manifest and evidence level

## Release scope

- Project: **V380 / V380 Pro IP Security Camera — Device ID Recovery**
- Initial case study: **2026-11-23**
- Research and camera test: [ECD5A](https://github.com/ECD5A)
- App: **V380 Pro**
- Camera connectivity in successful case: **4G/LTE**
- LTE module label: **ZXInfoTek ZX800-VG**
- Mainboard SoC / full `Hwname`: **unknown**
- Payload header string: **`V380E6_G1`** (not verified as tested mainboard identity)
- Success reported: **`update_record` created, `last_id` accepted by the app, camera connected and worked**
- Shell diagnostic dump: **not observed**
- Additional devices tested: **none confirmed**

## SD payload files (exact bytes, unchanged from successful attempt)

| Path | Size | SHA-256 |
| --- | ---: | --- |
| `sdcard/local_update.conf` | 50 | `4d0443f75449d080eb967a80320087f254acf0927ad973998f8f1b9a441d7295` |
| `sdcard/patch_reuse` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `sdcard/updatepatch/288032472d4d508105188fadf5a3ae8e.patch` | 1596 | `ba254a416b540e841860220e2edfa0061113147d40c3bcdf9a5e4e6317e91ca2` |

Patch MD5: `288032472d4d508105188fadf5a3ae8e`

## Downloadable archive

`releases/microSD-files-only.zip` holds exactly the three files above and nothing else, so nobody has to browse the repository to build a card. The same archive is attached to the GitHub release.

| File | Size | SHA-256 |
| --- | ---: | --- |
| `releases/microSD-files-only.zip` | 1215 | `53c29d2c678efc5f74e814bb8743c7f853bd50b90c88f630c0831ef007b0c18d` |

The archive is reproducible: `python tools/rebuild_patch.py` packs fixed timestamps, `python tools/verify_payload.py` fails if the ZIP stops matching `sdcard/`, and CI runs both checks on every push.

**Audit:** the patch is byte-identical to the patch recovered from the successful SD card's archive; the observed camera-generated `update_record` was **not bundled** with the files. An embedded script attempts a read-only configuration export, but its execution was not established.

## Provenance / no personal identifiers

The public repository deliberately **does not include** the camera's actual `last_id`, IMEI, original SD-card images/video, manufacturing serial/QR data, the owner’s private email, or an unredacted diagnostic dump. Public examples use made-up digits.

## Independent tools and licensing

The helper Python code, the documented experimental script, and documentation in this repository are provided under MIT. Linked third-party resources are used for explanation and are **not** copied or relicensed here. The binary `.patch` is a generated experimental package, **not a complete commercial firmware image**.
