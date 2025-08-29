import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestsAPI:
    """Tests para los endpoints principales de la API"""

    def test_endpoint_inicio(self):
        """Test del endpoint raíz"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "mensaje" in data
        assert "autor" in data
        assert data["autor"] == "Ignacio Torres González"
    
    def test_endpoint_salud(self):
        """Test del endpoint de monitoreo de salud"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "timestamp" in data
        assert "version" in data
        assert data["version"] == "1.0.0"
    
    def test_endpoint_test(self):
        """Test del endpoint de prueba"""
        response = client.get("/test")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "OK"
    
    def test_buscar_sin_params(self):
        """Test del endpoint de búsqueda sin parámetros requeridos"""
        response = client.get("/api/stations/search")
        assert response.status_code == 422  # Error de validación
    
    def test_buscar_producto_malo(self):
        """Test del endpoint de búsqueda con producto inválido"""
        response = client.get("/api/stations/search?lat=-23.65&lng=-70.40&product=invalid")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == False
        assert "error" in data
    
    def test_buscar_ok(self):
        """Test del endpoint de búsqueda con parámetros válidos"""
        response = client.get("/api/stations/search?lat=-23.65&lng=-70.40&product=93&nearest=true")
        assert response.status_code == 200
        data = response.json()
        # Puede ser success=true o false dependiendo de la disponibilidad de la API externa
        assert "success" in data
        
        if data["success"]:
            assert "data" in data
            estacion = data["data"]
            assert "id" in estacion
            assert "distancia(lineal)" in estacion
        else:
            assert "error" in data
