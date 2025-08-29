import pytest
from services.fuel_service import FuelService
from utils.distance import calculate_distance
from utils.mappings import get_product_id, get_company_name, validate_product
from utils.search_utils import validate_coordinates

class TestServicios:
    """Tests para el servicio de combustibles"""

    def test_inicializar_servicio(self):
        """Test de inicialización del servicio"""
        servicio = FuelService()
        assert servicio.api_url is not None
        assert servicio.timeout > 0
    
    def test_mapeo_combustibles(self):
        """Test del mapeo de productos usando las utilidades"""
        # Verificar que el mapeo de productos funcione
        productos_validos = ["93", "95", "97", "diesel", "kerosene"]
        
        for producto in productos_validos:
            assert validate_product(producto)
            id_producto = get_product_id(producto)
            assert id_producto is not None
            assert isinstance(id_producto, int)

class TestMappings:
    """Tests para las utilidades de mapeo"""
    
    def test_mapeo_companias(self):
        """Test del mapeo de compañías"""
        # Test con algunas compañías conocidas
        assert get_company_name(5) == "COPEC"
        assert get_company_name(4) == "SHELL"
        assert get_company_name(3) == "TERPEL"
        assert get_company_name(999) == "Compañía 999"  # ID no existente
    
    def test_validacion_productos(self):
        """Test de validación de productos"""
        assert validate_product("93") == True
        assert validate_product("95") == True
        assert validate_product("97") == True
        assert validate_product("diesel") == True
        assert validate_product("kerosene") == True
        assert validate_product("invalido") == False
        assert validate_product("") == False
        assert validate_product(None) == False

class TestDistancias:
    """Tests para el cálculo de distancias"""

    def test_mismo_punto(self):
        """Test de distancia entre el mismo punto"""
        dist = calculate_distance(-23.65, -70.40, -23.65, -70.40)
        assert dist == 0.0
    
    def test_puntos_conocidos(self):
        """Test de distancia entre puntos conocidos"""
        # Distancia aproximada entre Santiago y Valparaíso
        stgo_lat, stgo_lng = -33.4489, -70.6693
        valpo_lat, valpo_lng = -33.0458, -71.6197
        
        dist = calculate_distance(stgo_lat, stgo_lng, valpo_lat, valpo_lng)
        
        # La distancia real es aproximadamente 100 km
        assert 90 < dist < 120
    
    def test_distancia_positiva(self):
        """Test que la distancia siempre sea positiva"""
        dist = calculate_distance(-23.65, -70.40, -20.21, -70.15)
        assert dist >= 0

class TestBusquedas:
    """Tests para la lógica de búsqueda"""
    
    def test_validar_parametros(self):
        """Test de validación de parámetros de búsqueda"""
        servicio = FuelService()
        
        # Test con producto inválido
        resultado = servicio.search_stations(-23.65, -70.40, "invalido", nearest=True)
        assert "error" in resultado
        assert "Producto no válido" in resultado["error"]
    
    def test_validar_coordenadas(self):
        """Test de validación de coordenadas"""
        # Coordenadas válidas para Chile
        assert validate_coordinates(-33.45, -70.65) == True  # Santiago
        assert validate_coordinates(-23.65, -70.40) == True  # Antofagasta
        
        # Coordenadas fuera de Chile
        assert validate_coordinates(40.7128, -74.0060) == False  # NY
        assert validate_coordinates(0, 0) == False  # Ecuador
