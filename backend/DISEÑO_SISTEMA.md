# Diseño del Sistema Multi-Agente de Supermercado

## 1. ARQUITECTURA GENERAL

### Agentes del Sistema
1. **Agente Comprador** (Goal-Based Agent)
2. **Agente Cajero** (Simple Reflex Agent)

### Comunicación
- **Canal de comunicación por sucursal**: Implementado mediante eventos y colas de mensajes
- **Comunicación directa agente-a-agente**: El comprador envía mensaje directamente al cajero específico usando su ID

---

## 2. AGENTE COMPRADOR (Goal-Based Agent)

### 2.1 PEAS del Agente Comprador

**Performance (Rendimiento)**
- Minimizar distancia recorrida
- Maximizar variedad de productos en la lista
- Cumplir exactamente con el presupuesto (o con margen de ±5%)
- Tiempo de recolección optimizado
- Comunicación exitosa con el cajero

**Environment (Entorno)**
- Mapa de la sucursal (grid con pasillos y estantes)
- Inventario de productos con precios y ubicaciones
- Múltiples cajeros en diferentes posiciones
- Vale con presupuesto específico
- Otros compradores (escalable para futuras versiones)

**Actuators (Actuadores)**
- Moverse en el mapa (arriba, abajo, izquierda, derecha)
- Recolectar producto en ubicación actual
- Enviar mensaje al cajero seleccionado
- Generar listas de compras
- Seleccionar cajero más cercano

**Sensors (Sensores)**
- Percibir posición actual en el mapa
- Leer inventario disponible
- Detectar ubicaciones de productos
- Identificar posiciones de cajeros
- Recibir vale con presupuesto
- Detectar confirmación del usuario sobre lista elegida

### 2.2 Arquitectura Interna del Agente Comprador

```
Estado Interno:
- posicion_actual: (fila, columna)
- vale_presupuesto: float
- lista_seleccionada: List[producto_id, cantidad]
- productos_recolectados: List[producto]
- objetivo_actual: str (planificar_listas | recolectar_productos | ir_a_cajero)
- estado: str (planificando | esperando_usuario | recolectando | en_caja)
```

### 2.3 Algoritmos de Búsqueda del Agente Comprador

#### A. Planificación de Listas de Compras
**Algoritmo: Temple Simulado (Simulated Annealing)**

*Justificación:*
- Problema de optimización combinatoria (selección de productos + cantidades)
- Espacio de soluciones muy grande (combinaciones de productos)
- Necesita escapar de óptimos locales
- Tres objetivos simultáneos (variedad, presupuesto, no repetición)

*Función de Costo:*
```python
costo = w1 * |total - presupuesto|^2 +
        w2 * penalizacion_repeticion +
        w3 * penalizacion_baja_variedad +
        w4 * bonus_categorias_diversas
```

*Estados:*
- Estado: Lista de tuplas [(producto_id, cantidad)]
- Vecindad: Agregar/quitar producto, cambiar cantidad

*Enfriamiento:*
- Temperatura inicial: 1000
- Factor de enfriamiento: 0.95
- Criterio de parada: temperatura < 1.0 o sin mejoras en 50 iteraciones

#### B. Navegación en el Mapa (Recolección de Productos)
**Algoritmo: A* (A-Estrella)**

*Justificación:*
- Encuentra el camino óptimo garantizado
- Eficiente para mapas de tamaño mediano
- Heurística admisible (distancia Manhattan/Euclidiana)
- Apropiado para grid de supermercado

*Heurística:*
```python
h(n) = distancia_manhattan(n, objetivo)
     = |fila_n - fila_objetivo| + |col_n - col_objetivo|
```

*Costo:*
```python
g(n) = distancia_real_desde_inicio(n)
f(n) = g(n) + h(n)
```

#### C. Selección de Cajero Más Cercano
**Algoritmo: Búsqueda de Costo Uniforme (Dijkstra)**

*Justificación:*
- Encontrar cajero más cercano desde posición actual
- No necesita heurística (objetivo no conocido de antemano)
- Expande nodos por costo creciente

*Implementación:*
- Ejecutar desde posición actual del comprador
- Detener cuando se encuentra el primer cajero
- Retornar camino más corto

