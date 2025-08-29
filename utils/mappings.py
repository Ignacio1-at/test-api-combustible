"""
Módulo de mapeos.
Contiene los mapeos de productos, compañías y tipos de tienda.
"""

# Mapeo de productos de combustible
PRODUCT_MAPPING = {
    "93": 1,
    "95": 7, 
    "97": 2,
    "diesel": 3,
    "kerosene": 4
}

# Mapeo completo de compañías chilenas basado en la API oficial
COMPANY_MAPPING = {
    5: "COPEC",
    4: "SHELL", 
    3: "TERPEL",
    2: "PETROBRAS",
    88: "ENEX",
    23: "ABASTIBLE",
    24: "LIPIGAS",
    151: "ARAMCO",
    10: "Sin Bandera",
    118: "SIN BANDERA",
    122: "GO!",
    25: "HN",
    15: "SESA",
    89: "ESTACION DE SERVICIO SANTA MARIA SPA",
    27: "APEX",
    28: "AUTOGASCO",
    33: "ATT",
    36: "COMERCIAL MAQUI",
    37: "SURENERGY",
    39: "PETROJAC",
    40: "SOCORRO",
    42: "SERVICENTRO LEAL",
    45: "SERVICENTROS RABALME",
    46: "SERVICENTRO SAN MIGUEL",
    47: "Rafael Letelier Yañez y Cia Ltda",
    48: "Combustibles Ortiz",
    51: "Coopeserau",
    52: "Combustible Alhue",
    53: "ECCO",
    54: "FACAZ",
    57: "DELPA",
    58: "BALTOLU",
    59: "CUSTOM SERVICE",
    64: "APM",
    65: "Combustibles J.L.T.",
    66: "Punto Sur",
    67: "Mimbral",
    69: "CNC COMBUSTIBLES",
    71: "JVL COMBUSTIBLES",
    72: "PETROCAMP",
    73: "REDSUR",
    75: "BULL ENERGY",
    76: "Del Solar",
    77: "NavCar Combustibles",
    78: "Aire",
    80: "Del Sol Combustibles",
    85: "Doña Lucina",
    90: "GASOLINERA MONTE AGUILA",
    91: "Speedway",
    92: "NEWEN",
    93: "PETROGAL",
    94: "FARCOM",
    96: "Transpetrol",
    97: "Servicentro Itata",
    99: "CKR",
    100: "Combustibles JSP",
    101: "Adquim",
    102: "Combustibles Josefita Spa",
    106: "SOLOGAR",
    107: "Ruta V45",
    110: "Dale Combustibles",
    113: "AGUESAN",
    116: "COMBUSTIBLES ANLOA",
    117: "ECOIL",
    119: "OIL BOX",
    120: "VIGU Ltda.",
    121: "Combustibles Nancagua SPA",
    123: "MODENA",
    125: "PETROSI",
    128: "GSP Combustibles",
    129: "COMERCIAL Y SERVICIOS MS",
    130: "MAMG COMBUSTIBLES",
    131: "GULF",
    132: "OASIS",
    136: "SERVITRUCK",
    137: "SIVORI COMBUSTIBLES",
    138: "ORANGE COMBUSTIBLES",
    139: "ALANDRA DIESEL",
    141: "Combustibles JRB",
    144: "Energy",
    145: "Petrowork",
    146: "COOPEUMO COMBUSTIBLES",
    147: "Servisur",
    148: "Petrosur",
    149: "Pegasur",
    150: "G.O.A.T",
    152: "Combustibles Santa María",
    153: "Groff",
    154: "Combustibles Sandoval",
    155: "FullEnergy",
    156: "BESPA",
    157: "Hola",
    158: "OKEY",
    159: "ESA",
    160: "JM-DIESEL",
    161: "Petrovic",
    162: "CES",
    163: "El Molino",
    164: "AMCO",
    165: "Gasolinera Makal",
    166: "Combustibles San Roque",
    167: "Infigas",
    168: "Lepe y Alamo",
    169: "Andes Combustibles",
    170: "WR FENIX",
    171: "Petrofull",
    172: "Go Abastible",
    173: "Combustibles B y C"
}

# Marcas principales que típicamente tienen tiendas de conveniencia
BRANDS_WITH_STORES = [5, 4, 3, 88, 2, 151]  # COPEC, SHELL, TERPEL, ENEX, PETROBRAS, ARAMCO

def get_product_id(product: str) -> int:
    """
    Obtiene el ID del producto basado en el nombre.
    
    Args:
        product: Nombre del producto ("93", "95", "97", "diesel", "kerosene")
        
    Returns:
        int: ID del producto o None si no es válido
    """
    return PRODUCT_MAPPING.get(product.lower() if product else "")

def get_company_name(company_id: int) -> str:
    """
    Obtiene el nombre de la compañía basado en el ID.
    
    Args:
        company_id: ID de la compañía
        
    Returns:
        str: Nombre de la compañía
    """
    return COMPANY_MAPPING.get(company_id, f"Compañía {company_id}")

def has_convenience_store(company_id: int) -> bool:
    """
    Determina si una compañía típicamente tiene tienda de conveniencia.
    
    Args:
        company_id: ID de la compañía
        
    Returns:
        bool: True si típicamente tiene tienda
    """
    return company_id in BRANDS_WITH_STORES

def get_store_info(company_id: int, company_name: str, comuna: str, station_id: str) -> dict:
    """
    Genera la información de tienda basada en la compañía.
    
    Args:
        company_id: ID de la compañía
        company_name: Nombre de la compañía
        comuna: Comuna de la estación
        station_id: ID de la estación
        
    Returns:
        dict: Información de la tienda o None si no tiene
    """
    if not has_convenience_store(company_id):
        return None
        
    # Mapeo real de tiendas según compañías chilenas
    if company_id == 5 or (company_name and "COPEC" in company_name):  # COPEC
        tipo_tienda = "Pronto"
        nombre_tienda = f"Pronto {comuna}"
    elif company_id == 4 or (company_name and "SHELL" in company_name):  # SHELL
        tipo_tienda = "Select"
        nombre_tienda = f"Select {comuna}"
    elif company_id == 3 or (company_name and "TERPEL" in company_name):  # TERPEL
        tipo_tienda = "Tienda Terpel"
        nombre_tienda = f"Tienda Terpel {comuna}"
    elif company_id == 88 or (company_name and "ENEX" in company_name):  # ENEX
        tipo_tienda = "Tienda ENEX"
        nombre_tienda = f"Tienda ENEX {comuna}"
    elif company_id == 2 or (company_name and "PETROBRAS" in company_name):  # PETROBRAS
        tipo_tienda = "Tienda Petrobras"
        nombre_tienda = f"Tienda Petrobras {comuna}"
    elif company_name and "ARAMCO" in company_name:  # ARAMCO
        tipo_tienda = "Select"
        nombre_tienda = f"Select {comuna}"
    else:
        # Para marcas independientes o menores que tienen tienda
        tipo_tienda = "Tienda Local"
        nombre_tienda = f"Tienda {comuna}"
    
    return {
        "codigo": station_id,
        "nombre": nombre_tienda,
        "tipo": tipo_tienda
    }

def validate_product(product: str) -> bool:
    """
    Valida si un producto es válido.
    
    Args:
        product: Nombre del producto
        
    Returns:
        bool: True si es válido
    """
    return product.lower() in PRODUCT_MAPPING if product else False

def get_valid_products() -> list:
    """
    Obtiene la lista de productos válidos.
    
    Returns:
        list: Lista de productos válidos
    """
    return list(PRODUCT_MAPPING.keys())
