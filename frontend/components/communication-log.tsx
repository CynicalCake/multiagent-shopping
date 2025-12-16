"use client"

import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import { useEffect, useRef } from "react"

interface Message {
  timestamp: string
  from: string
  to: string
  type: string
  content: string
}

interface CommunicationLogProps {
  messages: Message[]
}

export function CommunicationLog({ messages }: CommunicationLogProps) {
  const scrollRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [messages])

  const getTypeColor = (type: string) => {
    switch (type) {
      case "success":
        return "bg-green-100 text-green-800 border-green-200"
      case "error":
        return "bg-red-100 text-red-800 border-red-200"
      case "communication":
        return "bg-blue-100 text-blue-800 border-blue-200"
      case "selection":
        return "bg-purple-100 text-purple-800 border-purple-200"
      default:
        return "bg-gray-100 text-gray-800 border-gray-200"
    }
  }

  return (
    <Card className="p-6">
      <h2 className="text-lg font-semibold mb-4">Registro de Comunicación</h2>

      <ScrollArea className="h-96" ref={scrollRef}>
        <div className="space-y-3">
          {messages.length === 0 ? (
            <p className="text-sm text-gray-500 text-center py-8">No hay mensajes aún</p>
          ) : (
            messages.map((message, index) => (
              <div key={index} className={`p-3 rounded-lg border ${getTypeColor(message.type)}`}>
                <div className="flex items-center justify-between mb-1">
                  <div className="flex items-center gap-2">
                    <Badge variant="outline" className="text-xs">
                      {message.from}
                    </Badge>
                    <span className="text-xs text-gray-600">→</span>
                    <Badge variant="outline" className="text-xs">
                      {message.to}
                    </Badge>
                  </div>
                  <span className="text-xs text-gray-500">{message.timestamp}</span>
                </div>
                <p className="text-sm">{message.content}</p>
              </div>
            ))
          )}
        </div>
      </ScrollArea>
    </Card>
  )
}
