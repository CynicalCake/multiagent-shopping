"use client"

import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Store, ArrowRight, ShoppingCart, Bot } from "lucide-react"
import Link from "next/link"

export default function HomePage() {
  const branches = [
    {
      id: "SUC001",
      name: "Hipermaxi - Circunvalación",
    },
    {
      id: "SUC002",
      name: "Hipermaxi - Torres Sófer",
    },
    {
      id: "SUC003",
      name: "Hipermaxi - Juan de la Rosa",
    },
    {
      id: "SUC004",
      name: "Hipermaxi - Blanco Galindo",
    },
    {
      id: "SUC005",
      name: "Hipermaxi - El Prado",
    },
    {
      id: "SUC006",
      name: "Hipermaxi - Panamericana",
    },
    {
      id: "SUC007",
      name: "Hipermaxi - Villazón",
    },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <div className="bg-white border-b shadow-sm">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Bot className="w-8 h-8 text-blue-600" />
              <div>
                <h1 className="text-3xl font-bold text-gray-900">Sistema de Agentes Inteligentes</h1>
                <p className="text-gray-600 text-sm">Simulación de compras autónomas en supermercados</p>
              </div>
            </div>
            <Link href="/editor">
              <Button variant="outline" className="gap-2">
                <Store className="w-4 h-4" />
                Editor de Mapas
              </Button>
            </Link>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-12">
        <Card className="max-w-4xl mx-auto p-8 bg-white/80 backdrop-blur">
          <div className="text-center mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-3">Seleccione una Sucursal</h2>
            <p className="text-gray-600">
              El agente comprador navegará por el supermercado usando algoritmos de búsqueda inteligente
            </p>
          </div>

          {/* Features */}
          <div className="grid md:grid-cols-3 gap-4 mb-8">
            <Card className="p-4 bg-blue-50 border-blue-200">
              <div className="flex items-center gap-3 mb-2">
                <ShoppingCart className="w-5 h-5 text-blue-600" />
                <h3 className="font-semibold text-blue-900">Temple Simulado</h3>
              </div>
              <p className="text-sm text-blue-700">Optimización de listas de compras</p>
            </Card>

            <Card className="p-4 bg-green-50 border-green-200">
              <div className="flex items-center gap-3 mb-2">
                <Bot className="w-5 h-5 text-green-600" />
                <h3 className="font-semibold text-green-900">Algoritmo A*</h3>
              </div>
              <p className="text-sm text-green-700">Navegación inteligente por el mapa</p>
            </Card>

            <Card className="p-4 bg-purple-50 border-purple-200">
              <div className="flex items-center gap-3 mb-2">
                <Store className="w-5 h-5 text-purple-600" />
                <h3 className="font-semibold text-purple-900">Búsqueda UCS</h3>
              </div>
              <p className="text-sm text-purple-700">Selección óptima de cajero</p>
            </Card>
          </div>

          {/* Branch Selection */}
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {branches.map((branch) => (
              <Card key={branch.id} className="p-6 hover:shadow-lg transition-shadow border-2">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <div className="flex items-center gap-2 mb-2">
                      <Store className="w-6 h-6 text-blue-600" />
                      <h3 className="text-xl font-bold text-gray-900">{branch.name}</h3>
                    </div>
                  </div>
                </div>

                <Link href={`/simulation/${branch.id}`}>
                  <Button className="w-full" size="lg">
                    Iniciar Simulación
                    <ArrowRight className="w-4 h-4 ml-2" />
                  </Button>
                </Link>
              </Card>
            ))}
          </div>

          {/* Instructions */}
          <Card className="mt-8 p-6 bg-gray-50 border-gray-200">
            <h3 className="font-semibold text-gray-900 mb-3">Cómo funciona:</h3>
            <ol className="space-y-2 text-sm text-gray-700">
              <li className="flex gap-2">
                <span className="font-semibold text-blue-600">1.</span>
                <span>Ingrese el presupuesto para el agente comprador</span>
              </li>
              <li className="flex gap-2">
                <span className="font-semibold text-blue-600">2.</span>
                <span>Seleccione una lista de compras optimizada con Temple Simulado</span>
              </li>
              <li className="flex gap-2">
                <span className="font-semibold text-blue-600">3.</span>
                <span>Observe al agente navegar usando A* para recolectar productos</span>
              </li>
              <li className="flex gap-2">
                <span className="font-semibold text-blue-600">4.</span>
                <span>El agente encontrará el cajero más cercano con Búsqueda de Costo Uniforme</span>
              </li>
              <li className="flex gap-2">
                <span className="font-semibold text-blue-600">5.</span>
                <span>Reciba la factura completa con el detalle de la compra</span>
              </li>
            </ol>
          </Card>
        </Card>
      </div>
    </div>
  )
}