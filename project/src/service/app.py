from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from contextlib import asynccontextmanager
import logging
import time
from datetime import datetime

from src.config import (
    MODEL_PATH, 
    ENCODERS_PATH, 
    API_HOST, 
    API_PORT, 
    LOG_LEVEL,
    CATEGORICAL_COLS
)
from src.data.preprocessor import DataPreprocessor
from src.models.predictor import ModelPredictor

# Настройка логирования
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Глобальные объекты
preprocessor = None
predictor = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager для инициализации и очистки ресурсов"""
    global preprocessor, predictor
    
    # Startup
    logger.info("Запуск сервиса...")
    
    try:
        # Загружаем предобработчик
        preprocessor = DataPreprocessor(ENCODERS_PATH)
        logger.info(f"Предобработчик загружен")
        
        # Загружаем модель
        predictor = ModelPredictor(MODEL_PATH)
        logger.info(f"Модель загружена")
        
        logger.info("Сервис готов к работе")
    except Exception as e:
        logger.error(f"Ошибка при загрузке: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Остановка сервиса...")

# Создаём приложение
app = FastAPI(
    title="Network Anomaly Detection API",
    description="API для детекции аномалий в сетевом трафике",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/health")
async def health_check():
    """
    Проверка здоровья сервиса
    """
    return {
        "status": "healthy",
        "model_loaded": predictor is not None,
        "preprocessor_loaded": preprocessor is not None,
        "timestamp": datetime.now().isoformat()
    }

class NetworkFlow(BaseModel):
    """
    Схема входных данных (сетевой поток)
    """
    dur: float
    proto: str
    service: str
    state: str
    spkts: int
    dpkts: int
    sbytes: int
    dbytes: int
    rate: float
    sttl: int
    dttl: int
    sload: float
    dload: float
    sloss: int
    dloss: int
    sinpkt: float
    dinpkt: float
    sjit: float
    djit: float
    swin: int
    stcpb: int
    dtcpb: int
    dwin: int
    tcprtt: float
    synack: float
    ackdat: float
    smean: float
    dmean: float
    trans_depth: int
    response_body_len: int
    ct_srv_src: int
    ct_state_ttl: int
    ct_dst_ltm: int
    ct_src_dport_ltm: int
    ct_dst_sport_ltm: int
    ct_dst_src_ltm: int
    is_ftp_login: int
    ct_ftp_cmd: int
    ct_flw_http_mthd: int
    ct_src_ltm: int
    ct_srv_dst: int
    is_sm_ips_ports: int

@app.post("/predict")
async def predict_anomaly(flow: NetworkFlow):
    """
    Предсказание аномалии для сетевого потока
    
    :param flow: данные сетевого потока
    :return: результат предсказания
    """
    start_time = time.time()
    
    try:
        # Проверяем, что модель и предобработчик загружены
        if preprocessor is None or predictor is None:
            raise RuntimeError("Модель или предобработчик не загружены")
        
        # Конвертируем в словарь (используем model_dump для Pydantic v2)
        flow_dict = flow.model_dump()
        
        # Предобработка (кодирование категорий)
        processed_dict = preprocessor.preprocess_dict(flow_dict, CATEGORICAL_COLS)
        
        # Предсказание
        result = predictor.predict_dict(processed_dict)
        
        # Логирование
        processing_time = time.time() - start_time
        logger.info(
            f"Prediction: label={result['label']}, "
            f"confidence={result['confidence']}, "
            f"time={processing_time:.3f}s"
        )
        
        # Добавляем время обработки
        result["processing_time_ms"] = round(processing_time * 1000, 2)
        
        return result
    
    except Exception as e:
        logger.error(f"Ошибка при предсказании: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """
    Корневой эндпоинт
    """
    return {
        "message": "Network Anomaly Detection API",
        "version": "1.0.0",
        "endpoints": {
            "/health": "Проверка здоровья сервиса",
            "/predict": "Предсказание аномалии (POST)"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)