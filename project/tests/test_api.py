import pytest
from fastapi.testclient import TestClient


class TestHealthEndpoint:
    """Тесты эндпоинта /health"""
    
    def test_health_check_status(self, client):
        """Проверка статуса /health"""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_check_response_structure(self, client):
        """Проверка структуры ответа /health"""
        response = client.get("/health")
        data = response.json()
        
        assert "status" in data
        assert "model_loaded" in data
        assert "preprocessor_loaded" in data
        assert "timestamp" in data
    
    def test_health_check_model_loaded(self, client):
        """Проверка, что модель загружена"""
        response = client.get("/health")
        data = response.json()
        
        assert data["status"] == "healthy"
        assert data["model_loaded"] is True
        assert data["preprocessor_loaded"] is True


class TestRootEndpoint:
    """Тесты корневого эндпоинта /"""
    
    def test_root_endpoint(self, client):
        """Проверка корневого эндпоинта"""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_root_response_structure(self, client):
        """Проверка структуры ответа /"""
        response = client.get("/")
        data = response.json()
        
        assert "message" in data
        assert "version" in data
        assert "endpoints" in data
    
    def test_root_contains_endpoints_info(self, client):
        """Проверка, что в ответе есть информация об эндпоинтах"""
        response = client.get("/")
        data = response.json()
        
        assert "/health" in data["endpoints"]
        assert "/predict" in data["endpoints"]


class TestPredictEndpoint:
    """Тесты эндпоинта /predict"""
    
    def test_predict_normal_flow(self, client, sample_normal_flow):
        """Тест предсказания для нормального потока"""
        response = client.post("/predict", json=sample_normal_flow)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "prediction" in data
        assert "label" in data
        assert "confidence" in data
        assert "attack_probability" in data
        assert "processing_time_ms" in data
    
    def test_predict_attack_flow(self, client, sample_attack_flow):
        """Тест предсказания для аномального потока"""
        response = client.post("/predict", json=sample_attack_flow)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "prediction" in data
        assert "label" in data
        assert "confidence" in data
    
    def test_predict_response_types(self, client, sample_normal_flow):
        """Проверка типов данных в ответе"""
        response = client.post("/predict", json=sample_normal_flow)
        data = response.json()
        
        assert isinstance(data["prediction"], int)
        assert isinstance(data["label"], str)
        assert isinstance(data["confidence"], float)
        assert isinstance(data["attack_probability"], float)
        assert isinstance(data["processing_time_ms"], float)
    
    def test_predict_label_values(self, client, sample_normal_flow):
        """Проверка, что label принимает только допустимые значения"""
        response = client.post("/predict", json=sample_normal_flow)
        data = response.json()
        
        assert data["label"] in ["Normal", "Attack"]
    
    def test_predict_confidence_range(self, client, sample_normal_flow):
        """Проверка, что confidence в диапазоне [0, 1]"""
        response = client.post("/predict", json=sample_normal_flow)
        data = response.json()
        
        assert 0 <= data["confidence"] <= 1
        assert 0 <= data["attack_probability"] <= 1
    
    def test_predict_invalid_data(self, client):
        """Тест с невалидными данными"""
        invalid_flow = {
            "dur": "not_a_number",  # Должно быть float
            "proto": "udp",
        }
        
        response = client.post("/predict", json=invalid_flow)
        assert response.status_code == 422  # Validation error
    
    def test_predict_missing_fields(self, client):
        """Тест с отсутствующими обязательными полями"""
        incomplete_flow = {
            "dur": 0.000011,
            "proto": "udp"
            # Отсутствуют все остальные поля
        }
        
        response = client.post("/predict", json=incomplete_flow)
        assert response.status_code == 422
    
    def test_predict_processing_time(self, client, sample_normal_flow):
        """Проверка, что время обработки разумное (< 1 секунды)"""
        response = client.post("/predict", json=sample_normal_flow)
        data = response.json()
        
        assert data["processing_time_ms"] < 1000  # Менее 1 секунды


class TestPredictEndpointEdgeCases:
    """Тесты граничных случаев для /predict"""
    
    def test_predict_with_unknown_protocol(self, client, sample_normal_flow):
        """Тест с неизвестным протоколом (должен обработаться как -1)"""
        flow = sample_normal_flow.copy()
        flow["proto"] = "unknown_protocol_xyz"
        
        response = client.post("/predict", json=flow)
        assert response.status_code == 200
    
    def test_predict_with_empty_service(self, client, sample_normal_flow):
        """Тест с пустым сервисом"""
        flow = sample_normal_flow.copy()
        flow["service"] = ""
        
        response = client.post("/predict", json=flow)
        assert response.status_code == 200
    
    def test_predict_with_zero_bytes(self, client, sample_normal_flow):
        """Тест с нулевыми байтами"""
        flow = sample_normal_flow.copy()
        flow["sbytes"] = 0
        flow["dbytes"] = 0
        
        response = client.post("/predict", json=flow)
        assert response.status_code == 200
    
    def test_predict_with_very_large_values(self, client, sample_normal_flow):
        """Тест с очень большими значениями"""
        flow = sample_normal_flow.copy()
        flow["sbytes"] = 999999999999
        flow["rate"] = 999999999999.999
        
        response = client.post("/predict", json=flow)
        assert response.status_code == 200