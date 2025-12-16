import json
import os

def generar_mapa_suc002():
    """Ketal - Equipetrol (Mediano)"""
    obstaculos = []
    # 3 filas de estanterías con 4x4 cada una
    for fila_base in [3, 9, 15]:
        for col_base in [5, 13, 21, 29]:
            for i in range(4):
                for j in range(4):
                    obstaculos.append({"fila": fila_base + i, "columna": col_base + j})
    
    return {
        "sucursal_id": "SUC002",
        "nombre": "Ketal - Equipetrol",
        "dimensiones": {"filas": 25, "columnas": 35},
        "entrada": {"fila": 0, "columna": 17, "tipo": "entrada"},
        "cajeros": [
            {"id": "CAJ001", "fila": 24, "columna": 12},
            {"id": "CAJ002", "fila": 24, "columna": 17},
            {"id": "CAJ003", "fila": 24, "columna": 22}
        ],
        "obstaculos": obstaculos,
        "zonas_productos": {
            "lacteos": {"fila": 3, "columna": 4, "productos": [1, 5, 12, 13]},
            "panaderia": {"fila": 3, "columna": 10, "productos": [2]},
            "granos": {"fila": 3, "columna": 12, "productos": [3, 6, 22, 23]},
            "aceites": {"fila": 3, "columna": 18, "productos": [4]},
            "endulzantes": {"fila": 3, "columna": 20, "productos": [7]},
            "condimentos": {"fila": 3, "columna": 26, "productos": [8]},
            "limpieza": {"fila": 9, "columna": 4, "productos": [9]},
            "higiene": {"fila": 9, "columna": 10, "productos": [10, 11]},
            "frutas": {"fila": 9, "columna": 12, "productos": [14, 15]},
            "verduras": {"fila": 9, "columna": 18, "productos": [16, 17, 18]},
            "carnes": {"fila": 9, "columna": 20, "productos": [19, 20]},
            "pescados": {"fila": 9, "columna": 26, "productos": [21]},
            "bebidas": {"fila": 15, "columna": 4, "productos": [24, 25, 26]},
            "snacks": {"fila": 15, "columna": 10, "productos": [27, 28]},
            "conservas": {"fila": 15, "columna": 12, "productos": [29]},
            "salsas": {"fila": 15, "columna": 18, "productos": [30]}
        }
    }

def generar_mapa_suc003():
    """Fidalga - Las Brisas (Grande)"""
    obstaculos = []
    # 4 filas de estanterias con 5x3 cada una
    for fila_base in [3, 9, 15, 21]:
        for col_base in [5, 12, 19, 26, 33]:
            for i in range(5):
                for j in range(3):
                    obstaculos.append({"fila": fila_base + i, "columna": col_base + j})
    
    return {
        "sucursal_id": "SUC003",
        "nombre": "Fidalga - Las Brisas",
        "dimensiones": {"filas": 30, "columnas": 40},
        "entrada": {"fila": 0, "columna": 20, "tipo": "entrada"},
        "cajeros": [
            {"id": "CAJ001", "fila": 29, "columna": 14},
            {"id": "CAJ002", "fila": 29, "columna": 20},
            {"id": "CAJ003", "fila": 29, "columna": 26}
        ],
        "obstaculos": obstaculos,
        "zonas_productos": {
            "lacteos": {"fila": 3, "columna": 4, "productos": [1, 5, 12, 13]},
            "panaderia": {"fila": 3, "columna": 9, "productos": [2]},
            "granos": {"fila": 3, "columna": 11, "productos": [3, 6, 22, 23]},
            "aceites": {"fila": 3, "columna": 16, "productos": [4]},
            "endulzantes": {"fila": 3, "columna": 18, "productos": [7]},
            "condimentos": {"fila": 3, "columna": 23, "productos": [8]},
            "limpieza": {"fila": 9, "columna": 4, "productos": [9]},
            "higiene": {"fila": 9, "columna": 11, "productos": [10, 11]},
            "frutas": {"fila": 9, "columna": 16, "productos": [14, 15]},
            "verduras": {"fila": 9, "columna": 23, "productos": [16, 17, 18]},
            "carnes": {"fila": 15, "columna": 4, "productos": [19, 20]},
            "pescados": {"fila": 15, "columna": 11, "productos": [21]},
            "bebidas": {"fila": 15, "columna": 16, "productos": [24, 25, 26]},
            "snacks": {"fila": 15, "columna": 23, "productos": [27, 28]},
            "conservas": {"fila": 21, "columna": 4, "productos": [29]},
            "salsas": {"fila": 21, "columna": 11, "productos": [30]}
        }
    }

