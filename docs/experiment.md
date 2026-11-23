# Результаты испытания V380 Pro на 4G/LTE

[Русский README](../README.md) · [English summary](#english-summary)

Испытание провёл [ECD5A](https://github.com/ECD5A).

## Устройство

| Параметр | Наблюдение |
| --- | --- |
| Дата испытания | 23 ноября 2026 года |
| Камера | Один экземпляр 4G/LTE IP-камеры, подключённой через V380 Pro |
| Маркировка LTE-модуля | **ZXInfoTek ZX800-VG** |
| Основная плата и версия прошивки | Точная модель и версия неизвестны |
| Упаковка | «WiFi Smart Net Camera», «Easy to achieve real-time remote viewing». [Фото коробки](v380-camera-box.jpg) |

## Наблюдения

| Этап | Результат |
| --- | --- |
| Запуск камеры в ходе испытания с локальным обновлением | Примерно через две минуты на microSD был обнаружен `update_record` с числовым полем `last_id`. |
| Ручной ввод | Приложение V380 Pro приняло значение из `last_id`. Камера подключилась и заработала. |
| Отдельный диагностический вывод | Ожидаемый файл с отдельной диагностикой на карте не появился. |

Пример структуры обнаруженной записи содержит вымышленный номер.

```ini
[PATCH]
last_id=123456789
```

Результат относится к этому экземпляру камеры. Одинаковая упаковка может использоваться для разных устройств. В руководстве V380 Pro Wi-Fi и 4G описаны как отдельные варианты подключения. [Руководство V380 Pro](https://device.report/m/d4a99834043f682937aa0cb2fa2eb3b707e76b95e6faa61410a1cf194f5efba5)

## Как работает утилита

[`read_update_record.py`](../read_update_record.py) принимает путь к файлу или к папке с `update_record`. Он читает файл средствами стандартной библиотеки Python 3 и выводит найденный числовой `last_id`.

| Код завершения | Что произошло |
| --- | --- |
| `0` | Найден числовой `last_id`. |
| `1` | Читаемый файл найден, подходящего значения `last_id` в нём нет. |
| `2` | Файл не удалось открыть или аргументы команды некорректны. |

## English summary

[ECD5A](https://github.com/ECD5A) tested one 4G/LTE camera with a **ZXInfoTek ZX800-VG** module on November 23, 2026. During a local update test, an `update_record` file with a numeric `last_id` was found on the microSD card about two minutes after powering on the camera. V380 Pro accepted that number, and the camera connected and worked. The expected separate diagnostic output file did not appear. The mainboard model and firmware version remain unknown.

The [reader](../read_update_record.py) accepts the file path or its containing directory. It returns `0` when an ID is found, `1` when the file has no matching ID, and `2` when the file cannot be read or the command line is invalid. [English instructions](../README.en.md)
