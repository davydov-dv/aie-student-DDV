import pytest
import pandas as pd
import numpy as np
from pathlib import Path

from src.models.predictor import ModelPredictor
from src.data.preprocessor import DataPreprocessor
from src.config import MODEL_PATH, ENCODERS_PATH, CATEGORICAL_COLS


class TestModelPredictorInit:
    """Тесты инициализации ModelPredictor"""
    
    def test_predictor_creation(self):
        """Проверка создания предиктора"""
        predictor = ModelPredictor(MODEL_PATH)
        assert predictor is not None
        assert predictor.model is not None
    
    def test_predictor_invalid_path(self):
        """Проверка обработки невалидного пути"""
        with pytest.raises(FileNotFoundError):
            ModelPredictor("nonexistent_model.pkl")


class TestModelPredictorPredict:
    """Тесты метода predict"""
    
    def test_predict_single_row(self, sample_dataframe):
        """Тест предсказания для одной строки"""
        predictor = ModelPredictor(MODEL_PATH)
        preprocessor = DataPreprocessor(ENCODERS_PATH)
        
        # Предобработка
        processed_df = preprocessor.preprocess(sample_dataframe, CATEGORICAL_COLS)
        single_row = processed_df.iloc[[0]]
        
        result = predictor.predict(single_row)
        
        assert isinstance(result, dict)
        assert "prediction" in result
        assert "label" in result
        assert "confidence" in result
        assert "attack_probability" in result
    
    def test_predict_multiple_rows(self, sample_dataframe):
        """Тест предсказания для нескольких строк"""
        predictor = ModelPredictor(MODEL_PATH)
        preprocessor = DataPreprocessor(ENCODERS_PATH)
        
        # Предобработка
        processed_df = preprocessor.preprocess(sample_dataframe, CATEGORICAL_COLS)
        
        result = predictor.predict(processed_df)
        
        assert isinstance(result, list)
        assert len(result) == len(sample_dataframe)
        
        for item in result:
            assert "prediction" in item
            assert "label" in item
    
    def test_predict_label_values(self, sample_dataframe):
        """Проверка допустимых значений label"""
        predictor = ModelPredictor(MODEL_PATH)
        preprocessor = DataPreprocessor(ENCODERS_PATH)
        
        # Предобработка
        processed_df = preprocessor.preprocess(sample_dataframe, CATEGORICAL_COLS)
        
        result = predictor.predict(processed_df)
        
        if isinstance(result, list):
            labels = [item["label"] for item in result]
        else:
            labels = [result["label"]]
        
        for label in labels:
            assert label in ["Normal", "Attack"]
    
    def test_predict_confidence_range(self, sample_dataframe):
        """Проверка диапазона confidence"""
        predictor = ModelPredictor(MODEL_PATH)
        preprocessor = DataPreprocessor(ENCODERS_PATH)
        
        # Предобработка
        processed_df = preprocessor.preprocess(sample_dataframe, CATEGORICAL_COLS)
        
        result = predictor.predict(processed_df)
        
        if isinstance(result, list):
            confidences = [item["confidence"] for item in result]
        else:
            confidences = [result["confidence"]]
        
        for conf in confidences:
            assert 0 <= conf <= 1


class TestModelPredictorPredictDict:
    """Тесты метода predict_dict"""
    
    def test_predict_dict(self, sample_normal_flow):
        """Тест предсказания из словаря"""
        predictor = ModelPredictor(MODEL_PATH)
        preprocessor = DataPreprocessor(ENCODERS_PATH)
        
        # Предобработка
        processed_dict = preprocessor.preprocess_dict(sample_normal_flow, CATEGORICAL_COLS)
        
        result = predictor.predict_dict(processed_dict)
        
        assert isinstance(result, dict)
        assert "prediction" in result
        assert "label" in result
        assert "confidence" in result
    
    def test_predict_dict_consistency(self, sample_normal_flow):
        """Проверка согласованности предсказаний"""
        predictor = ModelPredictor(MODEL_PATH)
        preprocessor = DataPreprocessor(ENCODERS_PATH)
        
        # Предобработка
        processed_dict = preprocessor.preprocess_dict(sample_normal_flow, CATEGORICAL_COLS)
        
        result1 = predictor.predict_dict(processed_dict)
        result2 = predictor.predict_dict(processed_dict)
        
        # Один и тот же вход должен давать один и тот же выход
        assert result1["prediction"] == result2["prediction"]
        assert result1["label"] == result2["label"]