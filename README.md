# Неофициальный русский перевод Scarlet Hollow

Перевод актуален для версии **25889443**.

Версия перевода: **1.0.5**.

100% перевод текста, картинок, видео.

[Скачать перевод 1.0.5](https://github.com/vorpalko/scarlet-hollow-ru/releases/download/v1.0.5/ScarletHollow_RU_1.0.5.zip)

## Установка

1. Откройте папку Scarlet Hollow, где находятся `ScarletHollow.exe` и папка `game`.
   В Steam: свойства игры → установленные файлы → обзор.
2. Скопируйте папку `game` из этого комплекта в папку Scarlet Hollow.
   Объедините её с существующей папкой `game`; при обновлении подтвердите
   замену совпадающих файлов перевода. Вложенной папки `game/game` быть не должно.
3. Запустите игру обычным способом и выберите «Русский» в главном меню.

Скачанный ZIP сначала распакуйте. Корневой README копировать в игру не требуется.

Во время реплики и выбора ответа клавиша Q открывает текст на другом языке.
Q или Esc закрывает панель. Основной язык и изображения при этом не переключаются.

## Обновление и удаление

Для обновления этой версии повторите копирование с заменой файлов.
Для чистой переустановки сначала удалите прежний слой по перечню ниже.

Для удаления перевода при закрытой игре удалите только принадлежащие ему папки
`game/tl/russian` и `game/ru_support`, а также следующие файлы:

- `game/zz_ru_accessibility.rpy`;
- `game/zz_ru_choice.rpy`;
- `game/zz_ru_creation.rpy`;
- `game/zz_ru_display.rpy`;
- `game/zz_ru_episode2_journal_text.rpy`;
- `game/zz_ru_episode3_journal_text.rpy`;
- `game/zz_ru_episode4_journal_text.rpy`;
- `game/zz_ru_episode4_video.rpy`;
- `game/zz_ru_episode_graphics.rpy`;
- `game/zz_ru_graphics.rpy`;
- `game/zz_ru_journal_text.rpy`;
- `game/zz_ru_media_compat.rpy`;
- `game/zz_ru_runtime.rpy`;
- `game/zz_ru_save_names.rpy`;
- `game/zz_ru_version_warning.rpy`.

У каждого перечисленного `.rpy` также удалите одноимённый `.rpyc`, если игра
успела его создать. Например: `zz_ru_runtime.rpy` и `zz_ru_runtime.rpyc`.
