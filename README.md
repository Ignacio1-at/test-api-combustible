```markdown
# API de Estaciones de Combustible Chile

API REST en Python/FastAPI que busca estaciones de combustible usando datos reales de Bencina en Línea (CNE).

## Instalación

```bash
git clone [repo]
cd mi_api_combustible
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

API disponible en: http://localhost:8000

## Uso

### Endpoint principal
```
GET /api/stations/search
```

**Parámetros:**
- `lat`, `lng` (requeridos): coordenadas
- `product` (requerido): `93`, `95`, `97`, `diesel`, `kerosene`
- `nearest`: buscar más cercana
- `store`: filtrar con tienda
- `cheapest`: ordenar por precio

### Ejemplos de Uso

#### 1. Estación más cercana por producto
```bash
curl "http://localhost:8000/api/stations/search?lat=-20.2&lng=-70.1&product=93&nearest=true"
```

#### 2. Estación más cercana con menor precio
```bash
curl "http://localhost:8000/api/stations/search?lat=-20.2&lng=-70.1&product=95&nearest=true&cheapest=true"
```

#### 3. Estación más cercana con tienda
```bash
curl "http://localhost:8000/api/stations/search?lat=-20.2&lng=-70.1&product=diesel&nearest=true&store=true"
```

#### 4. Estación más cercana con tienda y menor precio
```bash
curl "http://localhost:8000/api/stations/search?lat=-20.2&lng=-70.1&product=97&nearest=true&store=true&cheapest=true"
```

### Respuesta de Ejemplo

```json
{
  "success": true,
  "data": {
    "id": 47,
    "compania": 4,
    "direccion": "OHiggins 2280",
    "comuna": "Iquique",
    "region": "Tarapacá",
    "latitud": -20.219516041030868,
    "longitud": -70.13424038887024,
    "distancia": 4.18,
    "precio": 1307,
    "producto": "93",
    "tiene_tienda": true
  }
}
```

## Estructura

```
mi_api_combustible/
├── main.py                 # Aplicación principal FastAPI
├── requirements.txt        # Dependencias
├── services/
│   ├── __init__.py
│   └── fuel_service.py     # Lógica de negocio
├── utils/
│   ├── __init__.py
│   └── distance.py         # Cálculo de distancias
└── README.md              # Este archivo
```

## Dependencias

- FastAPI
- httpx  
- uvicorn

## Datos

Consume API real de https://api.bencinaenlinea.cl/api/ (CNE Chile).

La detección de tiendas usa la cantidad de servicios (≥2 = tiene tienda).

Distancias calculadas con fórmula Haversine en kilómetros.

## Documentación

Swagger UI: http://localhost:8000/docs
```