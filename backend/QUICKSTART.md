# Guía de Inicio Rápido

## Instalación

1. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

## Ejecución

### 1. Iniciar el servidor

```bash
python app.py
```

El servidor estará disponible en `http://localhost:5000`

### 2. Ejecutar pruebas

En otra terminal:

```bash
python test_sistema.py
```

## Uso Rápido desde Python

```python
import requests

# Proceso completo de compra
response = requests.post("http://localhost:5000/api/comprador/proceso-completo", json={
    "comprador_id": "COMP001",
    "sucursal_id": "SUC001",
    "presupuesto": 200.0,
    "tipo_lista": "exacta"
})

resultado = response.json()
print(f"Total: {resultado['proceso']['factura']['total']} Bs.")
```

## Arquitectura

- **Agente Comprador**: Goal-Based Agent (Temple Simulado + A* + Búsqueda Costo Uniforme)
- **Agente Cajero**: Simple Reflex Agent (Tabla REAS)
- **Comunicación**: Canal directo agente-a-agente

## Documentación Completa

Ver [README.md](README.md) y [DISEÑO_SISTEMA.md](DISEÑO_SISTEMA.md)
