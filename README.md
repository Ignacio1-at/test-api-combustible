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

#### 5. Buscar en Santiago (gasolina 97)
```bash
curl "http://localhost:8000/api/stations/search?lat=-33.45&lng=-70.65&product=97&nearest=true"
```

#### 6. Buscar en Valparaíso (diesel)
```bash
curl "http://localhost:8000/api/stations/search?lat=-33.03&lng=-71.62&product=diesel&nearest=true"
```

#### 7. Buscar en Concepción (gasolina 95 más barata)
```bash
curl "http://localhost:8000/api/stations/search?lat=-36.83&lng=-73.03&product=95&nearest=true&cheapest=true"
```

#### 8. Buscar estación específica ARAMCO en Iquique
```bash
curl "http://localhost:8000/api/stations/search?lat=-20.238&lng=-70.143&product=97&nearest=true"
```

#### 9. Buscar con kerosene en zona norte
```bash
curl "http://localhost:8000/api/stations/search?lat=-24.5&lng=-70.4&product=kerosene&nearest=true"
```

#### 10. Buscar solo estaciones con tienda (sin filtro de cercanía)
```bash
curl "http://localhost:8000/api/stations/search?lat=-33.45&lng=-70.65&product=93&store=true"
```

### Respuesta de Ejemplo

```json
{
  "success": true,
  "data": {
    "id": "1555",
    "compania": "COPEC",
    "direccion": "ARTURO PRAT 683",
    "comuna": "Santiago Centro",
    "region": "Metropolitana de Santiago",
    "latitud": -33.45374438281472,
    "longitud": -70.64860761165619,
    "distancia(lineal)": 0.44,
    "precios97": 1303,
    "tienda": {
      "codigo": "1555",
      "nombre": "Pronto Santiago Centro",
      "tipo": "Pronto"
    },
    "tiene_tienda": true
  }
}
```

## Estructura

```
mi_api_combustible/
├── main.py                    # FastAPI app principal
├── requirements.txt           # Dependencias
├── pytest.ini               # Config de tests
├── README.md                 # Documentación
├── services/                 # Servicios
│   ├── __init__.py
│   └── fuel_service.py      # Servicio principal
├── utils/                    # Utilidades modulares
│   ├── __init__.py
│   ├── distance.py          # Cálculos geográficos
│   ├── mappings.py          # Mapeos de datos
│   └── search_utils.py      # Lógica de búsqueda
└── tests/                    # Suite de tests
    ├── __init__.py
    ├── test_api.py          # Tests de endpoints
    └── test_services.py     # Tests de servicios y utilidades
```

## Dependencias

- FastAPI
- httpx  
- uvicorn

## Agregado nuevo

- ** Health Check**: `/health` - Monitoreo del estado de la app
- ** Variables de entorno**: Configuración externa via `.env`
- ** Tests unitarios**: Probando test con pytest

### Endpoints adicionales
- `GET /health` - Estado de la aplicación y API externa
- `GET /test` - Verificación rápida de funcionamiento

## Datos

Consume API real de https://api.bencinaenlinea.cl/api/ (CNE Chile).

La detección de tiendas usa la cantidad de servicios (≥2 = tiene tienda).

Distancias calculadas con fórmula Haversine en kilómetros.

## Documentación

Swagger UI: http://localhost:8000/docs

## Testing

Para ejecutar los tests unitarios:

```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar todos los tests
pytest tests/ -v

# Ejecutar tests específicos
pytest tests/test_api.py -v
pytest tests/test_services.py -v
```

### Cobertura de Tests
- Endpoints de la API
- Validación de parámetros
- Cálculo de distancias
- Manejo de errores
- Health check

## Config

El proyecto utiliza variables de entorno:

```env
API_BASE_URL=https://api.bencinaenlinea.cl/api
TIMEOUT_SECONDS=30
APP_NAME=API de Estaciones de Combustible Chile
APP_VERSION=1.0.0
DEBUG_MODE=false
```
```