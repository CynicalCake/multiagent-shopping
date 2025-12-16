# 📖 Guía para el Estudiante

## ¡Bienvenido a tu Sistema Multi-Agente! 🎉

Este documento te ayudará a entender y utilizar el sistema que he diseñado para tu proyecto.

---

## 🎯 ¿Qué tengo ahora?

Un sistema multi-agente **completamente funcional** con:

1. **Agente Comprador** (basado en objetivos) con:
   - Temple Simulado para generar 3 tipos de listas
   - A* para navegar por la sucursal
   - Búsqueda de Costo Uniforme para encontrar el cajero más cercano

2. **Agente Cajero** (reflexivo simple) con:
   - Tabla REAS implementada
   - Procesamiento de productos
   - Generación de facturas

3. **Sistema de Comunicación** agente-a-agente

4. **API REST completa** para que la consumas desde un frontend

---

## 📚 Archivos Importantes

### Para Entender el Sistema

1. **`DISEÑO_SISTEMA.md`** ⭐ MUY IMPORTANTE
   - Lee esto primero
   - Contiene toda la teoría: PEAS, REAS, algoritmos, planificación
   - Esto es lo que debes explicar en tu presentación

2. **`RESUMEN_EJECUTIVO.md`**
   - Vista rápida de todo el sistema
   - Perfecto para tu exposición

3. **`README.md`**
   - Cómo usar el sistema
   - Todos los endpoints de la API

### Para Usar el Sistema

4. **`QUICKSTART.md`**
   - Instalación rápida
   - Primeros pasos

5. **`test_sistema.py`**
   - Script para probar todo
   - Úsalo para demostrar que funciona

---

## 🚀 Primeros Pasos

### 1. Instalar

```bash
cd prop2
pip install -r requirements.txt
```

### 2. Ejecutar el servidor

```bash
python app.py
```

Deberías ver:
```
[Agente Cajero CAJ001] Inicializado en sucursal SUC001
[Agente Cajero CAJ002] Inicializado en sucursal SUC001
...
🚀 Servidor Flask iniciado
📡 Escuchando en http://localhost:5000
```

### 3. Probar el sistema

Abre otra terminal:

```bash
python test_sistema.py
```

Selecciona opción 1 (Prueba completa) y verás todo el proceso.

---

## 🎓 Para Tu Presentación/Defensa

### Conceptos Clave que Debes Dominar

#### 1. Agente Comprador (Goal-Based)

**¿Qué es un agente basado en objetivos?**
- No solo reacciona al entorno, sino que planifica para alcanzar objetivos
- Tiene un estado interno que mantiene
- Evalúa consecuencias futuras de sus acciones

**Explica el PEAS:**
- **Performance**: Distancia mínima, variedad máxima, presupuesto cumplido
- **Environment**: Mapa, inventario, cajeros
- **Actuators**: Moverse, recolectar, comunicar
- **Sensors**: Posición, productos disponibles, presupuesto

**Los 3 Algoritmos:**

1. **Temple Simulado** (para listas):
   - ¿Por qué? Problema de optimización combinatoria
   - Escapa de óptimos locales con probabilidad de aceptar soluciones peores
   - Temperatura baja → más "frío" → menos aventurado

2. **A*** (para navegación):
   - ¿Por qué? Encuentra el camino óptimo garantizado
   - f(n) = g(n) + h(n)
   - Heurística Manhattan es admisible

3. **Búsqueda de Costo Uniforme** (para cajero):
   - ¿Por qué? No sabemos cuál cajero es el objetivo, solo queremos el más cercano
   - Es Dijkstra pero se detiene al encontrar el primero

**Planificación STRIPS:**
- Estados: posiciones, productos recolectados
- Acciones: generar_listas, moverse, recolectar, comunicar
- Objetivo: completar compra + obtener factura

#### 2. Agente Cajero (Simple Reflex)

**¿Qué es un agente reflexivo simple?**
- Reacciona directamente a percepciones actuales
- No mantiene historial
- Reglas: SI percepción ENTONCES acción

