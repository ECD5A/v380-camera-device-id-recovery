# Packaging terminology and search keywords

### Verified phrases found in public packaging listings

- **WiFi Smart Net Camera** — generic box/product descriptor, **not an exact model number**.
- **Easy to achieve real-time remote viewing** — promotional slogan for remote viewing. The camera specifications identify the supported connection types.
- **V380 / V380 Pro** — names associated with the camera app/software ecosystem, not a single board revision.
- **4G Smart Camera** and **WiFi Smart Camera** — categories in V380 Pro instructions; do not assume both radios exist in one camera.

### Sources

- [Retail packaging photos](https://www.ebay.com/itm/335940974885) show both packaging phrases.
- [V380 Pro product manual](https://device.report/m/d4a99834043f682937aa0cb2fa2eb3b707e76b95e6faa61410a1cf194f5efba5) lists separate Wi-Fi and 4G setup categories.
- [Macro-Video FAQ](https://macro-video.com/en/support/support-faq/support-faq/v380/record-replay-1/page/19) documents manual Device ID entry for 4G cameras.

### Suggested GitHub repository metadata

- **Repository:** `v380-camera-device-id-recovery`
- **Title:** V380 / V380 Pro IP Security Camera — Device ID Recovery via microSD
- **Description:** Recover a missing V380 Pro IP security camera Device ID from microSD `update_record`. One verified 4G/LTE case; experimental patch and RU/EN guide.
- **Topics:** `v380`, `v380-pro`, `ip-camera`, `security-camera`, `camera-recovery`, `device-id`, `microsd`, `4g-camera`, `reverse-engineering`

Do not label the tool **universal**, **works on all V380 Wi-Fi and 4G cameras**, or **official firmware**.
