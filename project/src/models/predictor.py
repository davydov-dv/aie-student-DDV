"""
Модуль для загрузки модели и получения предсказаний
"""
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class ModelPredictor:
    """
    Класс для работы с обученной моделью
    """
    def __init__(self, model_path: str):
        """
        :param model_path: путь к файлу модели
        """
        self.model_path = Path(model_path)
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Загружает модель из файла"""
        if not self.model_path.exists():
            raise FileNotFoundError(f"Файл модели не найден: {self.model_path}")
        
        self.model = joblib.load(self.model_path)
        logger.info(f"Модель загружена: {self.model_path.name}")
    
    def predict(self, features: pd.DataFrame) -> Dict[str, Any]:
        """
        Делает предсказание
        
        :param features: DataFrame с признаками (одна строка или несколько)
        :return: словарь с результатами
        """
        if self.model is None:
            raise RuntimeError("Модель не загружена")
        
        # Предсказание
        prediction = self.model.predict(features)
        probabilities = self.model.predict_proba(features)
        
        # Формируем результат
        results = []
        for i in range(len(features)):
            pred_class = int(prediction[i])
            pred_proba = float(probabilities[i][pred_class])
            
            results.append({
                "prediction": pred_class,
                "label": "Attack" if pred_class == 1 else "Normal",
                "confidence": round(pred_proba, 4),
                "attack_probability": round(float(probabilities[i][1]), 4)
            })
        
        # Если одна строка — возвращаем словарь, иначе список
        if len(results) == 1:
            return results[0]
        return results
    
    def predict_dict(self, features_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Делает предсказание из словаря (для API)
        
        :param features_dict: словарь с признаками
        :return: словарь с результатами
        """
        features = pd.DataFrame([features_dict])
        return self.predict(features)