from fastapi import FastAPI
from datetime import datetime
from services.fuel_service import FuelService

app = FastAPI(
    title="API de Estaciones de Combustible Chile",
    description="Mi API para buscar estaciones de combustible",
    version="1.0.0"
)

@app.get("/")
def inicio():
    service = FuelService()
    return {
        "mensaje": "Esta ready",
        "autor": "Ignacio Torres González",
        "test": service.test_connection()
    }

@app.get("/test")
def prueba():
    return {"status": "OK", "info": "Conexión ready"}

@app.get("/health")
def chequeo_salud():
    """Endpoint de monitoreo del estado de la aplicación"""
    service = FuelService()
    api_status = service.test_connection()
    
    return {
        "status": "healthy" if "ready" in api_status else "degraded",
        "timestamp": datetime.now().isoformat(),
        "api_externa": api_status,
        "version": "1.0.0",
        "uptime": "running"
    }

@app.get("/combustibles")
def obtener_combustibles():
    service = FuelService()
    data = service.get_combustibles()
    return {"datos": data, "fuente": "API real Bencina en Línea"}

@app.get("/estaciones")
def obtener_estaciones():
    service = FuelService()
    data = service.buscar_estaciones()
    return {"total_estaciones": len(data.get('data', [])), "muestra": data}

@app.get("/api/stations/search")
def search_stations(
    lat: float,
    lng: float,
    product: str,
    nearest: bool = False,
    store: bool = False,
    cheapest: bool = False
):
    service = FuelService()
    result = service.search_stations(lat, lng, product, nearest, store, cheapest)
    
    if isinstance(result, dict) and 'error' in result:
        return {"success": False, "error": result['error']}
    
    return {"success": True, "data": result}

@app.get("/debug/estacion")
def debug_estacion():
    service = FuelService()
    data = service.buscar_estaciones()
    
    if 'data' in data and len(data['data']) > 0:
        # Buscar específicamente la estación 42
        station_42 = None
        for station in data['data']:
            if station.get('id') == 42:
                station_42 = station
                break
        
        if station_42:
            return {
                "estacion_42": station_42,
                "servicios": station_42.get('servicios', []),
                "cantidad_servicios": len(station_42.get('servicios', [])),
                "estructura_servicio": station_42.get('servicios', [])[0] if station_42.get('servicios') else "Sin servicios"
            }
        else:
            return {"error": "Estación 42 no encontrada en búsqueda masiva"}
    return {"error": "No hay datos"}

@app.get("/debug/tiendas")
def debug_tiendas():
    service = FuelService()
    data = service.buscar_estaciones()
    
    if 'data' in data:
        # Buscar estaciones que podrían tener tienda
        estaciones_con_info = []
        for estacion in data['data'][:10]:  # Solo las primeras 10
            servicios = estacion.get('servicios', [])
            estaciones_con_info.append({
                "id": estacion.get('id'),
                "direccion": estacion.get('direccion'),
                "servicios": servicios,
                "total_servicios": len(servicios),
                "nombres_servicios": [s.get('nombre') for s in servicios if s.get('nombre')]
            })
        return {"estaciones": estaciones_con_info}
    return {"error": "No hay datos"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)