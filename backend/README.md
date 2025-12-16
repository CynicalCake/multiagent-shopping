# Sistema Multi-Agente de Supermercado

Sistema inteligente de compras en supermercados con agentes autónomos que colaboran para optimizar el proceso de compra.

## 🎯 Descripción

Este proyecto implementa un sistema multi-agente compuesto por:

- **Agente Comprador** (Goal-Based Agent): Genera listas de compras optimizadas, navega por la sucursal recolectando productos y se comunica con cajeros.
- **Agente Cajero** (Simple Reflex Agent): Procesa pedidos de compradores, valida productos y genera facturas.

## 🏗️ Arquitectura

### Agente Comprador
- **Tipo**: Agente Basado en Objetivos (Goal-Based)
- **Algoritmos**:
  - Temple Simulado: Generación de listas de compras optimizadas
  - A*: Navegación óptima por el mapa
  - Búsqueda de Costo Uniforme: Selección de cajero más cercano
- **Planificación**: STRIPS-like (clásica)

### Agente Cajero
- **Tipo**: Agente Reflexivo Simple (Simple Reflex)
- **Arquitectura**: Tabla REAS (Reglas Condición-Acción)
- **Función**: Procesamiento de pedidos y generación de facturas

### Comunicación
- Canal de comunicación por sucursal
- Comunicación directa agente-a-agente (comprador → cajero específico)

## 📁 Estructura del Proyecto

```
prop2/
├── app.py                      # Servidor Flask principal
├── requirements.txt            # Dependencias
├── models/
│   ├── agente_comprador.py    # Agente comprador (goal-based)
│   └── agente_cajero.py       # Agente cajero (simple reflex)
├── utils/
│   ├── algoritmos_busqueda.py # A*, Temple Simulado, Costo Uniforme
│   └── canal_comunicacion.py  # Sistema de comunicación entre agentes
└── data/
    ├── inventario/
    │   ├── SUC001.json        # Inventario sucursal 1
    │   └── SUC002.json        # Inventario sucursal 2
    └── mapas/
        ├── SUC001.json        # Mapa sucursal 1
        └── SUC002.json        # Mapa sucursal 2
```

## 🚀 Instalación

### 1. Crear entorno virtual (opcional pero recomendado)

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

## ▶️ Ejecución

### Iniciar el servidor

```bash
python app.py
```

El servidor estará disponible en: `http://localhost:5000`

## 📡 API Endpoints

### Información General

- `GET /` - Información del sistema
- `GET /api/estado` - Estado general del sistema

### Agente Comprador

#### Crear Comprador
```http
POST /api/comprador/crear
Content-Type: application/json

{
  "comprador_id": "COMP001",
  "sucursal_id": "SUC001",
  "presupuesto": 200.0
}
```

#### Generar Listas de Compras
```http
POST /api/comprador/generar-listas
Content-Type: application/json

{
  "comprador_id": "COMP001"
}
```

#### Seleccionar Lista
```http
POST /api/comprador/seleccionar-lista
Content-Type: application/json

{
  "comprador_id": "COMP001",
  "tipo_lista": "exacta"
}
```
Opciones: `"exacta"`, `"superior"`, `"inferior"`

#### Iniciar Recolección
```http
POST /api/comprador/iniciar-recoleccion
Content-Type: application/json

{
  "comprador_id": "COMP001"
}
```

#### Ir a Cajero
```http
POST /api/comprador/ir-a-cajero
Content-Type: application/json

{
  "comprador_id": "COMP001"
}
```

#### Comunicar con Cajero
```http
POST /api/comprador/comunicar-cajero
Content-Type: application/json

{
  "comprador_id": "COMP001",
  "cajero_id": "CAJ001"
}
```

#### Proceso Completo (Todo en Uno)
```http
POST /api/comprador/proceso-completo
Content-Type: application/json

{
  "comprador_id": "COMP001",
  "sucursal_id": "SUC001",
  "presupuesto": 200.0,
  "tipo_lista": "exacta"
}
```

#### Estado del Comprador
```http
GET /api/comprador/estado/{comprador_id}
```

### Agente Cajero

#### Estado del Cajero
```http
GET /api/cajero/estado/{sucursal_id}/{cajero_id}
```

### Sucursal

#### Estado de Sucursal
```http
GET /api/sucursal/{sucursal_id}/estado
```

## 🧪 Ejemplo de Uso (Python)

```python
import requests

BASE_URL = "http://localhost:5000"

# Proceso completo de compra
response = requests.post(f"{BASE_URL}/api/comprador/proceso-completo", json={
    "comprador_id": "COMP001",
    "sucursal_id": "SUC001",
    "presupuesto": 200.0,
    "tipo_lista": "exacta"
})

resultado = response.json()
print(f"Total facturado: {resultado['proceso']['factura']['total']} Bs.")
print(f"Distancia recorrida: {resultado['proceso']['recoleccion']['distancia']} pasos")
```

## 📊 Ejemplo de Flujo Paso a Paso

