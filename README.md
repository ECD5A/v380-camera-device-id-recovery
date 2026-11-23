# V380 / V380 Pro: восстановление Device ID камеры

**Русский** · [English](README.en.md)

```text
/*
 * V380 / V380 Pro - Device ID recovery through microSD.
 * Copyright (c) 2026 ECD5A
 * Licensed under the MIT License.
 * https://github.com/ECD5A/v380-camera-device-id-recovery
 * SPDX-License-Identifier: MIT
 */
```

[![Лицензия MIT](https://img.shields.io/badge/%D0%9B%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D1%8F-MIT-blue)](LICENSE)
[![Проверено на одной 4G/LTE-камере](https://img.shields.io/badge/4G_LTE-1%20%D0%BA%D0%B0%D0%BC%D0%B5%D1%80%D0%B0-2E7D32)](MANIFEST.md)
[![Проверка пакета](https://github.com/ECD5A/v380-camera-device-id-recovery/actions/workflows/verify.yml/badge.svg)](https://github.com/ECD5A/v380-camera-device-id-recovery/actions/workflows/verify.yml)

Наклейка с QR потерялась, и камеру нечем привязать к приложению. Тут описан способ вытащить **Device ID** камеры **V380 / V380 Pro** через microSD: камера сама запишет ID в файл на карте, останется ввести его в V380 Pro вручную. QR с коробки часто ведёт не на привязку, а на скачивание приложения.

[Коротко](#коротко) · [Скачать 3 файла](releases/microSD-files-only.zip) · [Проблемы](docs/troubleshooting.md) · [Журнал](docs/experiment-log.md) · [Как устроено](docs/technical-notes.md) · [Поддержать](#поддержка)

## Коротко

1. Скачайте [`microSD-files-only.zip`](releases/microSD-files-only.zip) и распакуйте **в корень** карты (FAT32). Вложенной папки внутри нет: на карте должно быть ровно `local_update.conf`, `patch_reuse` и папка `updatepatch/`.
2. Выключите камеру, вставьте карту, включите. Reset не нажимайте. Если камера сказала про обновление, питание не выдёргивайте.
3. Минут через 3 выключите камеру, достаньте карту и откройте `update_record` в Блокноте. Строка `last_id=` и есть Device ID.
4. В V380 Pro: **+** → **Ввести вручную** → номер.

Нет `update_record`? Значит ваша прошивка этот пакет не обрабатывает. Дальше мучить камеру смысла нет.

## Что проверено

| Параметр | Наблюдение |
| --- | --- |
| Камера | Одна IP-камера 4G/LTE, модуль **ZXInfoTek ZX800-VG**. Плата и процессор неизвестны. |
| Восстановление | Камера записала `last_id` в `update_record`. V380 Pro принял номер при ручном вводе, владелец подтвердил: камера подключилась и работает. |
| Диагностика | `V380_ID_RESULT/00_RESULT.txt` не появился. Выполнение встроенного скрипта не подтверждено. |

Другие 4G/LTE, Wi-Fi и Ethernet-камеры не проверялись. `V380E6_G1` стоит в заголовке патча, но это не подтверждённый `Hwname`. Хеши и происхождение файлов: [MANIFEST.md](MANIFEST.md).

![Коробка V380: двухобъективная камера и надпись WiFi Smart Net Camera](docs/images/v380-camera-box.jpg)

*Коробка из эксперимента. Фото ECD5A.*

На коробке написано **«WiFi Smart Net Camera»** и **«Easy to achieve real-time remote viewing»**. В инструкции V380 Pro **WiFi Smart Camera** и **4G Smart Camera** идут отдельными пунктами. [Маркировка и терминология](docs/technical-notes.md#packaging-and-wording)

> [!WARNING]
> Пакет идёт через штатный апдейтер прошивки. На неподходящей камере он может переписать служебные данные, подвесить её или убить прошивку. Только своя камера и свой риск.

## Инструкция

1. Скопируйте нужные видео с карты на компьютер. При необходимости отформатируйте карту в **FAT32**. Готовый набор: [`releases/microSD-files-only.zip`](releases/microSD-files-only.zip).
2. В **корень** карты положите **только** содержимое [`sdcard/`](sdcard/):

   ```text
   microSD/
   ├── local_update.conf
   ├── patch_reuse             # пустой файл, так и надо
   └── updatepatch/
       └── 288032472d4d508105188fadf5a3ae8e.patch
   ```

3. Выключите камеру из питания, вставьте карту, включите. **Reset не нажимайте**.
4. Подождите около **3 минут**. Если камера объявила обновление, **питание не отключайте**, пока оно не закончится.
5. После нормальной загрузки (или тихого включения без обновления) выключите камеру, достаньте карту и откройте её на ПК.
6. Ищите файл **`update_record`** без расширения в **корне карты**. Пример с **вымышленным** номером:

   ```ini
   [PATCH]
   last_id=123456789
   ```

7. Если строка есть, жмите **+** в V380 Pro, выбирайте **Ввести вручную** и вводите номер. Названия пунктов зависят от версии приложения.
8. После проверки удалите с карты файлы обновления, чтобы апдейтер не запускался снова. Копию оставьте себе.

Появился только `RecFiles/record.ini`, или ID приняли, а камера офлайн? Смотрите [типовые проблемы](docs/troubleshooting.md).

`update_record` - обычный текстовый файл. Откройте Блокнотом (Notepad, Notepad++, TextEdit) и найдите `last_id=`. Ничего устанавливать не нужно. Не переименовывайте файл и не выкладывайте значение: это идентификатор вашей камеры.

## Что в репозитории

- [`sdcard/`](sdcard/) - **только 3 файла для карты**, без документации.
- [`source/exshell_bfu.sh`](source/exshell_bfu.sh) - исходник скрипта из патча; отдельно на карту **не копировать**.
- [`tools/`](tools/) - офлайн-проверка и пересборка пакета. Python 3, сеть не нужна.
- [`docs/experiment-log.md`](docs/experiment-log.md) - что пробовали, что сработало, что нет.
- [`docs/troubleshooting.md`](docs/troubleshooting.md) - типовые ситуации.
- [`docs/technical-notes.md`](docs/technical-notes.md) - как устроен пакет и где кончаются доказательства.
- [`MANIFEST.md`](MANIFEST.md) - хеши, происхождение, статус проверки.

## Проверка пакета

Одна команда, камера не нужна:

```bash
python tools/check_payload.py
```

Скрипт сверяет SHA-256 трёх файлов, MD5 и заголовок патча, содержимое `releases/microSD-files-only.zip`, потом заново собирает патч из `source/` и сравнивает байт в байт. Любое расхождение - ошибка и ненулевой код возврата.

`patch_reuse` должен остаться пустым (**0 байт**). Если редактор дописал туда текст, пакет уже не тот: скачайте ZIP заново.

## Конфиденциальность

**Не выкладывайте** реальный Device ID, IMEI, серийник, содержимое QR, данные SIM, MAC, пароль Wi-Fi и личные видео. Для отчёта хватает типа камеры, ревизии платы (если видели), версии приложения и факта, появился ли `update_record`.

## Статус проекта

**Неофициальный проект.** Никак не связан с V380, V380 Pro и Macro-Video. Образов прошивки здесь нет. Код и тексты - [MIT](LICENSE).

## Поддержка

Если репозиторий сэкономил время:

- TON: `pointoncurve.ton`
- Bitcoin (BTC): `1ECDSA1b4d5TcZHtqNpcxmY8pBH1GgHntN`
- USDT (TRC20): `TUF4vPdB6QkjCvZq18rBL4Qj4dK5ihCN75`

На содержание это не влияет: тесты публикую как есть, включая провалы. Актуальные адреса только здесь, в форках их могут подменить.

## Связь

Вопросы, отчёты по другим моделям, правки:

<p>
  <a href="mailto:stelmak159@gmail.com" aria-label="Email"><img alt="Email" height="24" src="https://cdn.simpleicons.org/gmail/EA4335"></a>
  &nbsp;
  <a href="https://t.me/ECDS4" aria-label="Telegram"><img alt="Telegram" height="24" src="https://cdn.simpleicons.org/telegram/26A5E4"></a>
  &nbsp;
  <a href="https://github.com/ECD5A/v380-camera-device-id-recovery" aria-label="GitHub repository"><picture><source media="(prefers-color-scheme: dark)" srcset="https://cdn.simpleicons.org/github/FFFFFF"><img alt="GitHub repository" height="24" src="https://cdn.simpleicons.org/github/181717"></picture></a>
</p>
