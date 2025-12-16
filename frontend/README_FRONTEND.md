# Frontend - Sistema de Agentes Inteligentes

Frontend desarrollado con Next.js para simular compras autónomas en supermercados usando agentes inteligentes.

## Tecnologías

- **Next.js 16** (con Turbopack)
- **React 19**
- **TypeScript**
- **Tailwind CSS**
- **shadcn/ui** - Componentes UI

## Instalación

### Requisitos Previos
- Node.js 18+ (recomendado 20+)
- pnpm (gestor de paquetes)

### Pasos

1. **Instalar dependencias:**
   ```bash
   pnpm install
   ```

2. **Configurar variables de entorno:**
   El archivo `.env.local` ya está configurado con:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:5000
   ```
   
   Ajusta esta URL si tu backend está en otro puerto.

3. **Iniciar el servidor de desarrollo:**
   ```bash
   pnpm dev
   ```

4. **Abrir en el navegador:**
   ```
   http://localhost:3000
   ```

## Estructura del Proyecto

```
frontend/
├── app/
│   ├── page.tsx              # Página inicial (selección de sucursal)
│   ├── layout.tsx            # Layout raíz
│   ├── globals.css           # Estilos globales
│   └── simulation/
│       └── [branchId]/
│           └── page.tsx      # Página de simulación
├── components/
│   ├── grid-map.tsx          # Mapa de la sucursal
│   ├── product-selection.tsx # Selección de listas de compras
│   ├── agent-status.tsx      # Estado del agente
│   ├── communication-log.tsx # Registro de comunicación
│   └── ui/                   # Componentes UI de shadcn
├── public/
│   └── maps/                 # Archivos JSON de mapas
│       ├── SUC001.json
│       └── SUC002.json
└── .env.local                # Variables de entorno
```

## Flujo de la Aplicación

### 1. Página Inicial (`/`)
- Muestra información del sistema
- Lista las sucursales disponibles (SUC001, SUC002)
- Botones para iniciar simulación en cada sucursal

### 2. Página de Simulación (`/simulation/[branchId]`)

La simulación pasa por 5 etapas:

#### **Etapa 1: Budget (Presupuesto)**
- Usuario ingresa el presupuesto en bolivianos
- Se crea un agente comprador con ID único
- POST `/api/comprador/crear`

#### **Etapa 2: Product-List (Lista de Productos)**
- El backend genera 3 listas usando **Temple Simulado**
- Se muestran las listas: Exacta, Superior, Inferior
- Usuario selecciona una lista
- POST `/api/comprador/generar-listas`
- POST `/api/comprador/seleccionar-lista`

#### **Etapa 3: Shopping (Recolección)**
- El agente usa el algoritmo **A\*** para navegar por el mapa
- Visualización del movimiento en tiempo real
- Recolecta productos de la lista seleccionada
- POST `/api/comprador/iniciar-recoleccion`

#### **Etapa 4: Checkout (Ir a Cajero)**
- Usa **Búsqueda de Costo Uniforme** para encontrar el cajero más cercano
- El agente se mueve a la posición del cajero
- POST `/api/comprador/ir-a-cajero`

#### **Etapa 5: Complete (Completado)**
- El cajero procesa la compra
- Se genera y muestra la factura con el total
- POST `/api/comprador/comunicar-cajero`

## Componentes Principales

### GridMap
Renderiza el mapa de la sucursal mostrando:
- Obstáculos (gris oscuro)
- Zonas de productos (amarillo)
- Cajeros (verde)
- Entrada (azul claro)
- Posición del agente (azul pulsante)

### ProductSelection
Muestra las 3 listas generadas por Temple Simulado con:
- Cantidad de productos
- Costo total
- Variedad de categorías
- Primeros productos de la lista

### AgentStatus
Indica el progreso de la simulación:
- Etapas completadas (✓)
- Etapa actual (spinner)
- Etapas pendientes (○)
- Información del presupuesto y productos

### CommunicationLog
Registro de mensajes entre agentes:
- Sistema → Agente
- Agente → Usuario
- Agente → Cajero
- Con timestamps y códigos de color

## API Backend

El frontend se comunica con el backend Flask en `http://localhost:5000`:

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/comprador/crear` | POST | Crea un nuevo agente comprador |
| `/api/comprador/generar-listas` | POST | Genera listas con Temple Simulado |
| `/api/comprador/seleccionar-lista` | POST | Selecciona una lista |
| `/api/comprador/iniciar-recoleccion` | POST | Inicia recolección con A* |
| `/api/comprador/ir-a-cajero` | POST | Busca cajero con UCS |
| `/api/comprador/comunicar-cajero` | POST | Procesa compra |

## Scripts Disponibles

```bash
# Desarrollo (con Turbopack)
pnpm dev

# Build de producción
pnpm build

# Iniciar en producción
pnpm start

# Linting
pnpm lint
```

## Notas Importantes

1. **Backend requerido**: El frontend necesita que el backend Flask esté corriendo en el puerto 5000.

2. **Mapas**: Los archivos JSON en `public/maps/` deben coincidir con las sucursales disponibles.

3. **CORS**: El backend debe tener CORS habilitado para peticiones desde `localhost:3000`.

4. **Hot Reload**: Turbopack proporciona recarga rápida durante el desarrollo.

## Troubleshooting

### "Module not found" errors
- Verifica que todas las dependencias estén instaladas: `pnpm install`
- Revisa las rutas de importación (usar `@/` para rutas absolutas)

### "Can't resolve JSON"
- Verifica que los archivos JSON existan en `public/maps/`
- La ruta debe ser `/maps/[id].json` sin el prefijo `public/`

### API errors
- Verifica que el backend esté corriendo
- Revisa la URL en `.env.local`
- Verifica CORS en el backend

### Build errors
- Limpia el caché: `rm -rf .next`
- Reinstala dependencias: `rm -rf node_modules pnpm-lock.yaml && pnpm install`

## Soporte

Para más información sobre el proyecto completo, consulta el README principal en la raíz del repositorio.
