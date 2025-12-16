# Guía de Instalación - Frontend del Sistema Multi-Agente

## Requisitos del Sistema

- **Node.js**: versión 18.17 o superior
- **npm**: versión 9 o superior (incluido con Node.js)
- **Sistema Operativo**: Windows, macOS, o Linux
- **Backend**: Flask ejecutándose en `http://localhost:5000`

## Verificar Instalaciones Previas

### 1. Verificar Node.js

Abrir terminal/consola y ejecutar:

```bash
node --version
```

Debe mostrar algo como `v18.17.0` o superior.

Si no está instalado, descargar desde: https://nodejs.org/

### 2. Verificar npm

```bash
npm --version
```

Debe mostrar algo como `9.0.0` o superior.

## Instalación Paso a Paso

### Paso 1: Navegar a la Carpeta del Frontend

```bash
cd frontend
```

Si estás en la raíz del proyecto donde está el backend Python.

### Paso 2: Instalar Dependencias

```bash
npm install
```

Este comando instalará todas las dependencias necesarias listadas en `package.json`. El proceso puede tomar 1-3 minutos dependiendo de tu conexión a internet.

### Paso 3: Verificar Instalación

Después de la instalación, deberías ver una carpeta `node_modules/` con todas las dependencias.

## Configuración

### Configurar URL del Backend (Opcional)

Por defecto, el frontend se conecta a `http://localhost:5000`.

Si tu backend está en otro puerto o dirección, crear archivo `.env.local`:

```bash
# En la carpeta frontend/
echo "NEXT_PUBLIC_API_URL=http://localhost:5000" > .env.local
```

En Windows (PowerShell):
```powershell
echo "NEXT_PUBLIC_API_URL=http://localhost:5000" | Out-File -FilePath .env.local -Encoding utf8
```

## Ejecutar la Aplicación

### Modo Desarrollo (Recomendado para Pruebas)

```bash
npm run dev
```

La aplicación estará disponible en: `http://localhost:3000`

### Modo Producción (Opcional)

```bash
npm run build
npm start
```

## Ejecutar el Sistema Completo

Para que todo funcione correctamente, necesitas **dos terminales abiertas**:

### Terminal 1 - Backend (Flask)

```bash
# Desde la raíz del proyecto
python app.py
```

Verás algo como:
```
🚀 Servidor Flask iniciado
📡 Escuchando en http://localhost:5000
```

### Terminal 2 - Frontend (Next.js)

```bash
# Desde la carpeta frontend/
cd frontend
npm run dev
```

Verás algo como:
```
▲ Next.js 15.1.0
- Local:        http://localhost:3000
- Ready in 2.3s
```

Ahora puedes abrir tu navegador en `http://localhost:3000`

## Estructura de Archivos Importante

```
frontend/
├── package.json           # Dependencias y scripts
├── node_modules/          # Dependencias instaladas (creada por npm install)
├── .next/                 # Archivos de compilación (creada por npm run dev/build)
├── app/                   # Páginas de la aplicación
├── components/            # Componentes React
├── public/                # Archivos estáticos (mapas JSON)
└── README.md             # Documentación
```

## Solución de Problemas Comunes

### Error: "node: command not found"

**Problema**: Node.js no está instalado.

**Solución**: Descargar e instalar desde https://nodejs.org/

### Error: "Cannot find module 'next'"

**Problema**: Dependencias no instaladas.

**Solución**: Ejecutar `npm install` en la carpeta frontend/

### Error: "Port 3000 is already in use"

**Problema**: El puerto 3000 está ocupado por otra aplicación.

**Soluciones**:

1. Cerrar otras aplicaciones que usen el puerto 3000
2. O ejecutar en otro puerto:
```bash
PORT=3001 npm run dev
```

En Windows:
```powershell
$env:PORT=3001; npm run dev
```

### Error: "Failed to fetch" en la aplicación

**Problema**: El backend Flask no está ejecutándose.

**Solución**: 
1. Abrir otra terminal
2. Ir a la raíz del proyecto
3. Ejecutar `python app.py`
4. Verificar que diga "Escuchando en http://localhost:5000"

### La página se ve sin estilos

**Problema**: Tailwind CSS no se compiló correctamente.

**Solución**:
1. Detener el servidor (Ctrl+C)
2. Borrar `.next/`
```bash
rm -rf .next   # En Linux/Mac
rmdir /s .next  # En Windows CMD
Remove-Item -Recurse -Force .next  # En Windows PowerShell
```
3. Ejecutar nuevamente `npm run dev`

### Error: "Module not found: Can't resolve '@/components/...'"

**Problema**: Problema con las rutas de TypeScript.

**Solución**: Verificar que `tsconfig.json` tenga:
```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

## Comandos Útiles

### Limpiar todo y reinstalar

```bash
# Borrar dependencias y archivos de compilación
rm -rf node_modules .next

# Reinstalar
npm install

# Ejecutar
npm run dev
```

En Windows PowerShell:
```powershell
Remove-Item -Recurse -Force node_modules, .next
npm install
npm run dev
```

### Ver logs detallados

```bash
npm run dev -- --verbose
```

### Verificar problemas de dependencias

```bash
npm audit
```

## Checklist de Instalación

- [ ] Node.js 18.17+ instalado
- [ ] npm 9+ instalado
- [ ] Navegado a la carpeta `frontend/`
- [ ] Ejecutado `npm install` exitosamente
- [ ] Backend Flask ejecutándose en puerto 5000
- [ ] Frontend ejecutándose en puerto 3000
- [ ] Navegador abierto en `http://localhost:3000`
- [ ] Página principal carga correctamente
- [ ] Se pueden ver las dos sucursales

## Siguientes Pasos

Una vez instalado y ejecutándose:

1. **Probar la Aplicación**: Selecciona una sucursal e inicia una simulación
2. **Leer la Documentación**: Revisa `README.md` para entender el flujo
3. **Explorar el Código**: Los componentes principales están en `components/`
4. **Personalizar**: Modifica colores, textos o funcionalidades según necesites

## Desinstalación

Para remover completamente el frontend:

```bash
cd frontend
rm -rf node_modules .next
```

En Windows:
```powershell
Remove-Item -Recurse -Force node_modules, .next
```

Esto no afecta el código fuente, solo las dependencias y archivos compilados.

## Soporte

Si tienes problemas no cubiertos en esta guía:

1. Verifica los logs en la terminal
2. Revisa la consola del navegador (F12)
3. Asegúrate de que el backend esté ejecutándose
4. Verifica que las versiones de Node.js y npm sean correctas

---

**Notas Importantes**:
- El frontend **DEBE** ejecutarse en la carpeta `frontend/`, no en la raíz del proyecto
- El backend **DEBE** estar ejecutándose para que el frontend funcione
- No subir la carpeta `node_modules/` a control de versiones (ya está en `.gitignore`)

¡Buena suerte con tu proyecto!
