# 📁 Estructura Completa del Proyecto

```
prop2/
│
├── 📄 DISEÑO_SISTEMA.md              # ⭐ Diseño completo: PEAS, REAS, algoritmos
├── 📄 README.md                      # Documentación completa de usuario
├── 📄 RESUMEN_EJECUTIVO.md           # Vista ejecutiva del proyecto
├── 📄 GUIA_ESTUDIANTE.md             # ⭐ Guía para entender y presentar
├── 📄 QUICKSTART.md                  # Inicio rápido
├── 📄 ESTRUCTURA.md                  # Este archivo
│
├── 📄 requirements.txt               # Dependencias: Flask, Flask-CORS
├── 🐍 app.py                         # ⭐ Servidor Flask principal (300 líneas)
├── 🧪 test_sistema.py                # Script de pruebas (300 líneas)
│
├── 📁 models/                        # Agentes del sistema
│   ├── 📄 __init__.py
│   ├── 🤖 agente_comprador.py        # ⭐ Goal-Based Agent (525 líneas)
│   │   ├── Temple Simulado para listas
│   │   ├── A* para navegación
│   │   ├── Búsqueda Costo Uniforme para cajero
│   │   └── Planificación STRIPS
│   │
│   └── 🤖 agente_cajero.py           # ⭐ Simple Reflex Agent (280 líneas)
│       ├── Tabla REAS implementada
│       ├── Procesamiento de productos
│       └── Generación de facturas
│
├── 📁 utils/                         # Utilidades y algoritmos
│   ├── 📄 __init__.py
│   ├── 🔍 algoritmos_busqueda.py     # ⭐ A*, Temple Simulado, Costo Uniforme (700 líneas)
│   │   ├── Clase Nodo
│   │   ├── BusquedaAEstrella
│   │   ├── BusquedaCostoUniforme
│   │   └── TempleSimulado
│   │
│   └── 📡 canal_comunicacion.py      # Sistema de comunicación (200 líneas)
│       ├── CanalComunicacion
│       └── GestorCanales
│
└── 📁 data/                          # Datos de sucursales
    ├── 📁 inventario/                # Inventarios por sucursal
    │   ├── 📋 SUC001.json           # 35 productos (sin importancia/cantidad_tipica)
    │   └── 📋 SUC002.json           # 30 productos
    │
    └── 📁 mapas/                     # Mapas por sucursal
        ├── 🗺️  SUC001.json           # Grid 20x30, 2 cajeros, obstáculos
        └── 🗺️  SUC002.json           # Grid 25x35, 3 cajeros, obstáculos

```

---

## 📊 Métricas del Proyecto

### Líneas de Código

| Archivo | Líneas | Descripción |
|---------|--------|-------------|
| `agente_comprador.py` | 525 | Agente basado en objetivos |
| `algoritmos_busqueda.py` | 700 | A*, Temple Simulado, Costo Uniforme |
| `app.py` | 300 | Servidor Flask con API REST |
| `agente_cajero.py` | 280 | Agente reflexivo simple |
| `test_sistema.py` | 300 | Scripts de prueba |
| `canal_comunicacion.py` | 200 | Sistema de comunicación |
| **TOTAL CÓDIGO** | **~2300** | **Sin contar comentarios** |

### Documentación

| Archivo | Contenido |
|---------|-----------|
| `DISEÑO_SISTEMA.md` | Teoría completa: PEAS, REAS, algoritmos, planificación |
| `README.md` | Manual de usuario y API |
| `GUIA_ESTUDIANTE.md` | Guía para entender y presentar el proyecto |
| `RESUMEN_EJECUTIVO.md` | Vista ejecutiva del sistema |
| `QUICKSTART.md` | Inicio rápido |
| **TOTAL DOCUMENTACIÓN** | **~1500 líneas** |

---

## 🎯 Componentes Principales

### 1. Agente Comprador (`models/agente_comprador.py`)

**Responsabilidades:**
- ✅ Generar 3 listas de compras optimizadas
- ✅ Navegar por el mapa de la sucursal
- ✅ Recolectar productos de la lista
- ✅ Buscar y comunicarse con cajero

**Algoritmos:**
- Temple Simulado (generación de listas)
- A* (navegación)
- Búsqueda de Costo Uniforme (selección de cajero)

**Métodos principales:**
```python
ingresar_a_sucursal()          # Ingresa y carga datos
generar_listas_compras()       # Temple Simulado
seleccionar_lista()            # Usuario elige
iniciar_recoleccion()          # Planifica con A*
ejecutar_recoleccion()         # Ejecuta el plan
buscar_cajero_mas_cercano()    # Costo Uniforme
comunicar_con_cajero()         # Envía mensaje
```

