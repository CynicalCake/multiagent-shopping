"use client"

import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Loader2 } from "lucide-react"

interface ProductSelectionProps {
  lists: any
  onSelectList: (listType: string) => void
  loading: boolean
}

export function ProductSelection({ lists, onSelectList, loading }: ProductSelectionProps) {
  const listTypes = [
    { key: "lista_exacta", label: "Lista Exacta", color: "bg-blue-50 border-blue-200", shortKey: "exacta" },
    { key: "lista_superior", label: "Lista Superior", color: "bg-green-50 border-green-200", shortKey: "superior" },
    { key: "lista_inferior", label: "Lista Inferior", color: "bg-amber-50 border-amber-200", shortKey: "inferior" },
  ]

  if (!lists) {
    return (
      <Card className="p-6">
        <h2 className="text-xl font-semibold mb-4">Seleccionar Lista de Compras</h2>
        <p className="text-sm text-gray-600 text-center py-8">Cargando listas...</p>
      </Card>
    )
  }

  return (
    <Card className="p-6">
      <h2 className="text-xl font-semibold mb-4">Seleccionar Lista de Compras</h2>
      <p className="text-sm text-gray-600 mb-6">
        El agente ha generado 3 listas usando Temple Simulado. Seleccione una para continuar.
      </p>

      <div className="grid md:grid-cols-3 gap-4">
        {listTypes.map((listType) => {
          const list = lists[listType.key]
          
          if (!list) {
            return (
              <Card key={listType.key} className={`p-4 border-2 ${listType.color}`}>
                <h3 className="font-semibold mb-2">{listType.label}</h3>
                <p className="text-sm text-gray-500">No disponible</p>
              </Card>
            )
          }

          // Obtener categorías únicas de los productos
          const uniqueCategories = new Set(list.productos?.map((p: any) => p.categoria) || [])

          return (
            <Card key={listType.key} className={`p-4 border-2 ${listType.color}`}>
              <h3 className="font-semibold mb-2">{listType.label}</h3>
              <div className="space-y-2 mb-4">
                <div className="text-sm">
                  <span className="text-gray-600">Productos:</span>
                  <span className="font-semibold ml-2">{list.cantidad_items || list.productos?.length || 0}</span>
                </div>
                <div className="text-sm">
                  <span className="text-gray-600">Costo:</span>
                  <span className="font-semibold ml-2">Bs. {list.total?.toFixed(2) || 0}</span>
                </div>
                <div className="text-sm">
                  <span className="text-gray-600">Categorías:</span>
                  <span className="font-semibold ml-2">{uniqueCategories.size}</span>
                </div>
              </div>

              <div className="flex flex-wrap gap-1 mb-4">
                {list.productos?.slice(0, 3).map((prod: any, idx: number) => (
                  <Badge key={idx} variant="secondary" className="text-xs">
                    {prod.nombre.substring(0, 15)}...
                  </Badge>
                ))}
                {(list.productos?.length || 0) > 3 && (
                  <Badge variant="outline" className="text-xs">
                    +{list.productos.length - 3}
                  </Badge>
                )}
              </div>

              <Button onClick={() => onSelectList(listType.shortKey)} disabled={loading} className="w-full" size="sm">
                {loading ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Procesando...
                  </>
                ) : (
                  "Seleccionar"
                )}
              </Button>
            </Card>
          )
        })}
      </div>
    </Card>
  )
}