**Explica la Tabla REAS:**
```
SI mensaje_es_para_mi Y estoy_disponible → procesar_pedido
SI mensaje_no_es_para_mi → ignorar
SI procesando Y productos_válidos → generar_factura
SI factura_generada → enviar + volver_a_disponible
```

**¿Por qué simple reflex para el cajero?**
- Su tarea es simple y repetitiva
- No necesita planificar a largo plazo
- Solo responde a lo que percibe ahora mismo

#### 3. Comunicación Agente-a-Agente

**¿Cómo funciona?**
- Cada sucursal tiene un canal
- Comprador envía mensaje al cajero específico (con su ID)
- Solo ese cajero lo escucha (tabla REAS: "si mensaje es para mí")
- No hay intermediario del sistema

**¿Por qué es importante?**
- Demuestra verdadera autonomía de agentes
- Los agentes colaboran directamente
- Escalable (muchos compradores → muchos cajeros)

---

## 💡 Respuestas a Preguntas Probables

### "¿Por qué Temple Simulado para las listas?"

Porque necesitamos optimizar múltiples objetivos simultáneamente:
1. Cumplir con presupuesto (exacto, ±5%)
2. Maximizar variedad de productos
3. Minimizar repeticiones
4. Diversificar categorías

Temple Simulado es perfecto para esto porque:
- Puede escapar de óptimos locales
- Explora el espacio de soluciones ampliamente
- El enfriamiento gradual refina la solución

### "¿Por qué A* y no otro algoritmo?"

A* es ideal porque:
- Encuentra el camino óptimo (importante para minimizar distancia)
- Es eficiente con una buena heurística
- La heurística Manhattan es perfecta para grids
- Garantiza optimalidad si la heurística es admisible

### "¿Qué es STRIPS exactamente?"

STRIPS es un sistema de planificación que define:
- **Estados**: Descripciones del mundo
- **Acciones**: Lo que el agente puede hacer (precondiciones + efectos)
- **Objetivo**: Estado que queremos alcanzar

Ejemplo en tu sistema:
```
Estado inicial: en_entrada, tiene_vale
Acción: generar_listas
  Precondición: tiene_vale
  Efecto: tiene_listas
Estado final: objetivo_cumplido (productos + factura)
```

### "¿Por qué el cajero es simple reflex y no goal-based?"

Porque su tarea es reactiva:
- No necesita planificar pasos futuros
- Solo responde al estímulo actual (mensaje)
- Su comportamiento es determinista y simple
- No tiene objetivos a largo plazo, solo procesar el pedido actual

---

## 🔍 Cómo Demostrar Tu Sistema

### Demostración en Vivo

1. **Inicia el servidor**
   ```bash
   python app.py
   ```
   Muestra los cajeros inicializándose

2. **Ejecuta test_sistema.py**
   ```bash
   python test_sistema.py
   ```
   Opción 1: Proceso completo

3. **Explica lo que está pasando:**
   - "El comprador ingresa con presupuesto de 150 Bs"
   - "Genera 3 listas con Temple Simulado"
   - "Selecciona la lista exacta"
   - "Navega con A* recolectando productos"
   - "Busca el cajero más cercano con Costo Uniforme"
   - "Se comunica directamente con el cajero"
   - "El cajero aplica su tabla REAS y genera factura"

### Usando la API

Muestra cómo un frontend consumiría tu backend:

```python
import requests

# Un frontend haría esto:
response = requests.post("http://localhost:5000/api/comprador/proceso-completo", 
    json={
        "comprador_id": "COMP001",
        "sucursal_id": "SUC001",
        "presupuesto": 200.0,
        "tipo_lista": "exacta"
    }
)

resultado = response.json()
print(f"Total: {resultado['proceso']['factura']['total']} Bs.")
```

---

## 📝 Estructura para tu Presentación

### 1. Introducción (2-3 min)
- Problema: Optimizar compras en supermercados
- Solución: Sistema multi-agente inteligente
- 2 agentes con roles diferentes