### 2. Agente Cajero (`models/agente_cajero.py`)

**Responsabilidades:**
- ✅ Escuchar mensajes del canal
- ✅ Detectar mensajes dirigidos a su ID
- ✅ Procesar lista de productos
- ✅ Generar y enviar factura

**Arquitectura:**
- Tabla REAS (Reglas Condición-Acción)
- Estado mínimo (disponible/procesando)

**Métodos principales:**
```python
escuchar_mensaje()       # Sensor principal + REAS
_mensaje_es_para_mi()    # Condición REAS
_procesar_pedido()       # Acción REAS
_generar_factura()       # Acción REAS
```

### 3. Algoritmos (`utils/algoritmos_busqueda.py`)

**Clases implementadas:**

1. **BusquedaAEstrella**
   - Búsqueda informada
   - Heurística Manhattan/Euclidiana
   - Encuentra camino óptimo

2. **BusquedaCostoUniforme**
   - Búsqueda no informada
   - Dijkstra con múltiples objetivos
   - Para encontrar cajero más cercano

3. **TempleSimulado**
   - Optimización estocástica
   - Para generar listas de compras
   - Función de costo multi-objetivo

### 4. Sistema de Comunicación (`utils/canal_comunicacion.py`)

**Clases:**

1. **CanalComunicacion**
   - Un canal por sucursal
   - Registra cajeros y compradores
   - Media mensajes directos

2. **GestorCanales**
   - Gestor global de todos los canales
   - Estadísticas del sistema
   - Singleton para toda la app

### 5. Servidor Flask (`app.py`)

**Endpoints implementados:**

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Información del sistema |
| GET | `/api/estado` | Estado general |
| POST | `/api/comprador/crear` | Crear comprador |
| POST | `/api/comprador/generar-listas` | Generar listas |
| POST | `/api/comprador/seleccionar-lista` | Seleccionar lista |
| POST | `/api/comprador/iniciar-recoleccion` | Recolectar productos |
| POST | `/api/comprador/ir-a-cajero` | Buscar cajero |
| POST | `/api/comprador/comunicar-cajero` | Procesar compra |
| POST | `/api/comprador/proceso-completo` | Todo en uno |
| GET | `/api/comprador/estado/{id}` | Estado comprador |
| GET | `/api/cajero/estado/{suc}/{id}` | Estado cajero |
| GET | `/api/sucursal/{id}/estado` | Estado sucursal |

---

## 📦 Datos del Sistema

### Inventarios

**SUC001** (Hipermaxi - Circunvalación)
- 35 productos
- Categorías: lacteos, panaderia, granos, aceites, condimentos, limpieza, higiene, frutas, verduras, carnes, bebidas, snacks, conservas, salsas
- Precios: 3.5 Bs - 45.0 Bs

**SUC002** (Ketal - Equipetrol)
- 30 productos  
- Categorías: lacteos, panaderia, granos, aceites, condimentos, limpieza, higiene, frutas, verduras, carnes, pescados, bebidas, snacks, conservas, salsas
- Precios: 4.5 Bs - 65.0 Bs

### Mapas

**SUC001**
- Dimensiones: 20x30
- Cajeros: 2 (CAJ001, CAJ002)
- Obstáculos: 12 posiciones bloqueadas
- Zonas: 15 zonas de productos

**SUC002**
- Dimensiones: 25x35
- Cajeros: 3 (CAJ001, CAJ002, CAJ003)
- Obstáculos: 20 posiciones bloqueadas
- Zonas: 16 zonas de productos

---

## 🔄 Flujo de Datos

```
┌──────────────┐
│   Frontend   │
│  (Cliente)   │
└──────┬───────┘
       │ HTTP POST/GET
       ▼
┌─────────────────────────────────────────┐
│         Servidor Flask (app.py)         │
│  • Endpoints API                        │
│  • Gestión de agentes                   │
│  • Coordinación                         │
└──────┬─────────────────────┬────────────┘
       │                     │
       ▼                     ▼
┌──────────────────┐  ┌─────────────────┐
│ AgenteComprador  │  │  AgenteCajero   │
│                  │  │                 │
│ • Temple Sim.    │  │ • Tabla REAS    │
│ • A*             │  │ • Validación    │
│ • Costo Unif.    │  │ • Facturación   │
└────────┬─────────┘  └────────┬────────┘
         │                     │
         │  ┌─────────────────┐│
         └─►│ Canal de        ││
            │ Comunicación    ││
            │ (por sucursal)  ││
            └─────────────────┘│
                    ▲           │
                    └───────────┘
                    Mensaje directo
                    agente-a-agente
```