def generar_mapa_suc004():
    """IC Norte - Compacto"""
    obstaculos = []
    # 3 filas de estanterías compactas 3x3
    for fila_base in [3, 8, 13]:
        for col_base in [4, 10, 16]:
            for i in range(3):
                for j in range(3):
                    obstaculos.append({"fila": fila_base + i, "columna": col_base + j})
    
    return {
        "sucursal_id": "SUC004",
        "nombre": "IC Norte - Villa 1ro de Mayo",
        "dimensiones": {"filas": 20, "columnas": 25},
        "entrada": {"fila": 0, "columna": 12, "tipo": "entrada"},
        "cajeros": [
            {"id": "CAJ001", "fila": 19, "columna": 9},
            {"id": "CAJ002", "fila": 19, "columna": 15}
        ],
        "obstaculos": obstaculos,
        "zonas_productos": {
            "lacteos": {"fila": 3, "columna": 3, "productos": [1, 5, 12, 13]},
            "panaderia": {"fila": 3, "columna": 8, "productos": [2]},
            "granos": {"fila": 3, "columna": 9, "productos": [3, 6, 22, 23]},
            "aceites": {"fila": 3, "columna": 14, "productos": [4]},
            "endulzantes": {"fila": 3, "columna": 15, "productos": [7]},
            "condimentos": {"fila": 3, "columna": 20, "productos": [8]},
            "limpieza": {"fila": 8, "columna": 3, "productos": [9]},
            "higiene": {"fila": 8, "columna": 8, "productos": [10, 11]},
            "frutas": {"fila": 8, "columna": 14, "productos": [14, 15]},
            "verduras": {"fila": 8, "columna": 20, "productos": [16, 17, 18]},
            "carnes": {"fila": 13, "columna": 3, "productos": [19, 20]},
            "pescados": {"fila": 13, "columna": 8, "productos": [21]},
            "bebidas": {"fila": 13, "columna": 14, "productos": [24, 25, 26]},
            "snacks": {"fila": 13, "columna": 20, "productos": [27, 28]},
            "conservas": {"fila": 16, "columna": 8, "productos": [29]},
            "salsas": {"fila": 16, "columna": 14, "productos": [30]}
        }
    }

def generar_mapa_suc005():
    """Tía - Hipermercado"""
    obstaculos = []
    # 5 filas de estanterías grandes 6x4
    for fila_base in [3, 11, 19, 27]:
        for col_base in [5, 13, 21, 29, 37]:
            for i in range(6):
                for j in range(4):
                    obstaculos.append({"fila": fila_base + i, "columna": col_base + j})
    
    return {
        "sucursal_id": "SUC005",
        "nombre": "Tía - Monseñor Rivero",
        "dimensiones": {"filas": 35, "columnas": 45},
        "entrada": {"fila": 0, "columna": 22, "tipo": "entrada"},
        "cajeros": [
            {"id": "CAJ001", "fila": 34, "columna": 15},
            {"id": "CAJ002", "fila": 34, "columna": 22},
            {"id": "CAJ003", "fila": 34, "columna": 29},
            {"id": "CAJ004", "fila": 34, "columna": 36}
        ],
        "obstaculos": obstaculos,
        "zonas_productos": {
            "lacteos": {"fila": 3, "columna": 4, "productos": [1, 5, 12, 13]},
            "panaderia": {"fila": 3, "columna": 10, "productos": [2]},
            "granos": {"fila": 3, "columna": 12, "productos": [3, 6, 22, 23]},
            "aceites": {"fila": 3, "columna": 18, "productos": [4]},
            "endulzantes": {"fila": 3, "columna": 20, "productos": [7]},
            "condimentos": {"fila": 3, "columna": 26, "productos": [8]},
            "limpieza": {"fila": 11, "columna": 4, "productos": [9]},
            "higiene": {"fila": 11, "columna": 10, "productos": [10, 11]},
            "frutas": {"fila": 11, "columna": 18, "productos": [14, 15]},
            "verduras": {"fila": 11, "columna": 26, "productos": [16, 17, 18]},
            "carnes": {"fila": 19, "columna": 4, "productos": [19, 20]},
            "pescados": {"fila": 19, "columna": 12, "productos": [21]},
            "bebidas": {"fila": 19, "columna": 18, "productos": [24, 25, 26]},
            "snacks": {"fila": 19, "columna": 26, "productos": [27, 28]},
            "conservas": {"fila": 27, "columna": 4, "productos": [29]},
            "salsas": {"fila": 27, "columna": 12, "productos": [30]}
        }
    }

# Generar y guardar mapas
mapas = [
    generar_mapa_suc002(),
    generar_mapa_suc003(),
    generar_mapa_suc004(),
    generar_mapa_suc005()
]

for mapa in mapas:
    filename = f"data/mapas/{mapa['sucursal_id']}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(mapa, f, indent=2, ensure_ascii=False)
    print(f"✓ Generado: {filename}")

print("\n✓ Todos los mapas generados exitosamente!")
