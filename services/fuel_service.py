import httpx
from utils.distance import calculate_distance

class FuelService:
    def __init__(self):
        self.api_url = "https://api.bencinaenlinea.cl/api"
    
    def test_connection(self):
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(f"{self.api_url}/combustible_ciudadano")
                if response.status_code == 200:
                    return "Conexión ready"
                else:
                    return f"Respuesta: {response.status_code}"
        except Exception as e:
            return f"Error de conexión: {str(e)}"
    
    def get_combustibles(self):
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(f"{self.api_url}/combustible_ciudadano")
                if response.status_code == 200:
                    return response.json()
                else:
                    return {"error": f"Status: {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
        
    def buscar_estaciones(self):
        try:
            with httpx.Client(timeout=30.0) as client:
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
            # Obtener todas las estaciones
            estaciones_data = self.buscar_estaciones()
            if 'error' in estaciones_data:
                return estaciones_data
            
            estaciones = estaciones_data.get('data', [])
            
            # Mapeo de productos basado en la API real
            product_map = {"93": 1, "95": 7, "97": 2, "diesel": 3, "kerosene": 4}
            product_id = product_map.get(product.lower())
            
            if not product_id:
                return {"error": "Producto no válido. Use: 93, 95, 97, diesel, kerosene"}
            
            resultado = []
            
            for estacion in estaciones:
                # Validar coordenadas
                if not estacion.get('latitud') or not estacion.get('longitud'):
                    continue
                    
                # Buscar el combustible específico
                combustibles = estacion.get('combustibles', [])
                precio_producto = None
                
                for combustible in combustibles:
                    if combustible.get('id') == product_id:
                        precio_str = combustible.get('precio')
                        if precio_str is not None:
                            try:
                                precio_producto = int(float(precio_str))
                                break
                            except (ValueError, TypeError):
                                continue
                
                if precio_producto is None:
                    continue
                
                 # Verificar si tiene tienda
                servicios = estacion.get('servicios', [])
                # Considerar que tiene tienda si tiene 2 o más servicios
                tiene_tienda = len(servicios) >= 2
                
                # Filtrar por tienda si se requiere
                if store and not tiene_tienda:
                    continue
                
                # Calcular distancia
                try:
                    est_lat_str = estacion.get('latitud')
                    est_lng_str = estacion.get('longitud')
                    
                    if est_lat_str is None or est_lng_str is None:
                        continue
                        
                    est_lat = float(est_lat_str)
                    est_lng = float(est_lng_str)
                    distancia = calculate_distance(lat, lng, est_lat, est_lng)
                except (ValueError, TypeError):
                    continue
                
                resultado.append({
                    "id": estacion.get('id'),
                    "compania": estacion.get('marca', 'N/A'),
                    "direccion": estacion.get('direccion', 'N/A'),
                    "comuna": estacion.get('comuna', 'N/A'),
                    "region": estacion.get('region', 'N/A'),
                    "latitud": est_lat,
                    "longitud": est_lng,
                    "distancia": round(distancia, 2),
                    "precio": precio_producto,
                    "producto": product,
                    "tiene_tienda": tiene_tienda
                })
            
            # Implementación de los 4 casos de búsqueda
            if nearest and cheapest:
                # Caso: más cercana con menor precio
                resultado.sort(key=lambda x: x['distancia'])
                cercanas = resultado[:15]  # Top 15 más cercanas
                cercanas.sort(key=lambda x: x['precio'])  # Entre esas, la más barata
                return cercanas[0] if cercanas else {"error": "No se encontraron estaciones"}
            elif nearest:
                # Caso: más cercana
                resultado.sort(key=lambda x: x['distancia'])
            elif cheapest:
                # Caso: menor precio
                resultado.sort(key=lambda x: x['precio'])
            else:
                # Sin criterios específicos, ordenar por distancia
                resultado.sort(key=lambda x: x['distancia'])
            
            return resultado[0] if resultado else {"error": "No se encontraron estaciones"}
            
        except Exception as e:
            return {"error": str(e)}