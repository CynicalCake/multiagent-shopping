"""
Sistema de Comunicación entre Agentes
Implementa el canal de comunicación para que el comprador pueda
hablar directamente con cajeros específicos.
"""

from typing import Dict, Callable, Optional
from collections import defaultdict


class CanalComunicacion:
    """
    Canal de comunicación por sucursal que permite comunicación
    directa entre agente comprador y agente cajero.
    
    Características:
    - Cada sucursal tiene su propio canal
    - Los cajeros se registran en el canal
    - El comprador envía mensaje a un cajero específico usando su ID
    - Solo el cajero con ese ID procesa el mensaje
    """
    
    def __init__(self, sucursal_id: str):
        """
        Inicializa el canal de comunicación para una sucursal.
        
        Args:
            sucursal_id: ID de la sucursal
        """
        self.sucursal_id = sucursal_id
        
        # Diccionario de cajeros registrados: {cajero_id: instancia_agente_cajero}
        self.cajeros_registrados = {}
        
        # Callbacks para respuestas: {comprador_id: callback}
        self.callbacks_compradores = {}
        
        # Historial de mensajes (para debugging)
        self.historial_mensajes = []
        
        print(f"[Canal Comunicación] Inicializado para sucursal {sucursal_id}")
    
    def registrar_cajero(self, agente_cajero) -> bool:
        """
        Registra un cajero en el canal de comunicación.
        El cajero podrá escuchar mensajes dirigidos a su ID.
        
        Args:
            agente_cajero: Instancia de AgenteCajero
            
        Returns:
            True si se registró exitosamente
        """
        cajero_id = agente_cajero.cajero_id
        
        if cajero_id in self.cajeros_registrados:
            print(f"[Canal Comunicación] ⚠ Cajero {cajero_id} ya está registrado")
            return False
        
        self.cajeros_registrados[cajero_id] = agente_cajero
        
        # Registrar callback para que el cajero pueda responder
        agente_cajero.registrar_callback_respuesta(self._recibir_respuesta_cajero)
        
        print(f"[Canal Comunicación] ✓ Cajero {cajero_id} registrado en {self.sucursal_id}")
        return True
    
    def desregistrar_cajero(self, cajero_id: str) -> bool:
        """
        Desregistra un cajero del canal.
        
        Args:
            cajero_id: ID del cajero a desregistrar
            
        Returns:
            True si se desregistró exitosamente
        """
        if cajero_id not in self.cajeros_registrados:
            print(f"[Canal Comunicación] ⚠ Cajero {cajero_id} no está registrado")
            return False
        
        del self.cajeros_registrados[cajero_id]
        print(f"[Canal Comunicación] ✓ Cajero {cajero_id} desregistrado")
        return True
    
    def registrar_comprador(self, comprador_id: str, callback_factura: Callable):
        """
        Registra un comprador para recibir respuestas (facturas).
        
        Args:
            comprador_id: ID del comprador
            callback_factura: Función que recibe la factura
        """
        self.callbacks_compradores[comprador_id] = callback_factura
        print(f"[Canal Comunicación] ✓ Comprador {comprador_id} registrado para respuestas")
    
    def enviar_mensaje(self, cajero_id: str, mensaje: Dict) -> bool:
        """
        Envía un mensaje del comprador a un cajero específico.
        El mensaje se entrega directamente al cajero identificado.
        
        Args:
            cajero_id: ID del cajero destinatario
            mensaje: Diccionario con el mensaje (debe incluir cajero_id)
            
        Returns:
            True si el mensaje fue entregado
        """
        comprador_id = mensaje.get('comprador_id', 'desconocido')
        
        print(f"\n[Canal Comunicación] Mensaje de {comprador_id} → {cajero_id}")
        
        # Verificar que el cajero está registrado
        if cajero_id not in self.cajeros_registrados:
            print(f"  ✗ Cajero {cajero_id} no está registrado en el canal")
            return False
        
        # Guardar en historial
        self.historial_mensajes.append({
            "tipo": "comprador_a_cajero",
            "comprador_id": comprador_id,
            "cajero_id": cajero_id,
            "mensaje": mensaje
        })
        
        # Entregar mensaje al cajero específico
        agente_cajero = self.cajeros_registrados[cajero_id]
        print(f"  ✓ Mensaje entregado a cajero {cajero_id}")
        
        # El cajero procesa el mensaje (ejecuta su tabla REAS)
        factura = agente_cajero.escuchar_mensaje(mensaje)
        
        return True
    
    def _recibir_respuesta_cajero(self, comprador_id: str, factura: Dict):
        """
        Callback interno: recibe respuesta del cajero y la envía al comprador.
        
        Args:
            comprador_id: ID del comprador destinatario
            factura: Factura o mensaje de error del cajero
        """
        cajero_id = factura.get('cajero_id', 'desconocido')
        
        print(f"\n[Canal Comunicación] Respuesta de {cajero_id} → {comprador_id}")
        
        # Guardar en historial
        self.historial_mensajes.append({
            "tipo": "cajero_a_comprador",
            "cajero_id": cajero_id,
            "comprador_id": comprador_id,
            "mensaje": factura
        })
        
        # Enviar al comprador si tiene callback registrado
        if comprador_id in self.callbacks_compradores:
            callback = self.callbacks_compradores[comprador_id]
            callback(factura)
            print(f"  ✓ Factura entregada a comprador {comprador_id}")
        else:
            print(f"  ⚠ Comprador {comprador_id} no tiene callback registrado")
    
    def obtener_cajeros_disponibles(self) -> list:
        """
        Obtiene la lista de cajeros disponibles en el canal.
        
        Returns:
            Lista de IDs de cajeros disponibles
        """
        disponibles = []
        for cajero_id, agente in self.cajeros_registrados.items():
            if agente.estado == "disponible":
                disponibles.append(cajero_id)
        return disponibles
    
    def obtener_estadisticas(self) -> Dict:
        """
        Obtiene estadísticas del canal.
        
        Returns:
            Diccionario con estadísticas
        """
        return {
            "sucursal_id": self.sucursal_id,
            "cajeros_registrados": len(self.cajeros_registrados),
            "cajeros_disponibles": len(self.obtener_cajeros_disponibles()),
            "mensajes_totales": len(self.historial_mensajes),
            "compradores_registrados": len(self.callbacks_compradores)
        }
    
    def limpiar_historial(self):
        """Limpia el historial de mensajes"""
        self.historial_mensajes = []
        print(f"[Canal Comunicación] Historial limpiado")