```python
import requests

BASE_URL = "http://localhost:5000"

# 1. Crear comprador
requests.post(f"{BASE_URL}/api/comprador/crear", json={
    "comprador_id": "COMP001",
    "sucursal_id": "SUC001",
    "presupuesto": 200.0
})

# 2. Generar listas
listas = requests.post(f"{BASE_URL}/api/comprador/generar-listas", json={
    "comprador_id": "COMP001"
}).json()

# Ver listas generadas
print("Lista exacta:", listas['listas']['lista_exacta']['total'])
print("Lista superior:", listas['listas']['lista_superior']['total'])
print("Lista inferior:", listas['listas']['lista_inferior']['total'])

# 3. Seleccionar lista
requests.post(f"{BASE_URL}/api/comprador/seleccionar-lista", json={
    "comprador_id": "COMP001",
    "tipo_lista": "exacta"
})

# 4. Recolectar productos
recoleccion = requests.post(f"{BASE_URL}/api/comprador/iniciar-recoleccion", json={
    "comprador_id": "COMP001"
}).json()

print(f"Productos recolectados: {len(recoleccion['resultado']['productos_recolectados'])}")

# 5. Ir a cajero
cajero_info = requests.post(f"{BASE_URL}/api/comprador/ir-a-cajero", json={
    "comprador_id": "COMP001"
}).json()

cajero_id = cajero_info['cajero']['cajero']['id']

# 6. Comunicar con cajero y obtener factura
factura = requests.post(f"{BASE_URL}/api/comprador/comunicar-cajero", json={
    "comprador_id": "COMP001",
    "cajero_id": cajero_id
}).json()

print(f"Total facturado: {factura['factura']['total']} Bs.")
```

## 🔬 Características Técnicas

### Algoritmos de Búsqueda

#### Temple Simulado (Simulated Annealing)
- **Uso**: Generación de listas de compras
- **Función objetivo**: Minimizar diferencia con presupuesto + maximizar variedad
- **Parámetros**:
  - Temperatura inicial: 1000.0
  - Factor de enfriamiento: 0.95
  - Temperatura mínima: 1.0

#### A* (A-Star)
- **Uso**: Navegación en el mapa
- **Heurística**: Distancia Manhattan
- **Garantía**: Encuentra el camino óptimo

#### Búsqueda de Costo Uniforme
- **Uso**: Encontrar cajero más cercano
- **Implementación**: Dijkstra con múltiples objetivos

### PEAS de los Agentes

Ver documentación completa en: [DISEÑO_SISTEMA.md](DISEÑO_SISTEMA.md)

## 🎓 Conceptos de IA Implementados

- ✅ Agentes basados en objetivos (Goal-Based)
- ✅ Agentes reflexivos simples (Simple Reflex)
- ✅ Planificación clásica (STRIPS)
- ✅ Búsqueda informada (A*, Heurísticas)
- ✅ Búsqueda no informada (Costo Uniforme)
- ✅ Optimización (Temple Simulado)
- ✅ Comunicación entre agentes
- ✅ Arquitectura PEAS
- ✅ Tabla REAS

## 📈 Escalabilidad

El sistema está diseñado para ser escalable:

- ✅ Múltiples compradores simultáneos
- ✅ Múltiples cajeros por sucursal
- ✅ Múltiples sucursales
- ✅ Agentes independientes del entorno
- ✅ Canales de comunicación por sucursal

## 🛠️ Desarrollo

### Agregar Nueva Sucursal

1. Crear `data/inventario/SUC00X.json`
2. Crear `data/mapas/SUC00X.json`
3. Agregar cajeros en `app.py` → `inicializar_cajeros()`

### Modificar Algoritmos

Los algoritmos están en `utils/algoritmos_busqueda.py` y son completamente independientes, facilitando modificaciones.

## 📚 Documentación Adicional

- [DISEÑO_SISTEMA.md](DISEÑO_SISTEMA.md) - Diseño completo del sistema, PEAS, algoritmos y planificación

## 👨‍💻 Autor

Proyecto desarrollado para la materia de Inteligencia Artificial - Diciembre 2025

## 📄 Licencia

Este proyecto es parte de un proyecto académico.

Tengo todo este proyecto de un backend para un sistema de agentes para compras en sucursales de supermercado. Está hecho en Python con Flask y con WebSocket para comunicación en tiempo real.

La cosa es que necesito un frontend para la interfaz de este proyecto. Que esté hecha en Next.js. Debe poder mostrar tanto una sección para el agente comprador (que, como verás, sigue mapas de cuadrículas en formato JSON, eso debe ser visible, además de los pasos que da este agente, si es posible con animaciones y que quede claro todo) como para el agente recomendador (es un agente que lee el inventario de la sucursal a la que fue asignado y da algunas recomendaciones basadas en el presupuesto del agente comprador).

El flujo debe ser el siguiente:
- El usuario tiene la pantalla principal para escoger una sucursal
- El usuario escoge una sucursal
- El agente comprador llega a esa sucursal
- El agente comprador pide el presupuesto para el vale
- El usuario debe poder elegir la lista de productos que quiera
- El agente comprador recibe la lista que el usuario escogió
- El agente comprador inicia la compra de productos en esa sucursal
- El usuario puede ver todo en tiempo real, de preferencia fluido y con animaciones
- Luego de llenar la lista, el agente comprador debe dirigirse al cajero más cercano
- Cuando llegue al cajero más cercano, empezará a hacer la comunicación de los productos hacia el cajero
- El agente cajero debe recibir el mensaje y procesar las compras

Esta interfaz debe mostrar la comunicación que están teniendo el agente comprador con el agente cajero

No sé mucho sobre frontend, por eso necesitaré que el proyecto sea descargable e instalable sin muchos problemas en mi PC, con instrucciones de su instalación y cómo hacerlo correr. Hazlo todo en una carpeta aparte que se llame "frontend", para no mezlcar archivos con el backend.