# Экипаж Skill

Универсальный Agent Skill для русскоязычного эксперта, фрилансера или самозанятого. Он превращает пустую рабочую папку в локальную Markdown-базу бизнеса и ведёт человека по процессу: профиль, стиль, состояние, анализ, правила, контент, КП, возражения, решения, база знаний и локальные агенты.

Репозиторий: <https://github.com/ChS23/ekipazh-skill>

## Что делает

- сам стартует в пустой папке и создаёт рабочую структуру
- ведёт короткое интервью, не превращая старт в длинную анкету
- сохраняет знания локально в Markdown, пригодно для git
- пишет посты, КП, ответы на возражения в стиле бизнеса
- формализует повторяющийся опыт в правила
- создаёт specs локальных агентов и мини-скиллы для повторяемых процессов
- оставляет handoff для будущих агентов в `база/` и `агенты/`

## Установка

Если используешь agents-compatible клиент:

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/ChS23/ekipazh-skill ~/.agents/skills/ekipazh
```

Для локальной разработки:

```bash
git clone https://github.com/ChS23/ekipazh-skill
```

## Первый запуск

Открой пустую папку бизнеса и попроси агента:

```text
Используй $ekipazh. Я [кратко что делаю]. Настрой папку под мой бизнес.
```

Skill должен сначала создать файлы, потом задавать вопросы. Быстрый bootstrap можно запустить вручную:

```bash
python3 ~/.agents/skills/ekipazh/scripts/bootstrap_workspace.py .
```

## Структура рабочей папки

После старта появляются:

```text
профиль/      бизнес.md, стиль.md, состояние.md
анализ/       рынок.md, конкуренты.md, swot.md, персоны/
правила/      правило-NNN-*.md
контент/      посты/, кп/, возражения/
решения/      решение-NNN-*.md
база/         индекс.md, факты.md, термины.md, открытые-вопросы.md, паттерны.md
агенты/       README.md, агент-*.md
.agents/      skills/<workflow-name>/SKILL.md
```

## Соответствие Claude-плагину

| Claude plugin | Agent Skill |
| --- | --- |
| `output-styles/ekipazh.md` | `SKILL.md` + `references/operating-loop.md` |
| `/start` | `references/onboarding.md` + `scripts/bootstrap_workspace.py` |
| `/status` | `references/workspace.md` |
| `/analyze` | `references/analysis.md` |
| `/rule` | `references/rules.md` |
| `/post` | `references/content.md` |
| `/kp`, `/objection` | `references/sales.md` |
| `/edit` | inline iteration в `SKILL.md`, `content.md`, `sales.md` |
| `/format` | `references/format.md` |
| `/workflow` | `references/agents.md` |
| `/setup` | не переносится как core skill: это Claude/IDE-specific запуск |
| `agents/interviewer`, `analyst`, `operator` | роли встроены в процессы onboarding, analysis, operating loop |
| SessionStart hook | стартовый скан в `SKILL.md` |

Намеренно не перенесены Claude-specific части: `.claude-plugin/`, marketplace manifest, slash-команды, `.claude/rules/`, Claude memory и desktop/IDE launch scripts. В skill они заменены переносимыми локальными файлами: `база/`, `агенты/`, `.agents/skills/`.

## Проверка

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.agents/skills/ekipazh
python3 ~/.agents/skills/ekipazh/scripts/bootstrap_workspace.py /tmp/ekipazh-bootstrap-test
```

Ожидаемо:

- `Skill is valid!`
- в тестовой папке созданы профиль, база, решение о тоне и `агенты/README.md`

## Лицензия

MIT