### 2.4 Planificación del Agente Comprador

**Tipo: Planificación Clásica (STRIPS-like)**

*Estados:*
- `en_entrada`: Comprador está en la entrada
- `tiene_lista_X`: Comprador tiene lista de tipo X (exacta/superior/inferior)
- `en_posicion(x,y)`: Comprador está en coordenada (x,y)
- `producto_recolectado(P)`: Producto P ha sido recolectado
- `todos_productos_recolectados`: Todos los productos de la lista están recolectados
- `en_cajero(C)`: Comprador está en el cajero C

*Acciones:*
```
Acción: GENERAR_LISTAS
  Precondición: en_entrada ∧ tiene_vale(presupuesto)
  Efecto: tiene_lista_exacta ∧ tiene_lista_superior ∧ tiene_lista_inferior

Acción: SELECCIONAR_LISTA(tipo)
  Precondición: tiene_lista_{tipo} ∧ usuario_eligió(tipo)
  Efecto: lista_activa(tipo)

Acción: MOVERSE(origen, destino)
  Precondición: en_posicion(origen) ∧ adyacente(origen, destino) ∧ no_obstaculo(destino)
  Efecto: ¬en_posicion(origen) ∧ en_posicion(destino)

Acción: RECOLECTAR_PRODUCTO(P, ubicacion)
  Precondición: en_posicion(ubicacion) ∧ producto_en(P, ubicacion) ∧ en_lista(P)
  Efecto: producto_recolectado(P)

Acción: COMUNICAR_CON_CAJERO(C)
  Precondición: en_cajero(C) ∧ todos_productos_recolectados
  Efecto: pedido_procesado ∧ objetivo_cumplido
```

*Objetivo:*
```
objetivo_cumplido = todos_productos_recolectados ∧ 
                    ∃C: en_cajero(C) ∧ pedido_procesado
```

*Plan de Ejecución:*
1. GENERAR_LISTAS
2. Esperar SELECCIONAR_LISTA(tipo) → entrada del usuario
3. Para cada producto P en lista:
   - Calcular ruta con A* hasta ubicación(P)
   - Ejecutar secuencia de MOVERSE hasta ubicación(P)
   - RECOLECTAR_PRODUCTO(P)
4. Buscar cajero más cercano con Búsqueda de Costo Uniforme
5. Ejecutar secuencia de MOVERSE hasta cajero(C)
6. COMUNICAR_CON_CAJERO(C)

---

## 3. AGENTE CAJERO (Simple Reflex Agent)

### 3.1 PEAS del Agente Cajero

**Performance (Rendimiento)**
- Procesar pedidos correctamente
- Validar todos los productos
- Generar facturas precisas
- Tiempo de respuesta rápido
- Disponibilidad para atender

**Environment (Entorno)**
- Canal de comunicación de la sucursal
- Inventario de precios de productos
- Cola de mensajes de compradores
- Identificador único del cajero

**Actuators (Actuadores)**
- Escuchar mensajes del canal
- Validar productos
- Calcular totales
- Generar factura
- Enviar respuesta al comprador

**Sensors (Sensores)**
- Detector de mensajes dirigidos a su ID
- Lector de lista de productos recibida
- Verificador de disponibilidad de productos

### 3.2 Arquitectura Interna del Agente Cajero

```
Estado Interno:
- cajero_id: str
- sucursal_id: str
- posicion: (fila, columna)
- estado: str (disponible | procesando)
- inventario_precios: Dict[producto_id, precio]
```

### 3.3 Tabla REAS (Reglas Condición-Acción)

| **Percepción** | **Acción** |
|----------------|------------|
| `mensaje_recibido(cajero_id=self.id)` ∧ `estado=disponible` | `cambiar_estado(procesando)` → `procesar_pedido()` |
| `mensaje_recibido(cajero_id≠self.id)` | `ignorar_mensaje()` |
| `estado=procesando` ∧ `lista_productos_valida` | `calcular_total()` → `generar_factura()` |
| `estado=procesando` ∧ `producto_no_existe` | `generar_error("Producto no encontrado")` |
| `estado=procesando` ∧ `factura_generada` | `enviar_respuesta()` → `cambiar_estado(disponible)` |
| `sin_mensajes` ∧ `estado=disponible` | `esperar()` |

