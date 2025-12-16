"use client"

import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { CheckCircle2, Circle, Loader2 } from "lucide-react"

interface AgentStatusProps {
  stage: string
  budget: string
  collectedProducts: any[]
  currentCashier: string
}

export function AgentStatus({ stage, budget, collectedProducts, currentCashier }: AgentStatusProps) {
  const stages = [
    { id: "budget", label: "Presupuesto", icon: Circle },
    { id: "product-list", label: "Lista de Productos", icon: Circle },
    { id: "shopping", label: "Recolección", icon: Circle },
    { id: "checkout", label: "Pago en Cajero", icon: Circle },
    { id: "complete", label: "Completado", icon: Circle },
  ]

  const getStageIndex = (stageId: string) => stages.findIndex((s) => s.id === stageId)
  const currentIndex = getStageIndex(stage)

  return (
    <Card className="p-6">
      <h2 className="text-lg font-semibold mb-4">Estado del Agente</h2>

      <div className="space-y-3">
        {stages.map((s, index) => {
          const isComplete = index < currentIndex
          const isCurrent = index === currentIndex
          const Icon = isComplete ? CheckCircle2 : isCurrent ? Loader2 : Circle

          return (
            <div key={s.id} className="flex items-center gap-3">
              <Icon
                className={`w-5 h-5 ${
                  isComplete ? "text-green-600" : isCurrent ? "text-blue-600 animate-spin" : "text-gray-300"
                }`}
              />
              <span
                className={`text-sm ${
                  isComplete
                    ? "text-green-900 font-medium"
                    : isCurrent
                      ? "text-blue-900 font-semibold"
                      : "text-gray-500"
                }`}
              >
                {s.label}
              </span>
            </div>
          )
        })}
      </div>

      {budget && (
        <div className="mt-6 pt-6 border-t">
          <h3 className="text-sm font-semibold mb-3">Información</h3>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-600">Presupuesto:</span>
              <span className="font-medium">Bs. {budget}</span>
            </div>
            {collectedProducts.length > 0 && (
              <div className="flex justify-between">
                <span className="text-gray-600">Productos:</span>
                <span className="font-medium">{collectedProducts.length}</span>
              </div>
            )}
            {currentCashier && (
              <div className="flex justify-between">
                <span className="text-gray-600">Cajero:</span>
                <Badge variant="outline">{currentCashier}</Badge>
              </div>
            )}
          </div>
        </div>
      )}
    </Card>
  )
}
