# 🎯 Resumen Ejecutivo del Proyecto

## Sistema Multi-Agente de Supermercado - Implementación Completa

### 📋 Descripción General

Sistema inteligente que implementa dos tipos de agentes autónomos para gestionar el proceso completo de compra en supermercados, desde la generación de listas optimizadas hasta la facturación.

---

## 🤖 Agentes Implementados

### 1. Agente Comprador (Goal-Based Agent)

**Tipo de Agente**: Basado en Objetivos

**PEAS**:
- **P**erformance: Minimizar distancia, maximizar variedad, cumplir presupuesto
- **E**nvironment: Mapa de sucursal, inventario, cajeros, vale
- **A**ctuators: Moverse, recolectar productos, enviar mensajes
- **S**ensors: Posición actual, inventario, ubicaciones, presupuesto

**Algoritmos Implementados**:
1. **Temple Simulado** - Generación de 3 listas de compras (exacta, superior, inferior)
2. **A*** - Navegación óptima por el mapa de la sucursal
3. **Búsqueda de Costo Uniforme** - Selección del cajero más cercano

**Planificación**: Clásica (STRIPS-like)
- Estados: posiciones, productos recolectados, objetivos
- Acciones: generar_listas, moverse, recolectar, comunicar
- Objetivo: productos_completos ∧ cajero_contactado ∧ factura_recibida

### 2. Agente Cajero (Simple Reflex Agent)

**Tipo de Agente**: Reflexivo Simple

**PEAS**:
- **P**erformance: Procesar pedidos correctamente, tiempo de respuesta rápido
- **E**nvironment: Canal de comunicación, inventario de precios, cola de mensajes
- **A**ctuators: Validar productos, calcular totales, generar facturas
- **S**ensors: Detector de mensajes con su ID, lector de lista de productos

**Tabla REAS**:
```
SI mensaje_para_mi ∧ disponible → procesar_pedido()
SI mensaje_para_otro → ignorar()
SI procesando ∧ productos_válidos → generar_factura()
SI factura_generada → enviar_respuesta() ∧ estado=disponible
```

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (Consumidor)                 │
│                     (API REST)                           │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│               SERVIDOR FLASK (app.py)                    │
│  - Gestión de agentes                                    │
│  - Endpoints API                                         │
│  - Coordinación general                                  │
└──────────────┬────────────────────────┬─────────────────┘
               │                        │
               ▼                        ▼
     ┌─────────────────┐      ┌─────────────────┐
     │ Agente Comprador│      │  Agente Cajero  │
     │  (Goal-Based)   │      │ (Simple Reflex) │
     └────────┬────────┘      └────────┬────────┘
              │                        │
              │    ┌──────────────────┐│
              └───►│ Canal de         ││
                   │ Comunicación     ││
                   │ (por sucursal)   ││
                   └──────────────────┘│
                          ▲             │
                          └─────────────┘
```

---

## 🔍 Algoritmos de Búsqueda Detallados

### Temple Simulado (Generación de Listas)

**Función de Costo**:
```
costo = w1 × (total - presupuesto)² +
        w2 × penalizacion_repeticion +
        w3 × penalizacion_baja_variedad +
        w4 × bonus_categorias
```

**Parámetros**:
- Temperatura inicial: 1000.0
- Factor enfriamiento: 0.95
- Temperatura mínima: 1.0
- Iteraciones por temperatura: 100

**Vecindad**: Agregar/quitar producto, aumentar/disminuir cantidad, reemplazar

### A* (Navegación)

**Función de Evaluación**:
```
f(n) = g(n) + h(n)
donde:
  g(n) = costo real desde inicio
  h(n) = distancia Manhattan al objetivo
```

**Heurística Admisible**: Distancia Manhattan nunca sobrestima el costo real

**Complejidad**: O(b^d) donde b es el factor de ramificación y d la profundidad

### Búsqueda de Costo Uniforme (Selección Cajero)

**Implementación**: Dijkstra con múltiples objetivos

**Criterio de parada**: Primer cajero encontrado = cajero más cercano

**Complejidad**: O(E log V) con cola de prioridad

---

## 📊 Características de las Listas Generadas

| Tipo Lista | Rango Presupuesto | Objetivo |
|------------|-------------------|----------|
| Exacta | 99.8% - 100.2% | Ajuste preciso al presupuesto |
| Superior | 100% - 105% | Ligeramente por encima |
| Inferior | 95% - 100% | Ligeramente por debajo |

**Optimización**:
- ✅ Maximiza variedad de productos
- ✅ Minimiza repetición (solo si necesario)
- ✅ Diversidad de categorías
- ✅ Ajuste al presupuesto

---

## 🔄 Flujo de Ejecución Completo

```
1. Usuario llega con vale (presupuesto)
   ↓
2. Sistema crea AgenteComprador
   ↓
3. Comprador ingresa a sucursal (carga mapa e inventario)
   ↓
4. Comprador genera 3 listas con Temple Simulado
   ↓
5. Usuario selecciona una lista
   ↓
6. Comprador planifica rutas con A*
   ↓
7. Comprador recolecta productos (ejecuta plan)
   ↓
8. Comprador busca cajero más cercano (Costo Uniforme)
   ↓
9. Comprador se mueve al cajero
   ↓
10. Comprador envía mensaje directo al cajero
    ↓
11. Cajero escucha mensaje (REAS)
    ↓
