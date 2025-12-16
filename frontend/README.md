# Sistema Multi-Agente de Supermercado - Frontend

Interfaz web construida con Next.js para visualizar la simulación de agentes inteligentes en supermercados.

## Características

- **Visualización en tiempo real** del movimiento de agentes en mapas de cuadrícula
- **Selección de listas de compra** generadas con Temple Simulado
- **Animaciones fluidas** del proceso de compra
- **Registro de comunicación** entre agentes comprador y cajero
- **Interfaz responsiva** con Tailwind CSS

## Requisitos Previos

- Node.js 18.17 o superior
- Backend Flask ejecutándose en `http://localhost:5000`

## Instalación

1. Navegar a la carpeta del frontend:
```bash
cd frontend
```

2. Instalar dependencias:
```bash
npm install
```

3. Configurar la URL del backend (opcional):
Crear un archivo `.env.local` con:
```
NEXT_PUBLIC_API_URL=http://localhost:5000
```

## Ejecutar en Desarrollo

```bash
npm run dev
```

La aplicación estará disponible en `http://localhost:3000`

## Ejecutar el Sistema Completo

### Terminal 1 - Backend
```bash
cd .. # Volver a la raíz del proyecto
python app.py
```

### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```

## Estructura del Proyecto

```
frontend/
├── app/
│   ├── page.tsx                    # Página principal (selección de sucursal)
│   ├── simulation/[branchId]/
│   │   └── page.tsx               # Página de simulación
│   ├── layout.tsx                 # Layout principal
│   └── globals.css                # Estilos globales
├── components/
│   ├── grid-map.tsx               # Visualización del mapa de cuadrícula
│   ├── product-selection.tsx     # Selector de listas de productos
│   ├── agent-status.tsx          # Estado del agente
│   ├── communication-log.tsx     # Registro de comunicación
│   └── ui/                       # Componentes UI (shadcn/ui)
├── public/
│   └── maps/                     # Archivos JSON de mapas
│       ├── SUC001.json
│       └── SUC002.json
└── package.json
```

## Flujo de la Aplicación

1. **Selección de Sucursal**: El usuario elige una sucursal (SUC001 o SUC002)
2. **Configuración de Presupuesto**: Se ingresa el presupuesto para la compra
3. **Generación de Listas**: El agente genera 3 listas con Temple Simulado
4. **Selección de Lista**: El usuario elige una de las 3 listas
5. **Recolección**: El agente recorre el mapa usando A* para recolectar productos
6. **Búsqueda de Cajero**: Encuentra el cajero más cercano con Búsqueda de Costo Uniforme
7. **Procesamiento**: El cajero procesa la compra y genera la factura
8. **Completado**: Se muestra el resumen final de la compra

## Tecnologías Utilizadas

- **Next.js 15**: Framework React con App Router
- **TypeScript**: Tipado estático
- **Tailwind CSS v4**: Estilos utilitarios
- **shadcn/ui**: Componentes UI accesibles
- **Lucide React**: Iconos

## API del Backend

El frontend se comunica con estos endpoints del backend:

- `POST /api/comprador/crear` - Crear agente comprador
- `POST /api/comprador/generar-listas` - Generar listas de compra
- `POST /api/comprador/seleccionar-lista` - Seleccionar lista
- `POST /api/comprador/iniciar-recoleccion` - Iniciar recolección
- `POST /api/comprador/ir-a-cajero` - Ir al cajero
- `POST /api/comprador/comunicar-cajero` - Comunicar con cajero

## Personalización

### Cambiar colores del mapa

Editar `components/grid-map.tsx` en la función que asigna colores a las celdas:

```tsx
let fill = '#f9fafb'  // Color base
if (obstacle) fill = '#374151'  // Obstáculos
if (productZone) fill = '#fef3c7'  // Zonas de productos
if (cashier) fill = '#d1fae5'  // Cajeros
```

### Agregar nuevas sucursales

1. Agregar el JSON del mapa en `public/maps/SUC00X.json`
2. Agregar la sucursal al array en `app/page.tsx`:

```tsx
const branches = [
  // ... sucursales existentes
  {
    id: 'SUC003',
    name: 'Nueva Sucursal',
    dimensions: { rows: 30, cols: 40 },
    cashiers: 4,
    products: 40
  }
]
```

## Compilar para Producción

```bash
npm run build
npm start
```

## Solución de Problemas

### Error de conexión al backend

Verificar que:
- El backend Flask esté ejecutándose en `http://localhost:5000`
- CORS esté habilitado en el backend (ya configurado con `flask-cors`)
- La variable `NEXT_PUBLIC_API_URL` esté correctamente configurada

### El mapa no se carga

Verificar que los archivos JSON en `public/maps/` tengan el formato correcto y coincidan con el `branchId`.

### Animaciones no fluidas

Las animaciones dependen de las respuestas del backend. Asegurarse de que el backend responda rápidamente y no tenga errores.

## Contacto y Soporte

Para preguntas sobre el frontend, revisa la documentación del backend en el directorio raíz del proyecto.

---

Desarrollado con Next.js para el Sistema Multi-Agente de Supermercado