### 3.4 Algoritmo de Procesamiento

```python
while True:
    percepcion = escuchar_canal()
    
    if mensaje_es_para_mi(percepcion):
        estado = "procesando"
        productos = extraer_productos(percepcion)
        
        factura = {
            "cajero_id": self.id,
            "items": [],
            "total": 0
        }
        
        for producto in productos:
            if producto.id in inventario:
                precio = inventario[producto.id]
                subtotal = precio * producto.cantidad
                factura["items"].append({
                    "producto": producto.nombre,
                    "cantidad": producto.cantidad,
                    "precio_unitario": precio,
                    "subtotal": subtotal
                })
                factura["total"] += subtotal
            else:
                generar_error("Producto no encontrado")
        
        enviar_factura(factura)
        estado = "disponible"
```

---

## 4. SISTEMA DE COMUNICACIÓN ENTRE AGENTES

### 4.1 Arquitectura de Canales

```python
class CanalComunicacion:
    def __init__(self, sucursal_id):
        self.sucursal_id = sucursal_id
        self.mensajes = queue.Queue()
        self.cajeros_suscritos = {}
    
    def registrar_cajero(self, cajero_id, callback):
        """Cajero se registra para escuchar mensajes"""
        self.cajeros_suscritos[cajero_id] = callback
    
    def enviar_mensaje(self, cajero_id, mensaje):
        """Comprador envía mensaje a un cajero específico"""
        if cajero_id in self.cajeros_suscritos:
            self.cajeros_suscritos[cajero_id](mensaje)
```

### 4.2 Protocolo de Mensajes

**Mensaje de Comprador a Cajero:**
```json
{
  "tipo": "pedido_procesamiento",
  "comprador_id": "COMP001",
  "cajero_id": "CAJ001",
  "productos": [
    {
      "producto_id": 1,
      "nombre": "Leche Entera 1L",
      "cantidad": 2,
      "precio_esperado": 8.5
    }
  ],
  "timestamp": "2025-12-16T10:30:00"
}
```

**Respuesta de Cajero a Comprador:**
```json
{
  "tipo": "factura",
  "cajero_id": "CAJ001",
  "comprador_id": "COMP001",
  "items": [
    {
      "producto": "Leche Entera 1L",
      "cantidad": 2,
      "precio_unitario": 8.5,
      "subtotal": 17.0
    }
  ],
  "total": 17.0,
  "timestamp": "2025-12-16T10:30:15"
}
```

---

## 5. ESTRUCTURA DE DATOS

### 5.1 Inventario (Simplificado)

```json
{
  "sucursal_id": "SUC001",
  "nombre": "Hipermaxi - Circunvalación",
  "productos": [
    {
      "id": 1,
      "nombre": "Leche Entera 1L",
      "precio": 8.5,
      "categoria": "lacteos",
      "ubicacion": {
        "fila": 5,
        "columna": 5
      }
    }
  ]
}
```

**Cambios respecto al sistema anterior:**
- ❌ Eliminados: `importancia`, `cantidad_tipica`
- ✅ Mantenidos: `id`, `nombre`, `precio`, `categoria`
- ✅ Agregado: `ubicacion` (fila, columna)

### 5.2 Mapa

```json
{
  "sucursal_id": "SUC001",
  "dimensiones": {
    "filas": 20,
    "columnas": 30
  },
  "entrada": {
    "fila": 0,
    "columna": 15
  },
  "cajeros": [
    {
      "id": "CAJ001",
      "fila": 19,
      "columna": 10
    },
    {
      "id": "CAJ002",
      "fila": 19,
      "columna": 20
    }
  ],
  "obstaculos": [
    {"fila": 5, "columna": 10},
    {"fila": 5, "columna": 11}
  ],
  "zonas_productos": {
    "lacteos": {"fila": 5, "columna": 5}
  }
}
```

---

## 6. FLUJO GENERAL DEL SISTEMA

