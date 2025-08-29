import httpx
import os
from dotenv import load_dotenv
from utils.distance import calculate_distance
from utils.mappings import (
    get_product_id, 
    get_company_name, 
    has_convenience_store, 
    get_store_info, 
    validate_product,
    get_valid_products
)
from utils.search_utils import (
    process_station_data,
    filter_stations_by_store,
    apply_search_logic,
    build_error_response,
    validate_coordinates
)

# Cargar variables de entorno
load_dotenv()

class FuelService:
    def __init__(self):
        self.api_url = os.getenv("API_BASE_URL", "https://api.bencinaenlinea.cl/api")
        self.timeout = int(os.getenv("TIMEOUT_SECONDS", "30"))
    
    def test_connection(self):
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(f"{self.api_url}/combustible_ciudadano")
                if response.status_code == 200:
                    return "Conexión ready"
                else:
                    return f"Respuesta: {response.status_code}"
        except Exception as e:
            return f"Error de conexión: {str(e)}"
    
    def get_combustibles(self):
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(f"{self.api_url}/combustible_ciudadano")
                if response.status_code == 200:
                    return response.json()
                else:
                    return {"error": f"Status: {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
        
    def buscar_estaciones(self):
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(f"{self.api_url}/busqueda_estacion_filtro")
                if response.status_code == 200:
                    return response.json()
                else:
                    return {"error": f"Status: {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    def search_stations(self, lat: float, lng: float, product: str, nearest: bool = False, 
                       store: bool = False, cheapest: bool = False):
        try:
            # Validar coordenadas
            if not validate_coordinates(lat, lng):
                return build_error_response("Coordenadas fuera del rango válido para Chile")
            
            # Validar producto
            if not validate_product(product):
                valid_products = get_valid_products()
                return build_error_response(f"Producto no válido. Use: {', '.join(valid_products)}")
            
            # Obtener todas las estaciones
            datos_estaciones = self.buscar_estaciones()
            if 'error' in datos_estaciones:
                return datos_estaciones
            
            estaciones = datos_estaciones.get('data', [])
            id_producto = get_product_id(product)
            
            # Procesar cada estación
            estaciones_validas = []
            for estacion in estaciones:
                estacion_procesada = process_station_data(estacion, lat, lng, product, id_producto)
                if estacion_procesada:
                    estaciones_validas.append(estacion_procesada)
            
            # Filtrar por tienda si se requiere
            estaciones_filtradas = filter_stations_by_store(estaciones_validas, store)
            
            # Aplicar lógica de búsqueda
            resultado = apply_search_logic(estaciones_filtradas, product, nearest, cheapest)
            
            if not resultado:
                return build_error_response("No se encontraron estaciones que cumplan los criterios")
            
            return resultado
            
        except Exception as e:
            return build_error_response(str(e))