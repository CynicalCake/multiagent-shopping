"use client"

import { useState, useEffect } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Save, Download, Upload, Trash2, Grid3x3, Plus } from "lucide-react"
import Link from "next/link"

type CellType = "empty" | "obstacle" | "entrance" | "cashier" | "product"

interface MapData {
  sucursal_id: string
  nombre: string
  dimensiones: {
    filas: number
    columnas: number
  }
  entrada: { fila: number; columna: number; tipo: string }
  cajeros: Array<{ id: string; fila: number; columna: number }>
  obstaculos: Array<{ fila: number; columna: number }>
  zonas_productos: Record<string, { fila: number; columna: number; productos: number[] }>
}

export default function MapEditorPage() {
  const [sucursalId, setSucursalId] = useState("SUC003")
  const [nombre, setNombre] = useState("Nueva Sucursal")
  const [filas, setFilas] = useState(20)
  const [columnas, setColumnas] = useState(30)
  const [grid, setGrid] = useState<CellType[][]>([])
  const [selectedTool, setSelectedTool] = useState<CellType>("obstacle")
  const [cajeros, setCajeros] = useState<Array<{ id: string; fila: number; columna: number }>>([])
  const [zonas, setZonas] = useState<Record<string, { fila: number; columna: number; productos: number[] }>>({})
  const [entrada, setEntrada] = useState<{ fila: number; columna: number } | null>(null)
  const [newZoneName, setNewZoneName] = useState("")
  const [newZonaProductos, setNewZonaProductos] = useState("")
  const [editingZone, setEditingZone] = useState<string | null>(null)
  const [saving, setSaving] = useState(false)

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000"

  // Inicializar grid solo cuando cambian las dimensiones manualmente
  useEffect(() => {
    console.log('🔥 useEffect disparado - filas:', filas, 'columnas:', columnas)
    // Verificar si el grid actual coincide con las nuevas dimensiones
    if (grid.length !== filas || (grid[0] && grid[0].length !== columnas)) {
      console.log('📐 Dimensiones cambiaron, reinicializando grid')
      initializeGrid()
    }
  }, [filas, columnas])

  const initializeGrid = () => {
    console.log('⚠️ initializeGrid ejecutado - borrando grid')
    const newGrid: CellType[][] = []
    for (let i = 0; i < filas; i++) {
      newGrid[i] = []
      for (let j = 0; j < columnas; j++) {
        newGrid[i][j] = "empty"
      }
    }
    setGrid(newGrid)
  }

  const handleCellClick = (row: number, col: number, isRightClick: boolean = false) => {
    // Si es clic derecho, eliminar elementos en esa posición
    if (isRightClick) {
      // Eliminar cajero si existe
      const cajeroIndex = cajeros.findIndex(c => c.fila === row && c.columna === col)
      if (cajeroIndex !== -1) {
        setCajeros(cajeros.filter((_, i) => i !== cajeroIndex))
        return
      }

      // Eliminar zona de productos si existe
      const zonaEntry = Object.entries(zonas).find(([_, z]) => z.fila === row && z.columna === col)
      if (zonaEntry) {
        const [zoneName] = zonaEntry
        const newZonas = { ...zonas }
        delete newZonas[zoneName]
        setZonas(newZonas)
        return
      }

      // Eliminar entrada si existe
      if (entrada && entrada.fila === row && entrada.columna === col) {
        setEntrada(null)
        return
      }
    }

    const newGrid = [...grid]

    if (selectedTool === "entrance") {
      // Solo puede haber una entrada
      setEntrada({ fila: row, columna: col })
      // No modificar el grid para entrada
    } else if (selectedTool === "cashier") {
      // Agregar cajero con ID único
      // Encontrar el próximo número disponible
      const existingNumbers = cajeros
        .map(c => parseInt(c.id.replace('CAJ', '')))
        .filter(n => !isNaN(n))
      
      let nextNumber = 1
      while (existingNumbers.includes(nextNumber)) {
        nextNumber++
      }
      
      const cajeroId = `CAJ${String(nextNumber).padStart(3, "0")}`
      setCajeros([...cajeros, { id: cajeroId, fila: row, columna: col }])
    } else if (selectedTool === "product") {
      // Agregar zona de productos
      if (newZoneName.trim()) {
        // Parsear lista de IDs de productos (ej: "1,2,3,4" o "1 2 3")
        const productIds = newZonaProductos
          .split(/[,\s]+/)
          .map(id => parseInt(id.trim()))
          .filter(id => !isNaN(id))
        
        setZonas({
          ...zonas,
          [newZoneName]: { fila: row, columna: col, productos: productIds.length > 0 ? productIds : [1] },
        })
        setNewZoneName("")
        setNewZonaProductos("")
      } else {
        alert("Ingrese el nombre de la zona primero")
      }
    } else if (selectedTool === "obstacle") {
      newGrid[row][col] = newGrid[row][col] === "obstacle" ? "empty" : "obstacle"
    } else {
      newGrid[row][col] = selectedTool
    }

    setGrid(newGrid)
  }

  const getCellColor = (row: number, col: number) => {
    // Check if entrance
    if (entrada && entrada.fila === row && entrada.columna === col) {
      return "#dbeafe"
    }

    // Check if cashier
    if (cajeros.some((c) => c.fila === row && c.columna === col)) {
      return "#d1fae5"
    }

    // Check if product zone
    const isProductZone = Object.values(zonas).some((z) => z.fila === row && z.columna === col)
    if (isProductZone) {
      return "#fef3c7"
    }

    // Check grid state
    if (grid[row]?.[col] === "obstacle") return "#374151"
    return "#f9fafb"
  }

  const exportMap = () => {
    const obstaculos = []
    for (let i = 0; i < filas; i++) {
      for (let j = 0; j < columnas; j++) {
        if (grid[i][j] === "obstacle") {
          obstaculos.push({ fila: i, columna: j })
        }
      }
    }

    const mapData: MapData = {
      sucursal_id: sucursalId,
      nombre,
      dimensiones: { filas, columnas },
      entrada: entrada || { fila: 0, columna: Math.floor(columnas / 2), tipo: "entrada" },
      cajeros,
      obstaculos,
      zonas_productos: zonas,
    }

    return mapData
  }

  const saveMap = async () => {
    setSaving(true)
    try {
      const mapData = exportMap()
      const response = await fetch(`${API_URL}/api/mapas/${sucursalId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(mapData),
      })

      const data = await response.json()
      if (data.success) {
        alert(
          `✓ Mapa ${sucursalId} guardado exitosamente\n\n` +
          `⚠️ IMPORTANTE: Debes reiniciar el servidor Flask para que los cajeros se inicialicen.\n\n` +
          `En la terminal de Flask, presiona Ctrl+C y luego ejecuta:\n` +
          `python app.py`
        )
      } else {
        alert(`Error: ${data.error}`)
      }
    } catch (error) {
      alert(`Error al guardar: ${error}`)
    } finally {
      setSaving(false)
    }
  }

  const downloadJSON = () => {
    const mapData = exportMap()
    const blob = new Blob([JSON.stringify(mapData, null, 2)], { type: "application/json" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `${sucursalId}.json`
    a.click()
    URL.revokeObjectURL(url)
  }

  const loadMap = async () => {
    try {
      console.log('📥 Iniciando carga de mapa:', sucursalId)
      
      const response = await fetch(`${API_URL}/api/mapas/${sucursalId}`)
      const data = await response.json()

      if (data.success) {
        const mapa = data.mapa
        console.log('📦 Mapa recibido:', mapa.dimensiones, 'obstáculos:', mapa.obstaculos.length)
        
        setNombre(mapa.nombre)
        setEntrada(mapa.entrada)
        setCajeros(mapa.cajeros)
        setZonas(mapa.zonas_productos)
        
        // Crear el grid completo con las dimensiones y obstáculos del mapa
        const newFilas = mapa.dimensiones.filas
        const newColumnas = mapa.dimensiones.columnas
        const newGrid: CellType[][] = []
        
        let obstacleCount = 0
        for (let i = 0; i < newFilas; i++) {
          newGrid[i] = []
          for (let j = 0; j < newColumnas; j++) {
            const isObstacle = mapa.obstaculos.some((obs: any) => obs.fila === i && obs.columna === j)
            newGrid[i][j] = isObstacle ? "obstacle" : "empty"
            if (isObstacle) obstacleCount++
          }
        }
        
        console.log('✅ Grid creado con', obstacleCount, 'obstáculos')
        console.log('🔄 Actualizando estado: filas', newFilas, 'columnas', newColumnas)
        
        // Actualizar grid PRIMERO, luego las dimensiones
        // Como el grid ya tiene el tamaño correcto, el useEffect no hará nada
        setGrid(newGrid)
        setFilas(newFilas)
        setColumnas(newColumnas)
        
        console.log('✅ Estados actualizados')

        alert(`✓ Mapa ${sucursalId} cargado exitosamente`)
      } else {
        alert(`Error: ${data.error}`)
      }
    } catch (error) {
      alert(`Error al cargar: ${error}`)
    }
  }

  const clearGrid = () => {
    if (confirm("¿Seguro que quieres limpiar todo el mapa?")) {
      initializeGrid()
      setCajeros([])
      setZonas({})
      setEntrada(null)
    }
  }

  const cellSize = 15

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-6">
          <Link href="/" className="text-blue-600 hover:underline mb-4 inline-block">
            ← Volver al inicio
          </Link>
          <h1 className="text-3xl font-bold">Editor de Mapas de Sucursales</h1>
          <p className="text-gray-600">Crea y edita mapas para el sistema multi-agente</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Panel de configuración */}
          <Card className="p-6 lg:col-span-1">
            <h2 className="text-xl font-semibold mb-4">Configuración</h2>

            <div className="space-y-4">
              <div>
                <Label htmlFor="sucursalId">ID de Sucursal</Label>
                <Input
                  id="sucursalId"
                  value={sucursalId}
                  onChange={(e) => setSucursalId(e.target.value)}
                  placeholder="SUC003"
                />
              </div>

              <div>
                <Label htmlFor="nombre">Nombre</Label>
                <Input
                  id="nombre"
                  value={nombre}
                  onChange={(e) => setNombre(e.target.value)}
                  placeholder="Nombre de la sucursal"
                />
              </div>

              <div className="grid grid-cols-2 gap-2">
                <div>
                  <Label htmlFor="filas">Filas</Label>
                  <Input
                    id="filas"
                    type="number"
                    value={filas}
                    onChange={(e) => setFilas(Number(e.target.value))}
                    min={5}
                    max={50}
                  />
                </div>
                <div>
                  <Label htmlFor="columnas">Columnas</Label>
                  <Input
                    id="columnas"
                    type="number"
                    value={columnas}
                    onChange={(e) => setColumnas(Number(e.target.value))}
                    min={5}
                    max={50}
                  />
                </div>
              </div>

              <div className="pt-4 border-t">
                <Label className="mb-2 block">Herramientas</Label>
                <div className="grid grid-cols-2 gap-2">
                  <Button
                    variant={selectedTool === "obstacle" ? "default" : "outline"}
                    onClick={() => setSelectedTool("obstacle")}
                    className="w-full"
                    size="sm"
                  >
                    Obstáculo
                  </Button>
                  <Button
                    variant={selectedTool === "entrance" ? "default" : "outline"}
                    onClick={() => setSelectedTool("entrance")}
                    className="w-full"
                    size="sm"
                  >
                    Entrada
                  </Button>
                  <Button
                    variant={selectedTool === "cashier" ? "default" : "outline"}
                    onClick={() => setSelectedTool("cashier")}
                    className="w-full"
                    size="sm"
                  >
                    Cajero
                  </Button>
                  <Button
                    variant={selectedTool === "product" ? "default" : "outline"}
                    onClick={() => setSelectedTool("product")}
                    className="w-full"
                    size="sm"
                  >
                    Producto
                  </Button>
                </div>
              </div>

              {selectedTool === "product" && (
                <div className="space-y-2">
                  <div>
                    <Label htmlFor="zoneName">Nombre de Zona</Label>
                    <Input
                      id="zoneName"
                      value={newZoneName}
                      onChange={(e) => setNewZoneName(e.target.value)}
                      placeholder="ej: lacteos, panaderia"
                    />
                  </div>
                  <div>
                    <Label htmlFor="productos">IDs de Productos</Label>
                    <Input
                      id="productos"
                      value={newZonaProductos}
                      onChange={(e) => setNewZonaProductos(e.target.value)}
                      placeholder="ej: 1,2,3,4 o 1 2 3"
                    />
                    <p className="text-xs text-gray-500 mt-1">Separados por comas o espacios</p>
                  </div>
                  <p className="text-xs text-blue-600 font-medium">Click en el mapa para colocar la zona</p>
                </div>
              )}

              <div className="pt-4 border-t space-y-2">
                <Button onClick={saveMap} disabled={saving} className="w-full" variant="default">
                  <Save className="w-4 h-4 mr-2" />
                  {saving ? "Guardando..." : "Guardar en Backend"}
                </Button>
                <Button onClick={loadMap} className="w-full" variant="outline">
                  <Upload className="w-4 h-4 mr-2" />
                  Cargar desde Backend
                </Button>
                <Button onClick={downloadJSON} className="w-full" variant="outline">
                  <Download className="w-4 h-4 mr-2" />
                  Descargar JSON
                </Button>
                <Button onClick={clearGrid} className="w-full" variant="destructive">
                  <Trash2 className="w-4 h-4 mr-2" />
                  Limpiar Todo
                </Button>
              </div>

              {/* Leyenda */}
              <div className="pt-4 border-t">
                <Label className="mb-2 block">Leyenda</Label>
                <div className="space-y-2 text-sm">
                  <div className="flex items-center gap-2">
                    <div className="w-4 h-4" style={{ backgroundColor: "#374151" }}></div>
                    <span>Obstáculos</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-4 h-4" style={{ backgroundColor: "#dbeafe" }}></div>
                    <span>Entrada</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-4 h-4" style={{ backgroundColor: "#fef3c7" }}></div>
                    <span>Productos</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-4 h-4" style={{ backgroundColor: "#d1fae5" }}></div>
                    <span>Cajeros</span>
                  </div>
                </div>
              </div>
            </div>
          </Card>

          {/* Grid del mapa */}
          <Card className="p-6 lg:col-span-2">
            <h2 className="text-xl font-semibold mb-4">Mapa {sucursalId}</h2>
            <p className="text-sm text-gray-600 mb-4">
              {filas} × {columnas} celdas - <strong>Clic izquierdo</strong> para colocar, <strong>clic derecho</strong> para eliminar
            </p>

            <div className="overflow-auto border rounded-lg bg-white">
              <svg width={columnas * cellSize} height={filas * cellSize} className="min-w-full">
                {grid.map((row, rowIndex) =>
                  row.map((cell, colIndex) => (
                    <rect
                      key={`${rowIndex}-${colIndex}`}
                      x={colIndex * cellSize}
                      y={rowIndex * cellSize}
                      width={cellSize}
                      height={cellSize}
                      fill={getCellColor(rowIndex, colIndex)}
                      stroke="#e5e7eb"
                      strokeWidth="0.5"
                      onClick={() => handleCellClick(rowIndex, colIndex, false)}
                      onContextMenu={(e) => {
                        e.preventDefault()
                        handleCellClick(rowIndex, colIndex, true)
                      }}
                      style={{ cursor: "pointer" }}
                    />
                  ))
                )}
              </svg>
            </div>

            {/* Información del mapa */}
            <div className="mt-4 grid grid-cols-3 gap-4 text-sm">
              <div className="p-3 bg-gray-50 rounded">
                <div className="font-semibold">Entrada</div>
                <div className="text-xs text-gray-600">
                  {entrada ? `Fila ${entrada.fila}, Col ${entrada.columna}` : "No definida"}
                </div>
              </div>
              <div className="p-3 bg-gray-50 rounded">

            {/* Lista de zonas con productos */}
            {Object.keys(zonas).length > 0 && (
              <div className="mt-4 pt-4 border-t">
                <h3 className="font-semibold mb-2">Zonas de Productos</h3>
                <div className="space-y-2 max-h-64 overflow-y-auto">
                  {Object.entries(zonas).map(([nombre, zona]) => (
                    <div key={nombre} className="p-2 bg-yellow-50 border border-yellow-200 rounded text-sm">
                      <div className="flex items-center justify-between mb-1">
                        <span className="font-semibold text-yellow-900">{nombre}</span>
                        <Button
                          size="sm"
                          variant="ghost"
                          onClick={() => {
                            const newZonas = { ...zonas }
                            delete newZonas[nombre]
                            setZonas(newZonas)
                          }}
                          className="h-6 w-6 p-0 text-red-600 hover:bg-red-100"
                        >
                          ×
                        </Button>
                      </div>
                      <div className="text-xs text-yellow-700">
                        📍 Posición: ({zona.fila}, {zona.columna})
                      </div>
                      <div className="text-xs text-yellow-700">
                        📦 Productos: [{zona.productos.join(", ")}]
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Lista de cajeros */}
            {cajeros.length > 0 && (
              <div className="mt-4 pt-4 border-t">
                <h3 className="font-semibold mb-2">Cajeros</h3>
                <div className="space-y-2">
                  {cajeros.map((cajero, index) => (
                    <div key={`cajero-${index}`} className="p-2 bg-green-50 border border-green-200 rounded text-sm">
                      <div className="flex items-center justify-between">
                        <div>
                          <span className="font-semibold text-green-900">{cajero.id}</span>
                          <span className="text-xs text-green-700 ml-2">
                            ({cajero.fila}, {cajero.columna})
                          </span>
                        </div>
                        <Button
                          size="sm"
                          variant="ghost"
                          onClick={() => {
                            setCajeros(cajeros.filter((_, i) => i !== index))
                          }}
                          className="h-6 w-6 p-0 text-red-600 hover:bg-red-100"
                        >
                          ×
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
                <div className="font-semibold">Cajeros: {cajeros.length}</div>
                <div className="text-xs text-gray-600">
                  {cajeros.map((c) => c.id).join(", ") || "Ninguno"}
                </div>
              </div>
              <div className="p-3 bg-gray-50 rounded">
                <div className="font-semibold">Zonas: {Object.keys(zonas).length}</div>
                <div className="text-xs text-gray-600">
                  {Object.keys(zonas).join(", ") || "Ninguna"}
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  )
}