---

## 🧠 Conceptos de IA Implementados

### Tipos de Agentes
- ✅ **Goal-Based Agent** (Comprador)
  - Mantiene estado interno
  - Planifica acciones futuras
  - Persigue objetivos

- ✅ **Simple Reflex Agent** (Cajero)
  - Reacciona a percepciones
  - Sin memoria de largo plazo
  - Reglas condición-acción

### Algoritmos de Búsqueda

#### Búsqueda Informada
- ✅ **A*** - Navegación en mapa
  - f(n) = g(n) + h(n)
  - Heurística admisible
  - Óptimo y completo

#### Búsqueda No Informada
- ✅ **Costo Uniforme** - Selección de cajero
  - Dijkstra simplificado
  - Sin heurística
  - Expande por costo creciente

#### Optimización
- ✅ **Temple Simulado** - Generación de listas
  - Metaheurística estocástica
  - Escapa de óptimos locales
  - Enfriamiento gradual

### Planificación
- ✅ **STRIPS** (Comprador)
  - Estados discretos
  - Acciones con precondiciones/efectos
  - Objetivo definido

### Arquitectura de Agentes
- ✅ **PEAS** definidos explícitamente
- ✅ **REAS** implementado (Cajero)
- ✅ Comunicación multi-agente

---

## 🎓 Para Tu Defensa

### Preguntas que Podrían Hacerte

**1. ¿Por qué usaste Temple Simulado para las listas?**
- Optimización multi-objetivo
- Espacio de búsqueda muy grande
- Necesita escapar de óptimos locales
- Ver `GUIA_ESTUDIANTE.md` sección "Respuestas a Preguntas Probables"

**2. ¿Cómo funciona A*?**
- f(n) = g(n) + h(n)
- g(n) = costo real desde inicio
- h(n) = estimación heurística al objetivo
- Ver `DISEÑO_SISTEMA.md` sección 2.3.B

**3. ¿Qué es la tabla REAS?**
- Reglas: SI percepción ENTONCES acción
- Implementada en el cajero
- Ver `DISEÑO_SISTEMA.md` sección 3.3

**4. ¿Cómo se comunican los agentes?**
- Canal por sucursal
- Mensaje directo comprador → cajero específico
- Sin intermediación del sistema
- Ver `DISEÑO_SISTEMA.md` sección 4

**5. ¿Qué es STRIPS?**
- Sistema de planificación clásica
- Estados + Acciones + Objetivo
- Ver `DISEÑO_SISTEMA.md` sección 2.4

---

## 📚 Referencias de Código

### Archivo Principal de Cada Concepto

| Concepto | Archivo | Línea |
|----------|---------|-------|
| Temple Simulado | `utils/algoritmos_busqueda.py` | ~300-700 |
| A* | `utils/algoritmos_busqueda.py` | ~30-200 |
| Costo Uniforme | `utils/algoritmos_busqueda.py` | ~210-290 |
| Goal-Based Agent | `models/agente_comprador.py` | Todo el archivo |
| Simple Reflex | `models/agente_cajero.py` | ~85-150 |
| REAS | `models/agente_cajero.py` | ~75-150 |
| Canal Comunicación | `utils/canal_comunicacion.py` | Todo el archivo |
| API REST | `app.py` | Todo el archivo |

---

## ✅ Checklist de Funcionalidades

### Agente Comprador
- [x] Ingresa a sucursal con vale
- [x] Carga mapa e inventario
- [x] Genera 3 listas de compras (Temple Simulado)
- [x] Usuario selecciona lista
- [x] Planifica rutas con A*
- [x] Recolecta productos
- [x] Busca cajero más cercano (Costo Uniforme)
- [x] Se mueve al cajero
- [x] Envía mensaje directo al cajero
- [x] Recibe factura

### Agente Cajero
- [x] Escucha canal de comunicación
- [x] Detecta mensajes con su ID
- [x] Ignora mensajes de otros
- [x] Procesa lista de productos
- [x] Valida productos contra inventario
- [x] Calcula totales
- [x] Genera factura
- [x] Envía factura al comprador
- [x] Vuelve a estado disponible

### Sistema General
- [x] Canal de comunicación por sucursal
- [x] Múltiples cajeros por sucursal
- [x] API REST completa
- [x] Proceso completo end-to-end
- [x] Scripts de prueba
- [x] Documentación exhaustiva
- [x] Independencia de agentes
- [x] Escalabilidad

---

**¡Proyecto 100% Completo y Funcional!** ✅

Todo el código está en `prop2/` y listo para usar.
