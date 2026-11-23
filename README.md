# V380 / V380 Pro — восстановление Device ID IP-камеры

**Русский** · [English](README.en.md)

[![Лицензия MIT](https://img.shields.io/badge/License-MIT-blue)](LICENSE)
[![Проверено на одной 4G/LTE-камере](https://img.shields.io/badge/4G_LTE-1%20%D0%BA%D0%B0%D0%BC%D0%B5%D1%80%D0%B0-2E7D32)](docs/experiment.md)

Если наклейка с QR-кодом потеряна, Device ID можно прочитать из поля `last_id` в существующем файле `update_record` на microSD. Затем этот номер можно ввести в V380 Pro вручную.

[Скачать ZIP](https://github.com/ECD5A/v380-camera-device-id-recovery/archive/refs/heads/main.zip) · [Быстрый старт](#быстрый-старт) · [Результат испытания](docs/experiment.md) · [Частые проблемы](#частые-проблемы)

[![Упаковка V380 с изображением двухобъективной камеры и надписью WiFi Smart Net Camera](docs/v380-camera-box.jpg)](docs/v380-camera-box.jpg)

*Упаковка 4G/LTE-камеры из испытания с маркировкой «WiFi Smart Net Camera».*

## Быстрый старт

1. Откройте карту microSD на компьютере. В её корне найдите файл `update_record` без расширения.
2. Распакуйте [ZIP проекта](https://github.com/ECD5A/v380-camera-device-id-recovery/archive/refs/heads/main.zip) и откройте терминал в распакованной папке. Если установлен Python 3, запустите [утилиту](read_update_record.py) с путём к файлу.

   **Windows** (карта подключена как `E:`)

   ```powershell
   python read_update_record.py "E:\update_record"
   ```

   **Linux или macOS**

   ```sh
   python3 read_update_record.py "/путь/к/microSD/update_record"
   ```

3. В V380 Pro нажмите **+**, выберите **Ввести вручную** (*Enter manually*) и укажите полученный номер. Название пункта может отличаться в вашей версии приложения. [FAQ Macro-Video](https://macro-video.com/en/support/support-faq/support-faq/v380/record-replay-1/page/19)

Без Python откройте `update_record` в текстовом редакторе и найдите значение после `last_id=`. Утилита работает локально и выводит номер в терминал.

## Что получилось

В испытании на одной 4G/LTE-камере с модулем **ZXInfoTek ZX800-VG** приложение приняло восстановленный номер. Камера подключилась и заработала. Совместимость с другими моделями и версиями прошивки пока не проверялась. [Подробности испытания](docs/experiment.md)

## Частые проблемы

| Ситуация | Что проверить |
| --- | --- |
| На карте нет `update_record` | Для этого способа нужен уже записанный файл. Device ID также бывает виден в списке устройств V380 Pro, если камера раньше была добавлена, или на наклейке корпуса. [Где посмотреть ID](https://macro-video.com/en/support/support-faq/support-faq/v380/record-replay-1/page/7) |
| В файле не найден `last_id` | Проверьте, что открыт `update_record` из корня карты и в поле записано число. |
| Приложение приняло ID, а камера офлайн | У 4G-камеры проверьте статус SIM-карты, остаток трафика и уровень сигнала. [Подключение 4G-камеры](https://macro-video.com/en/support/support-faq/support-faq/v380/record-replay-1/page/19) |
| QR-код на коробке открывает страницу приложения | В комплекте могут быть отдельные коды для установки приложения и добавления камеры. [Руководство V380 Pro](https://device.report/m/d4a99834043f682937aa0cb2fa2eb3b707e76b95e6faa61410a1cf194f5efba5) |

При сообщении о результате укажите тип подключения, модель камеры, если она известна, и приняло ли приложение ID. Уберите из снимков и логов сам Device ID, QR-коды, IMEI и серийные номера.

[Лицензия MIT](LICENSE)