class GestorCanales:
    """
    Gestor global de canales de comunicación.
    Mantiene un canal por sucursal y facilita el acceso a ellos.
    """
    
    def __init__(self):
        """Inicializa el gestor de canales"""
        # Diccionario: {sucursal_id: CanalComunicacion}
        self.canales = {}
        print("[Gestor Canales] Inicializado")
    
    def obtener_canal(self, sucursal_id: str) -> CanalComunicacion:
        """
        Obtiene el canal de comunicación de una sucursal.
        Si no existe, lo crea automáticamente.
        
        Args:
            sucursal_id: ID de la sucursal
            
        Returns:
            Canal de comunicación de la sucursal
        """
        if sucursal_id not in self.canales:
            canal = CanalComunicacion(sucursal_id)
            self.canales[sucursal_id] = canal
            print(f"[Gestor Canales] Nuevo canal creado para {sucursal_id}")
        
        return self.canales[sucursal_id]
    
    def registrar_cajero_en_sucursal(self, sucursal_id: str, agente_cajero) -> bool:
        """
        Registra un cajero en el canal de su sucursal.
        
        Args:
            sucursal_id: ID de la sucursal
            agente_cajero: Instancia del agente cajero
            
        Returns:
            True si se registró exitosamente
        """
        canal = self.obtener_canal(sucursal_id)
        return canal.registrar_cajero(agente_cajero)
    
    def registrar_comprador_en_sucursal(
        self, 
        sucursal_id: str, 
        comprador_id: str, 
        callback_factura: Callable
    ):
        """
        Registra un comprador en el canal de su sucursal.
        
        Args:
            sucursal_id: ID de la sucursal
            comprador_id: ID del comprador
            callback_factura: Callback para recibir factura
        """
        canal = self.obtener_canal(sucursal_id)
        canal.registrar_comprador(comprador_id, callback_factura)
    
    def obtener_estadisticas_global(self) -> Dict:
        """
        Obtiene estadísticas globales de todos los canales.
        
        Returns:
            Estadísticas de todos los canales
        """
        stats = {
            "total_canales": len(self.canales),
            "canales": {}
        }
        
        for sucursal_id, canal in self.canales.items():
            stats["canales"][sucursal_id] = canal.obtener_estadisticas()
        
        return stats


# ========== INSTANCIA GLOBAL ==========
# Instancia única del gestor de canales para toda la aplicación
gestor_canales_global = GestorCanales()