```
1. Usuario llega a sucursal con vale (presupuesto)
   ↓
2. Sistema instancia AgenteComprador(comprador_id, sucursal_id)
   ↓
3. Comprador ingresa a sucursal (carga mapa e inventario)
   ↓
4. Comprador genera 3 listas usando Temple Simulado:
   - Lista exacta (100% presupuesto)
   - Lista superior (100-105% presupuesto)
   - Lista inferior (95-100% presupuesto)
   ↓
5. Sistema presenta listas al usuario
   ↓
6. Usuario selecciona una lista
   ↓
7. Comprador ejecuta planificación STRIPS:
   a. Para cada producto en lista:
      - Calcula ruta A* hasta producto
      - Se mueve y recolecta
   b. Busca cajero más cercano (Búsqueda de Costo Uniforme)
   c. Se mueve hasta cajero
   ↓
8. Comprador envía mensaje por canal a cajero específico
   ↓
9. Cajero (que está escuchando) detecta su ID en mensaje
   ↓
10. Cajero ejecuta REAS:
    - Procesa productos
    - Calcula total
    - Genera factura
    ↓
11. Cajero envía factura al comprador
    ↓
12. Sistema finaliza y presenta resultado al usuario
```

---

## 7. CONSIDERACIONES DE ESCALABILIDAD

### Independencia de Agentes
- ✅ Cada AgenteComprador puede operar en cualquier sucursal
- ✅ Cada AgenteCajero puede procesar cualquier pedido de su sucursal
- ✅ No hay acoplamiento entre agentes específicos

### Extensibilidad
- Agregar nuevas sucursales: Solo crear archivos de datos
- Agregar cajeros: Instanciar más AgenteCajero con ID único
- Agregar compradores concurrentes: Sistema de colas en canal
- Nuevos algoritmos: Módulo de algoritmos desacoplado

### Comunicación con Frontend
- API REST para operaciones CRUD
- WebSockets (Socket.IO) para comunicación en tiempo real
- Eventos para actualización de estado de agentes

---

## 8. ENDPOINTS API (Flask)

```
POST /api/comprador/crear
  Body: {comprador_id, sucursal_id, presupuesto}
  Response: {comprador_id, estado}

POST /api/comprador/generar-listas
  Body: {comprador_id}
  Response: {lista_exacta, lista_superior, lista_inferior}

POST /api/comprador/seleccionar-lista
  Body: {comprador_id, tipo_lista}
  Response: {lista_seleccionada}

POST /api/comprador/iniciar-recoleccion
  Body: {comprador_id}
  Response: {ruta_planificada, distancia_total}

GET /api/comprador/estado/{comprador_id}
  Response: {posicion, productos_recolectados, estado}

POST /api/cajero/crear
  Body: {cajero_id, sucursal_id, posicion}
  Response: {cajero_id, estado}

GET /api/sucursal/{sucursal_id}/estado
  Response: {compradores_activos, cajeros_activos, inventario}
```

---

## 9. COMPARACIÓN CON SISTEMA ANTERIOR

| Aspecto | Sistema Anterior | Sistema Nuevo |
|---------|------------------|---------------|
| Generación de listas | AgenteRecomendador (separado) | AgenteComprador (integrado) |
| Algoritmo de listas | Temple Simulado + importancia | Temple Simulado + variedad |
| Navegación | A* | A* (mantenido) |
| Selección cajero | No existía | Búsqueda de Costo Uniforme |
| Comunicación | Sistema centralizado | Agente-a-agente directo |
| Cajeros | No existían como agentes | AgenteCajero (Simple Reflex) |
| Inventario | importancia, cantidad_tipica | Sin esos campos |
| PEAS explícitos | No documentados | Completamente definidos |

---

## 10. TECNOLOGÍAS Y LIBRERÍAS

- **Backend:** Flask 3.0+
- **Comunicación:** Flask-SocketIO
- **CORS:** Flask-CORS
- **Datos:** JSON (archivos)
- **Estructuras:** heapq (cola de prioridad para A*)
- **Algoritmos:** math, random (Temple Simulado)

---

## Autor
Sistema diseñado para el proyecto de Inteligencia Artificial
Fecha: Diciembre 2025
