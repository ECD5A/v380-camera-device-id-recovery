# V380 / V380 Pro — восстановление Device ID камеры

[Русский](#русский) · [English](#english) · [![MIT](https://img.shields.io/badge/License-MIT-blue)](LICENSE)

## Русский

Скрипт читает `last_id` из существующего файла `update_record` на microSD IP-камеры V380 и выводит Device ID. Номер позволяет добавить камеру в V380 Pro, если потеряна наклейка с QR-кодом. Проверено на одной 4G/LTE-камере.

### Запуск

Нужен Python 3. Запустите из папки репозитория, указав путь к файлу на microSD.

```console
python read_update_record.py "E:\update_record"
```

Замените `E:` на букву вашей карты. В V380 Pro нажмите **+ → Ввести вручную** и укажите найденный Device ID. [FAQ Macro-Video](https://macro-video.com/en/support/support-faq/support-faq/v380/record-replay-1/page/19)

## English

Read the Device ID of a V380 / V380 Pro IP security camera from `last_id` in an existing microSD `update_record` file. This helps when the pairing QR code is missing. Tested on one 4G/LTE camera.

Run the [command above](#запуск) with Python 3 and the path to your `update_record` file. In V380 Pro, tap **+ → Enter manually** and enter the ID.
