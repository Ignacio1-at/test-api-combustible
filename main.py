from fastapi import FastAPI
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
        # Mostrar solo la primera estación para ver la estructura
        primera_estacion = data['data'][0]
        return {
            "estructura": primera_estacion,
            "precios_disponibles": primera_estacion.get('Prices', []),
            "total_estaciones": len(data['data'])
        }
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