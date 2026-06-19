FROM python:3.10-slim

# Системные зависимости для LightGBM и healthcheck
RUN apt-get update && apt-get install -y \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Зависимости Python (кэшируются отдельно)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Конфигурация
COPY configs/ ./configs/

# Исходный код
COPY src/ ./src/

# Артефакты (модели и энкодеры)
COPY artifacts/ ./artifacts/

# Порт
EXPOSE 8000

# Запуск
CMD ["uvicorn", "src.service.app:app", "--host", "0.0.0.0", "--port", "8000"]