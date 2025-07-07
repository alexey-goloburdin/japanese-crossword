Попытка написать решатель [японских кроссвордов](https://ru.wikipedia.org/wiki/%D0%AF%D0%BF%D0%BE%D0%BD%D1%81%D0%BA%D0%B8%D0%B9_%D0%BA%D1%80%D0%BE%D1%81%D1%81%D0%B2%D0%BE%D1%80%D0%B4).

# Использование

Используется `uv` ([установка uv](https://github.com/astral-sh/uv)) для работы с Python-проектами.

```bash
# Клонирование репозитория
git clone https://github.com/alexey-goloburdin/japanese-crossword.git
cd japanese-crossword

# Установка зависимостей
uv sync

# Запуск решения одного из кроссвордов, его исхдодные данные в JSON-файле crosswords/1.json
uv run python -m japanese_crossword crosswords/1.json
```

# Разработка

```bash
# Создание виртуального окружения и установка dev-зависимостей
uv sync --dev
uv pip install -e .

# Установка правил pre-commit для их выполнения перед коммитом
uv run pre-commit install

# Запуск тестов
uv run pytest

# Запуск линтера и форматирования кода
uv run ruff check src/ tests/
uv run ruff format src/ tests/

# Запуск проверки типов
uv run pyright src/
```

«Колбасками» в коде называем непрерывные закрашенные сегменты:)

# TODO

Программа в активной разработке, TODO:

- [ ] продлить те колбаски, которые начинаются рядом с краем строки/столбца и явно идут дальше от начальной точки (см. столбец 10)
- [ ] типизация
- [ ] `get_size` пусть возвращает `namedtuple`
- [ ] автотесты
- [ ] унификация структурно повторяющегося кода
- [ ] рефакторинг
