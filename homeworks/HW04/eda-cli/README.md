# HW04 – HTTP-сервис качества датасетов поверх проекта eda-cli (FastAPI + REST API).

HTTP-сервис качества датасетов поверх проекта eda-cli.
Используется в рамках Домашнего задания 04 курса «Инженерия ИИ».

## Требования

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) установлен в систему

## Инициализация проекта

В корне проекта (HW03):

```bash
uv sync
```

Эта команда:

- создаст виртуальное окружение `.venv`;
- установит зависимости из `pyproject.toml`;
- установит сам проект `eda-cli` в окружение.

## Запуск CLI

### Краткий обзор

```bash
uv run eda-cli overview data/example.csv
```

Параметры:

- `--sep` – разделитель (по умолчанию `,`);
- `--encoding` – кодировка (по умолчанию `utf-8`).

~~~bash
uv run eda-cli head data/example.csv --n 10
~~~

Параметры:

- `--sep` – разделитель (по умолчанию `,`);
- `--encoding` – кодировка (по умолчанию `utf-8`).
- `--n` – количество первых строк датасета(по умолчанию `5`).

### Полный EDA-отчёт

```bash
uv run eda-cli report data/example.csv --out-dir reports
```

Параметры:

- `--out-dir` – каталог для отчёта.
- `--sep` – разделитель (по умолчанию `,`).
- `--encoding` – кодировка (по умолчанию `utf-8`).
- `--max-hist-columns` – максимум числовых колонок для гистограмм (по умолчанию `6`).
- `--top-k-categories` – top-значений для категориальных признаков (по умолчанию `5`).
- `--title` – заголовок отчёта (по умолчанию `EDA-отчёт`).
- `--min-missing-share` – порог доли пропусков, выше которого колонка считается проблемной (по умолчанию `0.05`).

В результате в каталоге `reports/` появятся:

- `report.md` – основной отчёт в Markdown;
- `summary.csv` – таблица по колонкам;
- `missing.csv` – пропуски по колонкам;
- `correlation.csv` – корреляционная матрица (если есть числовые признаки);
- `top_categories/*.csv` – top-k категорий по строковым признакам;
- `hist_*.png` – гистограммы числовых колонок;
- `missing_matrix.png` – визуализация пропусков;
- `correlation_heatmap.png` – тепловая карта корреляций.

Пример вызова eda-cli report с новыми опциями:

```bash
uv run eda-cli report .\data\example.csv --out-dir reports_example --max-hist-columns 5 --title "Мой отчёт" --top-k-categories 4 --min-missing-share 0.052
```

## Тесты

```bash
uv run pytest -q
```


## HTTP-сервис

Запуск серсиса:

```bash
uv run uvicorn eda_cli.api:app --reload --port 8000
```
URL после запуска сервиса
- `http://127.0.0.1:8000/docs`

Системный эндпоинт:

- `/health` – простой health-check сервиса.

Эндпоинты качества:
- `/quality` - принимает агрегированные признаки датасета и возвращает эвристическую оценку качества.
- `/quality-from-csv` - Эндпоинт, который принимает CSV-файл, запускает EDA-ядро (summarize_dataset + missing_table + compute_quality_flags) и возвращает оценку качества данных.
- `/quality-flags-from-csv` - Эндпоинт, который принимает CSV-файл, запускает EDA-ядро (summarize_dataset + missing_table + compute_quality_flags) и возвращает набов флагов качества данных.

Эндпоинт по выводу данных csv:
- `/head` - Эндпоинт, который принимает CSV-файл, параметр n (число выводимых строк) и возвращает первых n строк данных.