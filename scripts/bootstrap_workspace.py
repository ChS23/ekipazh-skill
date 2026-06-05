#!/usr/bin/env python3
"""Bootstrap an Ekipazh business workspace without overwriting user files."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


DIRECTORIES = [
    "профиль",
    "анализ/персоны",
    "правила",
    "контент/посты/идеи",
    "контент/посты/черновики",
    "контент/посты/опубликовано",
    "контент/кп/черновики",
    "контент/кп/отправлено",
    "контент/кп/принято",
    "контент/кп/отказано",
    "контент/возражения",
    "решения",
    "база",
    "агенты",
    ".agents/skills",
]


def today() -> str:
    return date.today().isoformat()


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def read_asset(name: str) -> str:
    content = (skill_root() / "assets" / name).read_text(encoding="utf-8")
    return content.replace("YYYY-MM-DD", today())


def write_once(path: Path, content: str, created: list[Path], skipped: list[Path]) -> None:
    if path.exists():
        skipped.append(path)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    created.append(path)


def index_md() -> str:
    return f"""---
type: индекс
status: черновик
created: {today()}
sources: []
---

# Индекс Базы

## Профиль

- профиль/бизнес.md — черновик
- профиль/стиль.md — черновик
- профиль/состояние.md — черновик

## Анализ

- анализ/рынок.md — не создан
- анализ/конкуренты.md — не создан
- анализ/swot.md — не создан
- анализ/персоны/ — папка создана

## Правила И Решения

- правила/ — папка создана
- решения/решение-001-тон.md — черновик первичного решения

## Контент И Продажи

- контент/посты/ — папки созданы
- контент/кп/ — папки созданы
- контент/возражения/ — папка создана

## База Знаний

- база/факты.md — черновик
- база/термины.md — черновик
- база/открытые-вопросы.md — черновик
- база/паттерны.md — черновик

## Агенты

- агенты/README.md — карта локальных агентов
- .agents/skills/ — место для зрелых мини-скиллов

## Лучший Следующий Шаг

Заполнить критические поля профиля: что делает бизнес, для кого и какой результат получает клиент.
"""


def open_questions_md() -> str:
    return f"""---
type: открытые-вопросы
status: черновик
created: {today()}
sources: []
---

# Открытые Вопросы

## Критические

1. Что ты делаешь и для кого?
2. Какой результат клиент получает после работы с тобой?
3. Что сейчас больше всего забирает время или раздражает?

## Вспомогательные

- Какие каналы продаж уже есть?
- Какой тон общения точно подходит или точно не подходит?
- Какие примеры контента или КП считаются удачными?
"""


def facts_md() -> str:
    return f"""---
type: факты
status: черновик
created: {today()}
sources: []
---

# Факты

Проверенные факты пока не собраны. Новые факты добавлять только после явного сообщения пользователя или проверки файлами.
"""


def terms_md() -> str:
    return f"""---
type: термины
status: черновик
created: {today()}
sources: []
---

# Термины

Словарь бизнеса пока не собран.

## Любимые Формулировки

- [уточнить]

## Нежелательные Формулировки

- [уточнить]
"""


def patterns_md() -> str:
    return f"""---
type: паттерны
status: черновик
created: {today()}
sources: []
---

# Паттерны

Повторяющиеся темы, правки, каналы и реакции клиентов пока не выявлены.
"""


def agents_readme() -> str:
    return """# Локальные агенты

Пока отдельных агентов нет.

## Когда создавать агента

- процесс повторился 3+ раза
- есть понятный вход и выход
- есть правила качества
- пользователь явно попросил автоматизировать роль

## Доступная база

- профиль/бизнес.md
- профиль/стиль.md
- профиль/состояние.md
- правила/
- база/

## Мини-скиллы

Зрелые повторяемые процессы сохраняются в `.agents/skills/<name>/SKILL.md`.
"""


def tone_decision() -> str:
    return f"""---
type: решение
status: черновик
created: {today()}
sources:
  - профиль/стиль.md
---

# Решение 001: Тон Экипажа

## Контекст

Первичная настройка локальной базы бизнеса.

## Решение

Пока использовать спокойный рабочий тон, обращение на "ты". Уточнить у пользователя, если нужен другой формат.

## Альтернативы

| Вариант | Плюсы | Минусы |
| --- | --- | --- |
| Формально | подходит для B2B и документов | может звучать сухо |
| Дружески | легче для быстрых итераций | может быть слишком разговорно |
| Экспертно | подчёркивает опыт | может звучать тяжело |

## Метрика успеха

Пользователь меньше правит стиль и формулировки.

## Пересмотр

После первых 2-3 правок стиля.
"""


def bootstrap(workspace: Path) -> tuple[list[Path], list[Path]]:
    workspace = workspace.resolve()
    created: list[Path] = []
    skipped: list[Path] = []

    for directory in DIRECTORIES:
        (workspace / directory).mkdir(parents=True, exist_ok=True)

    files = {
        "профиль/бизнес.md": read_asset("business.md"),
        "профиль/стиль.md": read_asset("style.md"),
        "профиль/состояние.md": read_asset("current-state.md"),
        "решения/решение-001-тон.md": tone_decision(),
        "база/индекс.md": index_md(),
        "база/факты.md": facts_md(),
        "база/термины.md": terms_md(),
        "база/открытые-вопросы.md": open_questions_md(),
        "база/паттерны.md": patterns_md(),
        "агенты/README.md": agents_readme(),
    }

    for relative_path, content in files.items():
        write_once(workspace / relative_path, content, created, skipped)

    return created, skipped


def main() -> None:
    parser = argparse.ArgumentParser(description="Bootstrap an Ekipazh workspace.")
    parser.add_argument("workspace", nargs="?", default=".", help="Target workspace directory.")
    args = parser.parse_args()

    created, skipped = bootstrap(Path(args.workspace))
    print("created:")
    for path in created:
        print(f"- {path}")
    if skipped:
        print("skipped_existing:")
        for path in skipped:
            print(f"- {path}")


if __name__ == "__main__":
    main()
