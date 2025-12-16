"use client"

import { use, useState, useEffect } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { ArrowLeft, Play, Loader2 } from "lucide-react"
import Link from "next/link"
import { GridMap } from "@/components/grid-map"
import { ProductSelection } from "@/components/product-selection"
import { AgentStatus } from "@/components/agent-status"
import { CommunicationLog } from "@/components/communication-log"

type SimulationStage = "budget" | "product-list" | "shopping" | "checkout" | "complete"

interface Product {
  producto_id: number
  nombre: string
  precio: number
  cantidad: number
  categoria: string
}

interface ProductList {
  productos: Product[]
  total: number
  cantidad_items: number
}

interface InvoiceItem {
  nombre: string
  cantidad: number
  subtotal: number
  producto_id: number
  categoria: string
  precio_unitario: number
}

interface Invoice {
  cajero_id: string
  total: number
  cantidad_items: number
  items: InvoiceItem[]
}

interface Message {
  timestamp: string
  from: string
  to: string
  type: string
  content: string
}

export default function SimulationPage({ params }: { params: Promise<{ branchId: string }> }) {
  const { branchId } = use(params)
  const [stage, setStage] = useState<SimulationStage>("budget")
  const [budget, setBudget] = useState("")
  const [buyerId, setBuyerId] = useState(`COMP_${Date.now()}`)
  const [loading, setLoading] = useState(false)
  const [agentPosition, setAgentPosition] = useState({ row: 0, col: 15 })
  const [productLists, setProductLists] = useState<Record<string, ProductList> | null>(null)
  const [selectedListType, setSelectedListType] = useState<string>("")
  const [messages, setMessages] = useState<Message[]>([])
  const [collectedProducts, setCollectedProducts] = useState<Product[]>([])
  const [currentCashier, setCurrentCashier] = useState<string>("")
  const [invoice, setInvoice] = useState<Invoice | null>(null)
  const [animationStep, setAnimationStep] = useState<string>("")
  const [totalSteps, setTotalSteps] = useState<number>(0)
  const [currentStep, setCurrentStep] = useState<number>(0)
  const [currentRoute, setCurrentRoute] = useState<Array<{ fila: number; columna: number }>>([]) // Ruta actual a seguir
  const [cashierStatuses, setCashierStatuses] = useState<Record<string, "esperando" | "recibiendo">>({})

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000"

  // Helper function to convert coordinate arrays to objects
  const toCoord = (arr: any) => {
    if (!arr) return null
    if (Array.isArray(arr)) {
      return { fila: arr[0], columna: arr[1] }
    }
    if (arr.fila !== undefined && arr.columna !== undefined) {
      return arr
    }
    return null
  }

  const addMessage = (from: string, to: string, type: string, content: string) => {
    setMessages((prev) => [
      ...prev,
      {
        timestamp: new Date().toLocaleTimeString(),
        from,
        to,
        type,
        content,
      },
    ])
  }

  const startSimulation = async () => {
    if (!budget || Number.parseFloat(budget) <= 0) {
      alert("Por favor ingrese un presupuesto válido")
      return
    }

    setLoading(true)
    try {
      const response = await fetch(`${API_URL}/api/comprador/crear`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          comprador_id: buyerId,
          sucursal_id: branchId,
          presupuesto: Number.parseFloat(budget),
        }),
      })

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }

      const data = await response.json()
      
      if (data.success) {        // Initialize all cashiers as "esperando"
        if (data.mapa_sucursal?.cajeros) {
          const initialStatuses: Record<string, "esperando" | "recibiendo"> = {}
          data.mapa_sucursal.cajeros.forEach((cajero: any) => {
            initialStatuses[cajero.id] = "esperando"
          })
          setCashierStatuses(initialStatuses)
        }
                addMessage(
          "Sistema",
          buyerId,
          "info",
          `Agente comprador ingresó a ${branchId} con presupuesto de Bs. ${budget}`,
        )

        // Generate shopping lists
        const listsResponse = await fetch(`${API_URL}/api/comprador/generar-listas`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ comprador_id: buyerId }),
        })

        if (!listsResponse.ok) {
          throw new Error(`HTTP ${listsResponse.status}: Error al generar listas`)
        }

        const listsData = await listsResponse.json()
        
        if (listsData.success) {
          setProductLists(listsData.listas)
          addMessage(buyerId, "Usuario", "info", "Listas de compras generadas con Temple Simulado")
          setStage("product-list")
        } else {
          throw new Error(listsData.mensaje || "Error al generar listas")
        }
      } else {
        throw new Error(data.mensaje || "Error al crear comprador")
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : "Error desconocido"
      addMessage("Sistema", "Usuario", "error", `Error: ${errorMessage}`)
      console.error("Error starting simulation:", error)
    } finally {
      setLoading(false)
    }
  }

  const selectList = async (listType: string) => {
    setLoading(true)
    setSelectedListType(listType)

    try {
      const response = await fetch(`${API_URL}/api/comprador/seleccionar-lista`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          comprador_id: buyerId,
          tipo_lista: listType,
        }),
      })

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: Error al seleccionar lista`)
      }

      const data = await response.json()
      if (data.success) {
        addMessage("Usuario", buyerId, "selection", `Lista "${listType}" seleccionada`)
        startShopping()
      } else {
        throw new Error(data.mensaje || "Error al seleccionar lista")
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : "Error desconocido"
      addMessage("Sistema", "Usuario", "error", `Error: ${errorMessage}`)
      console.error("Error selecting list:", error)
    } finally {
      setLoading(false)
    }
  }

  const startShopping = async () => {
    setStage("shopping")
    addMessage(buyerId, "Sistema", "info", "Iniciando recolección de productos con A*")

    try {
      const response = await fetch(`${API_URL}/api/comprador/iniciar-recoleccion`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ comprador_id: buyerId }),
      })

      const data = await response.json()
      
      if (data.success) {
        addMessage(
          buyerId,
          "Sistema",
          "info",
          `Plan de recolección generado para ${data.resultado.productos_recolectados.length} productos`,
        )

        // Transform coordinate arrays to objects and log
        console.log("📦 Datos originales del backend:", data)
        
        // Animate movement through all routes
        if (data.plan?.plan_recoleccion?.length > 0) {
          const planSteps = data.plan.plan_recoleccion
          
          // Transform routes from arrays to coordinate objects
          const transformedSteps = planSteps.map((step: any) => ({
            ...step,
            ruta: step.ruta?.map((pos: any) => toCoord(pos)).filter((p: any) => p !== null) || [],
            ubicacion: toCoord(step.ubicacion),
            origen: toCoord(step.origen),
            destino: toCoord(step.destino)
          }))
          
          console.log("✅ Pasos transformados:", transformedSteps)
          
          // Calculate total steps for progress
          const totalMovements = transformedSteps.reduce((acc: number, step: any) => acc + (step.ruta?.length || 0), 0)
          console.log(`🚶 Total de movimientos: ${totalMovements}`)
          
          setTotalSteps(totalMovements)
          let stepCounter = 0
          
          // Animate through all product collection steps
          for (let i = 0; i < transformedSteps.length; i++) {
            const step = transformedSteps[i]
            console.log(`\n🎯 Producto ${i + 1}/${transformedSteps.length}: ${step.nombre}`)
            console.log(`   Ruta tiene ${step.ruta?.length || 0} pasos`)
            
            if (step.ruta && step.ruta.length > 0) {
              setAnimationStep(`Recolectando: ${step.nombre} (${i + 1}/${transformedSteps.length})`)
              
              // Set the full route for visualization
              setCurrentRoute(step.ruta)
              
              // Animate through the complete route to this product
              for (let j = 0; j < step.ruta.length; j++) {
                const pos = step.ruta[j]
                if (pos && pos.fila !== undefined && pos.columna !== undefined) {
                  console.log(`   Movimiento ${j + 1}: Fila ${pos.fila}, Col ${pos.columna}`)
                  setAgentPosition({ row: pos.fila, col: pos.columna })
                  stepCounter++
                  setCurrentStep(stepCounter)
                  // Update remaining route
                  setCurrentRoute(step.ruta.slice(j + 1))
                  await new Promise((resolve) => setTimeout(resolve, 100))
                } else {
                  console.warn(`   ⚠️ Posición inválida en índice ${j}:`, pos)
                }
              }
              
              console.log(`   ✓ Llegó a producto: ${step.nombre}`)
              // Clear route when arrived at product
              setCurrentRoute([])
              // Pause at product location
              await new Promise((resolve) => setTimeout(resolve, 300))
            } else {
              console.warn(`   ⚠️ Producto sin ruta válida`)
            }
          }
          
          console.log(`\n🎉 Recolección completada!`)
        } else {
          console.warn("⚠️ No hay plan de recolección o está vacío")
        }

        // Update collected products
        setCollectedProducts(data.resultado.productos_recolectados)
        addMessage(
          buyerId,
          "Sistema",
          "success",
          `✓ ${data.resultado.productos_recolectados.length} productos recolectados`,
        )

        // Move to final position if available
        if (data.resultado.posicion_final) {
          const finalPos = toCoord(data.resultado.posicion_final)
          if (finalPos) {
            console.log(`📍 Posición final: Fila ${finalPos.fila}, Col ${finalPos.columna}`)
            setAgentPosition({ row: finalPos.fila, col: finalPos.columna })
          }
        }

        setAnimationStep("")
        await new Promise((resolve) => setTimeout(resolve, 800))
        goToCashier()
      } else {
        throw new Error(data.mensaje || "Error en recolección")
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : "Error desconocido"
      addMessage("Sistema", "Usuario", "error", `Error durante recolección: ${errorMessage}`)
      console.error("Error during shopping:", error)
    }
  }

  const goToCashier = async () => {
    addMessage(buyerId, "Sistema", "info", "Buscando cajero más cercano con Búsqueda de Costo Uniforme")

    try {
      console.log("🏪 Enviando solicitud ir-a-cajero para:", buyerId)
      
      const response = await fetch(`${API_URL}/api/comprador/ir-a-cajero`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ comprador_id: buyerId }),
      })

      console.log("🏪 Response status:", response.status, response.statusText)
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }

      const data = await response.json()
      console.log("🏪 Respuesta ir-a-cajero completa:", JSON.stringify(data, null, 2))
      console.log("🏪 data.success:", data.success)
      console.log("🏪 data.cajero:", data.cajero)
      console.log("🏪 data.error:", data.error)
      
      if (data.success) {
        const cajeroInfo = data.cajero.cajero
        const rutaACajero = data.cajero.ruta_a_cajero || []
        const cajeroId = cajeroInfo?.id ?? 'CAJ_DESCONOCIDO'
        
        console.log("💰 Cajero info:", cajeroInfo)
        console.log("🚶 Ruta recibida:", rutaACajero)
        
        setCurrentCashier(cajeroId)
        addMessage(buyerId, "Sistema", "info", `Dirigiéndose a ${cajeroId} con UCS`)

        // Animate movement to cashier
        if (cajeroInfo && rutaACajero.length > 0) {
          const transformedRoute = rutaACajero.map((pos: any) => toCoord(pos)).filter((p: any) => p !== null)
          console.log(`🚶 Ruta al cajero tiene ${transformedRoute.length} pasos`)
          
          // Set the full route for visualization
          setCurrentRoute(transformedRoute)
          
          setAnimationStep(`Dirigiéndose al cajero ${cajeroId}`)
          setTotalSteps(transformedRoute.length)
          
          for (let i = 0; i < transformedRoute.length; i++) {
            const pos = transformedRoute[i]
            if (pos && pos.fila !== undefined && pos.columna !== undefined) {
              console.log(`   Movimiento ${i + 1}: Fila ${pos.fila}, Col ${pos.columna}`)
              setAgentPosition({ row: pos.fila, col: pos.columna })
              setCurrentStep(i + 1)
              // Update remaining route
              setCurrentRoute(transformedRoute.slice(i + 1))
              await new Promise((resolve) => setTimeout(resolve, 100))
            }
          }
          
          // Clear route when arrived
          setCurrentRoute([])
          
          // Set final position at cashier
          const finalPos = toCoord([cajeroInfo.fila, cajeroInfo.columna])
          if (finalPos) {
            console.log(`✓ Llegó al cajero en: Fila ${finalPos.fila}, Col ${finalPos.columna}`)
            setAgentPosition({ row: finalPos.fila, col: finalPos.columna })
          }
        } else {
          console.warn("⚠️ No hay ruta al cajero o información del cajero inválida")
        }

        setAnimationStep("")
        addMessage(buyerId, cajeroId, "info", `Llegó al cajero ${cajeroId}`)
        
        // Update cashier status to receiving
        setCashierStatuses(prev => ({ ...prev, [cajeroId]: "recibiendo" }))
        
        await new Promise((resolve) => setTimeout(resolve, 1000))
        setStage("checkout")
        processPurchase(cajeroId)
      } else {
        throw new Error(data.mensaje || "Error al buscar cajero")
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : "Error desconocido"
      addMessage("Sistema", "Usuario", "error", `Error al ir al cajero: ${errorMessage}`)
      console.error("Error going to cashier:", error)
    }
  }

  const processPurchase = async (cashierId: string) => {
    addMessage(buyerId, cashierId, "communication", "Enviando lista de productos al cajero")

    try {
      const response = await fetch(`${API_URL}/api/comprador/comunicar-cajero`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          comprador_id: buyerId,
          cajero_id: cashierId,
        }),
      })

      const data = await response.json()
      
      if (data.success) {
        addMessage(cashierId, buyerId, "communication", "Procesando productos...")
        await new Promise((resolve) => setTimeout(resolve, 1000))

        setInvoice(data.factura)
        addMessage(cashierId, buyerId, "success", `Factura generada. Total: Bs. ${data.factura.total.toFixed(2)}`)
        
        // Update cashier status back to waiting
        setCashierStatuses(prev => ({ ...prev, [cashierId]: "esperando" }))
        
        setStage("complete")
      } else {
        throw new Error(data.mensaje || "Error al procesar compra")
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : "Error desconocido"
      addMessage("Sistema", "Usuario", "error", `Error al procesar compra: ${errorMessage}`)
      console.error("Error processing purchase:", error)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="border-b bg-white">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Link href="/">
                <Button variant="ghost" size="sm">
                  <ArrowLeft className="w-4 h-4 mr-2" />
                  Volver
                </Button>
              </Link>
              <h1 className="text-2xl font-bold text-gray-900">Simulación: {branchId}</h1>
            </div>
            <div className="text-sm text-gray-600">Agente: {buyerId}</div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-6">
        <div className="grid lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            {stage === "budget" && (
              <Card className="p-6">
                <h2 className="text-xl font-semibold mb-4">Configurar Presupuesto</h2>
                <p className="text-gray-600 mb-4">Ingrese el presupuesto para la compra del agente</p>
                <div className="flex gap-4">
                  <Input
                    type="number"
                    placeholder="Presupuesto en Bs."
                    value={budget}
                    onChange={(e) => setBudget(e.target.value)}
                    className="flex-1"
                  />
                  <Button onClick={startSimulation} disabled={loading}>
                    {loading ? (
                      <>
                        <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                        Iniciando...
                      </>
                    ) : (
                      <>
                        <Play className="w-4 h-4 mr-2" />
                        Iniciar
                      </>
                    )}
                  </Button>
                </div>
              </Card>
            )}

            {stage === "product-list" && productLists && (
              <ProductSelection lists={productLists} onSelectList={selectList} loading={loading} />
            )}

            {stage === "product-list" && !productLists && (
              <Card className="p-6">
                <h2 className="text-xl font-semibold mb-4">Generando Listas...</h2>
                <div className="flex items-center justify-center py-8">
                  <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
                </div>
              </Card>
            )}

            {/* Animation Progress Indicator */}
            {(stage === "shopping" || stage === "checkout") && animationStep && (
              <Card className="p-4 bg-blue-50 border-blue-200">
                <div className="flex items-center gap-3">
                  <Loader2 className="w-5 h-5 animate-spin text-blue-600" />
                  <div className="flex-1">
                    <p className="font-semibold text-blue-900">{animationStep}</p>
                    {totalSteps > 0 && (
                      <p className="text-sm text-blue-700">
                        Paso {currentStep} de {totalSteps}
                      </p>
                    )}
                  </div>
                </div>
              </Card>
            )}

            <GridMap
              branchId={branchId}
              agentPosition={agentPosition}
              collectedProducts={collectedProducts}
              currentCashier={currentCashier}
              currentRoute={currentRoute}
              cashierStatuses={cashierStatuses}
            />

            {stage === "complete" && invoice && (
              <Card className="p-6">
                <h2 className="text-xl font-semibold mb-4">Factura de Compra</h2>
                <div className="space-y-3 text-sm mb-4">
                  <div className="flex justify-between">
                    <span className="text-gray-700">Cajero:</span>
                    <Badge variant="outline">{invoice.cajero_id || currentCashier}</Badge>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-700">Total de productos:</span>
                    <span className="font-semibold">{invoice.cantidad_items || invoice.items?.length || 0}</span>
                  </div>
                  <div className="flex justify-between text-lg font-bold text-green-900 pt-2 border-t">
                    <span>Total a pagar:</span>
                    <span>Bs. {invoice.total?.toFixed(2) || "0.00"}</span>
                  </div>
                </div>

                {/* Lista de productos comprados */}
                {invoice.items && invoice.items.length > 0 && (
                  <div className="mt-4 border-t pt-4">
                    <h3 className="font-semibold text-gray-900 mb-3">Detalle de Compra:</h3>
                    <div className="space-y-2 max-h-60 overflow-y-auto">
                      {invoice.items.map((item: any, idx: number) => (
                        <div key={idx} className="flex justify-between text-sm bg-white p-2 rounded border">
                          <div className="flex-1">
                            <span className="font-medium">{item.nombre}</span>
                            <span className="text-gray-500 ml-2">x{item.cantidad}</span>
                          </div>
                          <span className="font-semibold">Bs. {item.subtotal?.toFixed(2)}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                <div className="mt-4 pt-4 border-t text-center">
                  <p className="text-sm text-gray-600">
                    ✓ Compra procesada exitosamente
                  </p>
                </div>
              </Card>
            )}
          </div>

          <div className="space-y-6">
            <AgentStatus
              stage={stage}
              budget={budget}
              collectedProducts={collectedProducts}
              currentCashier={currentCashier}
            />

            <CommunicationLog messages={messages} />
          </div>
        </div>
      </div>
    </div>
  )
}