### 2. Agente Comprador (5-7 min)
- Tipo: Goal-Based Agent
- PEAS completo
- 3 algoritmos y por qué cada uno
- Planificación STRIPS
- Demo: Muestra generación de listas

### 3. Agente Cajero (3-4 min)
- Tipo: Simple Reflex Agent
- PEAS completo
- Tabla REAS
- Por qué simple reflex es apropiado
- Demo: Muestra procesamiento

### 4. Comunicación (2-3 min)
- Agente-a-agente directo
- Canal por sucursal
- Escalabilidad

### 5. Demostración Completa (3-5 min)
- Ejecuta proceso completo
- Muestra resultados
- Destaca características clave

### 6. Arquitectura y Conclusiones (2-3 min)
- Arquitectura modular
- Escalable y extensible
- Listo para frontend

---

## 🛠️ Si Quieres Modificar Algo

### Cambiar Parámetros de Temple Simulado

En `utils/algoritmos_busqueda.py`, línea ~360:

```python
self.temperatura_inicial = 1000.0  # Más alto = más exploración
self.factor_enfriamiento = 0.95     # Más bajo = enfriamiento más rápido
```

### Agregar Más Productos

Edita `data/inventario/SUC001.json` y agrega:

```json
{
  "id": 36,
  "nombre": "Nuevo Producto",
  "precio": 10.0,
  "categoria": "nueva_categoria"
}
```

Luego agrega su ubicación en `data/mapas/SUC001.json`.

### Cambiar el Mapa

En `data/mapas/SUC001.json`:
- `dimensiones`: Tamaño del grid
- `obstaculos`: Celdas bloqueadas
- `zonas_productos`: Dónde están los productos

---

## ⚠️ Posibles Problemas y Soluciones

### "No se encuentra el módulo X"
```bash
pip install -r requirements.txt
```

### "Puerto 5000 en uso"
Cierra otros servidores o cambia el puerto en `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Cambia a 5001
```

### "No se encuentra el archivo JSON"
Asegúrate de ejecutar desde el directorio `prop2`:
```bash
cd prop2
python app.py
```

---

## 📖 Para Profundizar

### Algoritmos de Búsqueda
- **Temple Simulado**: Russell & Norvig, Capítulo 4.1
- **A***: Russell & Norvig, Capítulo 3.5
- **Búsqueda de Costo Uniforme**: Russell & Norvig, Capítulo 3.4

### Agentes
- **Goal-Based Agents**: Russell & Norvig, Capítulo 2.4
- **Simple Reflex Agents**: Russell & Norvig, Capítulo 2.2
- **PEAS**: Russell & Norvig, Capítulo 2.3

### Planificación
- **STRIPS**: Russell & Norvig, Capítulo 10.1
- **Grafos de Planificación**: Russell & Norvig, Capítulo 10.3

---

## ✅ Checklist para tu Defensa

- [ ] Entiendo qué es un agente basado en objetivos
- [ ] Puedo explicar el PEAS del comprador
- [ ] Sé por qué usamos Temple Simulado, A* y Costo Uniforme
- [ ] Entiendo STRIPS y puedo dar ejemplos
- [ ] Entiendo qué es un agente reflexivo simple
- [ ] Puedo explicar la tabla REAS del cajero
- [ ] Sé cómo funciona la comunicación agente-a-agente
- [ ] Puedo ejecutar una demostración en vivo
- [ ] Conozco la estructura del proyecto
- [ ] Entiendo cómo un frontend consumiría la API

---

## 🎉 ¡Éxito en tu Proyecto!

Tienes un sistema completo, bien diseñado y documentado. Los conceptos están correctamente implementados y el código es de calidad profesional.

**Recuerda**: No solo implementaste código, implementaste un sistema multi-agente inteligente con fundamentos teóricos sólidos.

¡Buena suerte! 🚀

---

**Nota Final**: Si tienes dudas sobre algún concepto, consulta primero `DISEÑO_SISTEMA.md` donde está toda la teoría detallada.
