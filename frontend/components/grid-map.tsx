"use client"

import { useEffect, useState } from "react"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Loader2 } from "lucide-react"

interface GridMapProps {
  branchId: string
  agentPosition: { row: number; col: number }
  collectedProducts: any[]
  currentCashier: string
  currentRoute?: Array<{ fila: number; columna: number }>
  cashierStatuses?: Record<string, "esperando" | "recibiendo">
}

export function GridMap({ branchId, agentPosition, collectedProducts, currentCashier, currentRoute = [], cashierStatuses = {} }: GridMapProps) {
  const [mapData, setMapData] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [prevPosition, setPrevPosition] = useState<{ row: number; col: number } | null>(null)
  const [inventario, setInventario] = useState<any>(null)
  const [hoveredZone, setHoveredZone] = useState<string | null>(null)

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000"

  useEffect(() => {
    // Leer mapa desde el backend (fuente única de verdad)
    fetch(`${API_URL}/api/mapas/${branchId}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          setMapData(data.mapa)
        } else {
          console.error("Error al cargar mapa:", data.error)
        }
        setLoading(false)
      })
      .catch((err) => {
        console.error("Error loading map:", err)
        setLoading(false)
      })
    
    // Cargar inventario para mostrar información de productos
    fetch(`${API_URL}/api/inventarios/${branchId}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          setInventario(data.inventario)
        }
      })
      .catch((err) => {
        console.error("Error loading inventory:", err)
      })
  }, [branchId, API_URL])

  // Track position changes
  useEffect(() => {
    if (agentPosition) {
      console.log(`🎯 GridMap: Agente actualizado a Fila ${agentPosition.row}, Col ${agentPosition.col}`)
      setPrevPosition(agentPosition)
    }
  }, [agentPosition])

  if (loading || !mapData) {
    return (
      <Card className="p-6">
        <div className="flex flex-col items-center justify-center h-96 gap-4">
          <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
          <p className="text-gray-500">Cargando mapa de {branchId}...</p>
        </div>
      </Card>
    )
  }

  const cellSize = 20
  const width = mapData.dimensiones.columnas * cellSize
  const height = mapData.dimensiones.filas * cellSize

  const isObstacle = (row: number, col: number) => {
    return mapData.obstaculos.some((obs: any) => obs.fila === row && obs.columna === col)
  }

  const isCashier = (row: number, col: number) => {
    return mapData.cajeros.find((caj: any) => caj.fila === row && caj.columna === col)
  }

  const isProductZone = (row: number, col: number) => {
    return Object.values(mapData.zonas_productos).find((zona: any) => zona.fila === row && zona.columna === col)
  }

  const getProductZoneName = (row: number, col: number) => {
    const entry = Object.entries(mapData.zonas_productos).find(
      ([_, zona]: [string, any]) => zona.fila === row && zona.columna === col
    )
    return entry ? entry[0] : null
  }

  const getProductsInZone = (zoneName: string) => {
    if (!inventario) return []
    const zona = mapData.zonas_productos[zoneName]
    if (!zona || !zona.productos) return []
    
    return zona.productos
      .map((prodId: number) => inventario.productos.find((p: any) => p.id === prodId))
      .filter(Boolean)
  }

  const isEntrance = (row: number, col: number) => {
    return mapData.entrada.fila === row && mapData.entrada.columna === col
  }

  return (
    <Card className="p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold">Mapa de Sucursal</h2>
        
        {/* Leyenda con colores reales */}
        <div className="flex gap-3 text-xs items-center">
          <div className="flex items-center gap-1">
            <div className="w-4 h-4 border border-gray-300" style={{ backgroundColor: "#374151" }}></div>
            <span>Obstáculos</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-4 h-4 border border-gray-300" style={{ backgroundColor: "#dbeafe" }}></div>
            <span>Entrada</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-4 h-4 border border-gray-300" style={{ backgroundColor: "#fef3c7" }}></div>
            <span>Productos</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-4 h-4 border border-gray-300" style={{ backgroundColor: "#d1fae5" }}></div>
            <span>Cajeros</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-4 h-4 border border-gray-300 rounded-full" style={{ backgroundColor: "#3b82f6" }}></div>
            <span>Agente</span>
          </div>
        </div>
      </div>

      <div className="overflow-auto border rounded-lg bg-white relative">
        <svg width={width} height={height} className="min-w-full">
          {Array.from({ length: mapData.dimensiones.filas }).map((_, row) =>
            Array.from({ length: mapData.dimensiones.columnas }).map((_, col) => {
              const x = col * cellSize
              const y = row * cellSize
              const obstacle = isObstacle(row, col)
              const cashier = isCashier(row, col)
              const productZone = isProductZone(row, col)
              const zoneName = getProductZoneName(row, col)
              const entrance = isEntrance(row, col)
              const isAgent = agentPosition.row === row && agentPosition.col === col

              let fill = "#f9fafb"
              if (obstacle) fill = "#374151"
              if (entrance) fill = "#dbeafe"
              if (productZone) fill = "#fef3c7"
              if (cashier) fill = "#d1fae5"
              if (isAgent) fill = "#3b82f6"

              return (
                <g key={`${row}-${col}`}>
                  <rect
                    x={x}
                    y={y}
                    width={cellSize}
                    height={cellSize}
                    fill={fill}
                    stroke="#e5e7eb"
                    strokeWidth="0.5"
                    onMouseEnter={() => {
                      if (zoneName) setHoveredZone(zoneName)
                    }}
                    onMouseLeave={() => {
                      if (zoneName) setHoveredZone(null)
                    }}
                    style={{ cursor: productZone ? "pointer" : "default" }}
                  />
                </g>
              )
            }),
          )}

          {/* Path visualization - Show route to next objective */}
          {currentRoute && currentRoute.length > 0 && (
            <g>
              {/* Draw path as connected line segments */}
              <polyline
                points={[
                  // Start from current agent position
                  `${agentPosition.col * cellSize + cellSize / 2},${agentPosition.row * cellSize + cellSize / 2}`,
                  // Add all route points
                  ...currentRoute.map(
                    (pos) => `${pos.columna * cellSize + cellSize / 2},${pos.fila * cellSize + cellSize / 2}`
                  ),
                ].join(" ")}
                fill="none"
                stroke="#10b981"
                strokeWidth="2"
                strokeDasharray="4,4"
                strokeLinecap="round"
                strokeLinejoin="round"
                opacity="0.7"
              />
              {/* Draw small circles at each waypoint */}
              {currentRoute.map((pos, idx) => (
                <circle
                  key={`waypoint-${idx}`}
                  cx={pos.columna * cellSize + cellSize / 2}
                  cy={pos.fila * cellSize + cellSize / 2}
                  r={2}
                  fill="#10b981"
                  opacity="0.5"
                />
              ))}
              {/* Highlight destination with a larger circle */}
              {currentRoute.length > 0 && (
                <circle
                  cx={currentRoute[currentRoute.length - 1].columna * cellSize + cellSize / 2}
                  cy={currentRoute[currentRoute.length - 1].fila * cellSize + cellSize / 2}
                  r={cellSize / 4}
                  fill="none"
                  stroke="#10b981"
                  strokeWidth="2"
                  opacity="0.8"
                />
              )}
            </g>
          )}

          {/* Agent marker - Enhanced visibility */}
          <g>
            {/* Shadow/glow effect */}
            <circle
              cx={agentPosition.col * cellSize + cellSize / 2}
              cy={agentPosition.row * cellSize + cellSize / 2}
              r={cellSize / 2.5}
              fill="#3b82f6"
              opacity="0.3"
              className="animate-pulse"
            />
            {/* Main agent circle */}
            <circle
              cx={agentPosition.col * cellSize + cellSize / 2}
              cy={agentPosition.row * cellSize + cellSize / 2}
              r={cellSize / 3.5}
              fill="#3b82f6"
              stroke="#ffffff"
              strokeWidth="2"
            />
            {/* Inner dot for better visibility */}
            <circle
              cx={agentPosition.col * cellSize + cellSize / 2}
              cy={agentPosition.row * cellSize + cellSize / 2}
              r={cellSize / 8}
              fill="#ffffff"
            />
          </g>
        </svg>
      </div>

      {/* Tooltip flotante para productos */}
      {hoveredZone && inventario && (
        <div className="absolute z-10 p-3 bg-white border-2 border-yellow-400 rounded-lg shadow-xl max-w-sm"
             style={{
               top: "50%",
               left: "50%",
               transform: "translate(-50%, -50%)",
             }}>
          <h4 className="font-bold text-sm mb-2 text-yellow-900 border-b border-yellow-200 pb-1">
            📦 {hoveredZone}
          </h4>
          <div className="space-y-1 max-h-48 overflow-y-auto">
            {getProductsInZone(hoveredZone).map((producto: any) => (
              <div key={producto.id} className="flex justify-between items-center text-xs py-1 px-2 bg-yellow-50 rounded">
                <span className="flex-1">{producto.nombre}</span>
                <span className="font-semibold text-green-700 ml-2">Bs. {producto.precio.toFixed(2)}</span>
              </div>
            ))}
            {getProductsInZone(hoveredZone).length === 0 && (
              <p className="text-xs text-gray-500 italic">No hay productos en esta zona</p>
            )}
          </div>
        </div>
      )}

      <div className="mt-4 space-y-3">
        {/* Estado de cajeros */}
        {mapData.cajeros && mapData.cajeros.length > 0 && (
          <div className="p-3 bg-green-50 rounded-lg">
            <h3 className="text-sm font-semibold text-green-900 mb-2">Estado de Cajeros</h3>
            <div className="grid grid-cols-3 gap-2">
              {mapData.cajeros.map((cajero: any) => {
                const status = cashierStatuses[cajero.id] || "esperando"
                const isActive = currentCashier === cajero.id
                return (
                  <div 
                    key={cajero.id} 
                    className={`text-xs p-2 rounded ${
                      isActive 
                        ? "bg-green-200 border-2 border-green-600" 
                        : status === "recibiendo"
                        ? "bg-yellow-100 border border-yellow-400"
                        : "bg-white border border-green-300"
                    }`}
                  >
                    <div className="font-semibold">{cajero.id}</div>
                    <div className={`text-xs ${
                      status === "recibiendo" ? "text-yellow-700" : "text-green-700"
                    }`}>
                      {status === "recibiendo" ? "Ocupado" : "Libre"}
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        )}

        {/* Información general */}
        <div className="text-xs text-gray-600 grid grid-cols-2 gap-2">
          <div>
            Dimensiones: {mapData.dimensiones.filas} × {mapData.dimensiones.columnas}
          </div>
          <div>Productos recolectados: {collectedProducts.length}</div>
        </div>
      </div>
      
      {/* Debug info - Agent position */}
      <div className="mt-2 p-2 bg-blue-50 rounded text-xs text-blue-900 font-mono">
        Agente en: Fila {agentPosition.row}, Columna {agentPosition.col}
      </div>
    </Card>
  )
}
