import pytest
import pandas as pd
import numpy as np
from pathlib import Path

from src.data.preprocessor import DataPreprocessor
from src.config import ENCODERS_PATH, CATEGORICAL_COLS


class TestDataPreprocessorInit:
    """Тесты инициализации DataPreprocessor"""
    
    def test_preprocessor_creation(self):
        """Проверка создания предобработчика"""
        preprocessor = DataPreprocessor(ENCODERS_PATH)
        assert preprocessor is not None
        assert preprocessor.encoders is not None
    
    def test_preprocessor_loads_encoders(self):
        """Проверка, что энкодеры загружены"""
        preprocessor = DataPreprocessor(ENCODERS_PATH)
        assert len(preprocessor.encoders) > 0
    
    def test_preprocessor_invalid_path(self):
        """Проверка обработки невалидного пути"""
        with pytest.raises(FileNotFoundError):
            DataPreprocessor("nonexistent_path.pkl")


class TestDataPreprocessorPreprocess:
    """Тесты метода preprocess"""
    
    def test_preprocess_dataframe(self, sample_dataframe):
        """Тест предобработки DataFrame"""
        preprocessor = DataPreprocessor(ENCODERS_PATH)
        result = preprocessor.preprocess(sample_dataframe, CATEGORICAL_COLS)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_dataframe)
    
    def test_preprocess_encodes_categorical(self, sample_dataframe):
        """Проверка, что категориальные колонки закодированы"""
        preprocessor = DataPreprocessor(ENCODERS_PATH)
        result = preprocessor.preprocess(sample_dataframe, CATEGORICAL_COLS)
        
        for col in CATEGORICAL_COLS:
            if col in result.columns:
                # Проверяем, что тип числовой (int или float)
                assert result[col].dtype in [np.int32, np.int64, np.float64, int, float]
    
    def test_preprocess_handles_unknown_category(self, sample_dataframe):
        """Проверка обработки неизвестных категорий"""
        preprocessor = DataPreprocessor(ENCODERS_PATH)
        
        # Добавляем неизвестную категорию
        df = sample_dataframe.copy()
        df.loc[0, 'proto'] = 'unknown_protocol_xyz'
        
        result = preprocessor.preprocess(df, CATEGORICAL_COLS)
        
        # Неизвестная категория должна быть закодирована как -1
        assert result.loc[0, 'proto'] == -1
    
    def test_preprocess_preserves_numeric_columns(self, sample_dataframe):
        """Проверка, что числовые колонки не изменяются"""
        preprocessor = DataPreprocessor(ENCODERS_PATH)
        result = preprocessor.preprocess(sample_dataframe, CATEGORICAL_COLS)
        
        # Числовые колонки должны остаться прежними
        assert result['dur'].equals(sample_dataframe['dur'])
        assert result['sbytes'].equals(sample_dataframe['sbytes'])


class TestDataPreprocessorPreprocessDict:
    """Тесты метода preprocess_dict"""
    
    def test_preprocess_dict(self, sample_normal_flow):
        """Тест предобработки словаря"""
        preprocessor = DataPreprocessor(ENCODERS_PATH)
        result = preprocessor.preprocess_dict(sample_normal_flow, CATEGORICAL_COLS)
        
        assert isinstance(result, dict)
        assert len(result) == len(sample_normal_flow)
    
    def test_preprocess_dict_encodes_categorical(self, sample_normal_flow):
        """Проверка кодирования категорий в словаре"""
        preprocessor = DataPreprocessor(ENCODERS_PATH)
        result = preprocessor.preprocess_dict(sample_normal_flow, CATEGORICAL_COLS)
        
        for col in CATEGORICAL_COLS:
            if col in result:
                # Проверяем, что тип числовой (int или float)
                assert isinstance(result[col], (int, float, np.integer, np.floating))