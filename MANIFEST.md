# Manifest: hashes and evidence level

## Scope

- Project: **V380 / V380 Pro: Device ID recovery**
- Case study: **2026-11-23**
- Test and research: [ECD5A](https://github.com/ECD5A)
- App: **V380 Pro**
- Working camera: **4G/LTE**, LTE module **ZXInfoTek ZX800-VG**
- Mainboard SoC and real `Hwname`: **unknown**
- Patch header: **`V380E6_G1`** (not verified as the board identity)
- Result: `update_record` created, `last_id` accepted by the app, camera connected
- Shell diagnostic dump: **not observed**
- Other devices tested: **none**

## SD payload (byte-identical to the successful attempt)

| Path | Size | SHA-256 |
| --- | ---: | --- |
| `sdcard/local_update.conf` | 50 | `4d0443f75449d080eb967a80320087f254acf0927ad973998f8f1b9a441d7295` |
| `sdcard/patch_reuse` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `sdcard/updatepatch/288032472d4d508105188fadf5a3ae8e.patch` | 1596 | `ba254a416b540e841860220e2edfa0061113147d40c3bcdf9a5e4e6317e91ca2` |

Patch MD5: `288032472d4d508105188fadf5a3ae8e`

## Release archive

| File | Size | SHA-256 |
| --- | ---: | --- |
| `releases/microSD-files-only.zip` | 1215 | `53c29d2c678efc5f74e814bb8743c7f853bd50b90c88f630c0831ef007b0c18d` |

The archive holds the three files above and nothing else. Same bytes are attached to the GitHub release.

Reproducible: `python tools/rebuild_patch.py` writes fixed timestamps, and `python tools/check_payload.py` fails if the hashes, the ZIP or the rebuilt patch stop matching `sdcard/` and `source/`. CI runs the same check on every push.

## Audit notes

The patch is byte-identical to the one recovered from the successful card snapshot. The camera-generated `update_record` was **not** bundled with the files. The embedded script attempts a read-only settings export; its execution was never observed.

## No personal identifiers

The repository does not include the real `last_id`, IMEI, original card images or video, serial or QR data, the owner's email, or an unredacted dump. Examples use made-up digits.

## Licensing

Helper scripts, the documented script and all text are MIT. The `.patch` is a small generated experimental package, not a firmware image.