12. Cajero procesa productos (REAS)
    ↓
13. Cajero genera factura (REAS)
    ↓
14. Cajero envía factura al comprador
    ↓
15. Proceso completado ✅
```

---

## 🎯 Cumplimiento de Requisitos

### ✅ Requisitos Funcionales

| Requisito | Estado | Implementación |
|-----------|--------|----------------|
| Agente basado en objetivos | ✅ | AgenteComprador |
| Agente reflexivo simple | ✅ | AgenteCajero |
| Generación de 3 listas | ✅ | Temple Simulado |
| Navegación en mapa | ✅ | A* |
| Selección de cajero | ✅ | Búsqueda Costo Uniforme |
| Comunicación agente-a-agente | ✅ | CanalComunicacion |
| Independencia de agentes | ✅ | Arquitectura modular |
| API para frontend | ✅ | Flask REST API |

### ✅ Requisitos No Funcionales

- **Escalabilidad**: ✅ Múltiples compradores, cajeros y sucursales
- **Independencia**: ✅ Agentes funcionan en cualquier entorno
- **Extensibilidad**: ✅ Fácil agregar nuevas sucursales/algoritmos
- **Mantenibilidad**: ✅ Código modular y documentado

---

## 📁 Estructura de Archivos Generados

```
prop2/
├── DISEÑO_SISTEMA.md          # Diseño completo, PEAS, algoritmos
├── README.md                   # Documentación de usuario
├── QUICKSTART.md               # Guía de inicio rápido
├── RESUMEN_EJECUTIVO.md        # Este archivo
├── requirements.txt            # Dependencias Python
├── app.py                      # Servidor Flask principal
├── test_sistema.py             # Script de pruebas
│
├── models/
│   ├── __init__.py
│   ├── agente_comprador.py    # Agente goal-based (525 líneas)
│   └── agente_cajero.py       # Agente simple reflex (280 líneas)
│
├── utils/
│   ├── __init__.py
│   ├── algoritmos_busqueda.py # A*, Temple Simulado, Costo Uniforme (700 líneas)
│   └── canal_comunicacion.py  # Sistema de comunicación (200 líneas)
│
└── data/
    ├── inventario/
    │   ├── SUC001.json        # 35 productos
    │   └── SUC002.json        # 30 productos
    └── mapas/
        ├── SUC001.json        # 20x30 grid, 2 cajeros
        └── SUC002.json        # 25x35 grid, 3 cajeros
```

**Total**: ~2000 líneas de código + documentación completa

---

## 🚀 Instalación y Ejecución

### Instalación
```bash
cd prop2
pip install -r requirements.txt
```

### Ejecutar Servidor
```bash
python app.py
```

### Ejecutar Pruebas
```bash
python test_sistema.py
```

### Uso desde API
```bash
curl -X POST http://localhost:5000/api/comprador/proceso-completo \
  -H "Content-Type: application/json" \
  -d '{"comprador_id":"COMP001","sucursal_id":"SUC001","presupuesto":200.0,"tipo_lista":"exacta"}'
```

---

## 📈 Ventajas del Diseño

1. **Independencia de Agentes**: Cada agente funciona en cualquier entorno sin cambios
2. **Escalabilidad**: Fácil agregar más compradores, cajeros o sucursales
3. **Comunicación Real**: Agentes se comunican directamente (no mediada por sistema)
4. **Algoritmos Apropiados**: Cada tarea usa el algoritmo más adecuado
5. **Planificación Explícita**: STRIPS claramente definido para el comprador
6. **REAS Explícito**: Tabla de reglas clara para el cajero
7. **Extensibilidad**: Módulos independientes fáciles de modificar

---

## 🎓 Conceptos de IA Cubiertos

- ✅ Agentes racionales
- ✅ Arquitecturas de agentes (goal-based, reflex)
- ✅ PEAS (Performance, Environment, Actuators, Sensors)
- ✅ Búsqueda informada (A*, heurísticas)
- ✅ Búsqueda no informada (Costo Uniforme)
- ✅ Optimización (Temple Simulado)
- ✅ Planificación clásica (STRIPS)
- ✅ Sistemas multi-agente
- ✅ Comunicación entre agentes
- ✅ Tabla REAS (condición-acción)

---

## 📝 Diferencias con Sistema Anterior

| Aspecto | Sistema Anterior | Sistema Nuevo |
|---------|------------------|---------------|
| Generación listas | Agente separado | Integrado en comprador |
| Criterio listas | Importancia + cantidad típica | Variedad + presupuesto |
| Cajeros | No existían | Agentes autónomos |
| Comunicación | Mediada por sistema | Directa agente-a-agente |
| Inventario | Con importancia/cantidad_tipica | Solo precio/categoría |
| Documentación PEAS | No explícita | Completamente definida |

---

## 🏆 Resultado Final

Sistema multi-agente completo, funcional y escalable que implementa correctamente:

- ✅ 2 tipos de agentes (goal-based y simple reflex)
- ✅ 3 algoritmos de búsqueda distintos
- ✅ Planificación STRIPS
- ✅ Tabla REAS
- ✅ Comunicación agente-a-agente
- ✅ Backend Flask completo
- ✅ Documentación exhaustiva
- ✅ Scripts de prueba
- ✅ Listo para integración con frontend

---

**Proyecto desarrollado para Inteligencia Artificial - Diciembre 2025**
