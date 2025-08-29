"""
Módulo de utilidades para la lógica de búsqueda de estaciones.
Contiene funciones para procesar y filtrar estaciones de combustible.
"""

from typing import List, Dict, Any, Optional
from utils.distance import calculate_distance
from utils.mappings import get_company_name, has_convenience_store, get_store_info


def process_station_data(estacion: Dict[str, Any], lat: float, lng: float, 
                        product: str, id_producto: int) -> Optional[Dict[str, Any]]:
    """
    Procesa los datos de una estación individual.
    
    Args:
        estacion: Datos raw de la estación
        lat: Latitud de búsqueda
        lng: Longitud de búsqueda
        product: Producto solicitado
        id_producto: ID del producto
        
    Returns:
        Dict con datos procesados de la estación o None si no es válida
    """
    # Validar coordenadas
    if not estacion.get('latitud') or not estacion.get('longitud'):
        return None
        
    # Buscar el combustible específico
    combustibles = estacion.get('combustibles', [])
    precio_producto = None
    
    for combustible in combustibles:
        if combustible.get('id') == id_producto:
            precio_str = combustible.get('precio')
            if precio_str is not None:
                try:
                    precio_producto = int(float(precio_str))
                    break
                except (ValueError, TypeError):
                    continue
    
    if precio_producto is None:
        return None
    
    # Calcular distancia
    try:
        est_lat_str = estacion.get('latitud')
        est_lng_str = estacion.get('longitud')
        
        if est_lat_str is None or est_lng_str is None:
            return None
            
        est_lat = float(est_lat_str)
        est_lng = float(est_lng_str)
        distancia = calculate_distance(lat, lng, est_lat, est_lng)
    except (ValueError, TypeError):
        return None
    
    # Información de compañía y tienda
    id_compania = estacion.get('marca', 0)
    tiene_tienda = has_convenience_store(id_compania)
    nombre_compania = get_company_name(id_compania)
    
    # Generar info de tienda si aplica
    info_tienda = None
    if tiene_tienda:
        comuna = estacion.get('comuna', 'Local')
        station_id = str(estacion.get('id', '0000'))
        info_tienda = get_store_info(id_compania, nombre_compania, comuna, station_id)
    
    # Crear el objeto de respuesta
    estacion_resultado = {
        "id": str(estacion.get('id', 'N/A')),
        "compania": nombre_compania,
        "direccion": estacion.get('direccion', estacion.get('Direccion', 'N/A')),
        "comuna": estacion.get('comuna', estacion.get('Comuna', 'N/A')),
        "region": estacion.get('region', estacion.get('Region', 'N/A')),
        "latitud": est_lat,
        "longitud": est_lng,
        "distancia(lineal)": round(distancia, 2),
        f"precios{product}": precio_producto,
        "tiene_tienda": tiene_tienda
    }
    
    # Agregar info de tienda si existe
    if info_tienda:
        estacion_resultado["tienda"] = info_tienda
    
    return estacion_resultado


def filter_stations_by_store(estaciones: List[Dict[str, Any]], store_required: bool) -> List[Dict[str, Any]]:
    """
    Filtra estaciones por requisito de tienda.
    
    Args:
        estaciones: Lista de estaciones procesadas
        store_required: Si se requiere tienda
        
    Returns:
        Lista filtrada de estaciones
    """
    if not store_required:
        return estaciones
    
    return [est for est in estaciones if est.get('tiene_tienda', False)]


def apply_search_logic(estaciones: List[Dict[str, Any]], product: str, 
                      nearest: bool, cheapest: bool) -> Optional[Dict[str, Any]]:
    """
    Aplica la lógica de búsqueda según los criterios especificados.
    
    Args:
        estaciones: Lista de estaciones válidas
        product: Producto solicitado
        nearest: Si buscar la más cercana
        cheapest: Si buscar la más barata
        
    Returns:
        Estación que cumple los criterios o None si no hay resultados
    """
    if not estaciones:
        return None
    
    # Los 4 casos de búsqueda implementados
    if nearest and cheapest:
        # Caso 4: más cercana con menor precio
        estaciones.sort(key=lambda x: x['distancia(lineal)'])
        cercanas = estaciones[:15]  # Top 15 más cercanas
        if cercanas:
            cercanas.sort(key=lambda x: x[f'precios{product}'])  # Entre esas, la más barata
            return cercanas[0]
    elif nearest:
        # Caso 1: más cercana
        estaciones.sort(key=lambda x: x['distancia(lineal)'])
        return estaciones[0]
    elif cheapest:
        # Caso 2: menor precio (sin filtro de distancia)
        estaciones.sort(key=lambda x: x[f'precios{product}'])
        return estaciones[0]
    else:
        # Sin criterios específicos, ordenar por distancia
        estaciones.sort(key=lambda x: x['distancia(lineal)'])
        return estaciones[0]
    
    return None


def build_error_response(message: str) -> Dict[str, str]:
    """
    Construye una respuesta de error estándar.
    
    Args:
        message: Mensaje de error
        
    Returns:
        Dict con el error
    """
    return {"error": message}


def validate_coordinates(lat: float, lng: float) -> bool:
    """
    Valida que las coordenadas estén en rangos válidos.
    
    Args:
        lat: Latitud
        lng: Longitud
        
    Returns:
        bool: True si son válidas
    """
    # Rango válido para Chile aproximadamente
    return (-56 <= lat <= -17) and (-109 <= lng <= -66)
