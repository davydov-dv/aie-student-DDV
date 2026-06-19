"""
Конфигурация проекта
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Базовые пути
BASE_DIR = Path(__file__).parent.parent
CONFIGS_DIR = BASE_DIR / "configs"
DATA_DIR = BASE_DIR / "data"
ARTIFACTS_DIR = BASE_DIR / "artifacts"

# Загружаем .env из configs/
env_path = CONFIGS_DIR / ".env"
if env_path.exists():
    load_dotenv(env_path)
    print(f"Загружен конфиг: {env_path}")
else:
    print(f"Файл .env не найден в {CONFIGS_DIR}, используются значения по умолчанию")

# Пути к моделям и энкодерам
MODEL_PATH = os.getenv("MODEL_PATH", str(ARTIFACTS_DIR / "lgbm_anomaly_model.pkl"))
ENCODERS_PATH = os.getenv("ENCODERS_PATH", str(ARTIFACTS_DIR / "label_encoders.pkl"))

# Настройки API
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Категориальные колонки (для предобработки)
CATEGORICAL_COLS = ['proto', 'service', 'state']

print(f"Конфигурация загружена:")
print(f"  - MODEL_PATH: {MODEL_PATH}")
print(f"  - ENCODERS_PATH: {ENCODERS_PATH}")
print(f"  - API: {API_HOST}:{API_PORT}")