"""
Agente Cajero (Simple Reflex Agent)
Agente reactivo simple que escucha mensajes de compradores,
procesa productos y genera facturas.
"""

import json
import os
from typing import Dict, Callable, Optional


class AgenteCajero:
    """
    Agente reflexivo simple que:
    1. Escucha mensajes del canal de comunicación
    2. Detecta si el mensaje es para él (mediante su ID)
    3. Procesa la lista de productos
    4. Genera y envía factura
    
    PEAS:
    - Performance: Procesar pedidos correctamente, tiempo de respuesta rápido
    - Environment: Canal de comunicación, inventario de precios, cola de mensajes
    - Actuators: Escuchar, validar productos, calcular totales, generar facturas
    - Sensors: Detector de mensajes con su ID, lector de lista de productos
    
    Tabla REAS (Reglas Condición-Acción):
    | Percepción                                  | Acción                              |
    |---------------------------------------------|-------------------------------------|
    | mensaje_recibido(mi_id) ∧ disponible       | cambiar_estado(procesando) →        |
    |                                             | procesar_pedido()                   |
    | mensaje_recibido(otro_id)                   | ignorar_mensaje()                   |
    | procesando ∧ productos_válidos             | calcular_total() → generar_factura()|
    | procesando ∧ producto_no_existe            | generar_error()                     |
    | procesando ∧ factura_generada              | enviar_respuesta() →                |
    |                                             | cambiar_estado(disponible)          |
    | sin_mensajes ∧ disponible                  | esperar()                           |
    """
    
    def __init__(self, cajero_id: str, sucursal_id: str, posicion: Dict):
        """
        Inicializa el agente cajero.
        
        Args:
            cajero_id: Identificador único del cajero (ej: "CAJ001")
            sucursal_id: ID de la sucursal donde está el cajero
            posicion: Diccionario con {"fila": int, "columna": int}
        """
        self.cajero_id = cajero_id
        self.sucursal_id = sucursal_id
        self.posicion = (posicion['fila'], posicion['columna'])
        
        # Estado interno (Simple Reflex Agent tiene estado mínimo)
        self.estado = "disponible"  # disponible, procesando
        
        # Inventario de precios (cargado del archivo)
        self.inventario_precios = {}
        self._cargar_inventario()
        
        # Callback para enviar respuestas
        self.callback_respuesta = None
        
        # Estadísticas
        self.pedidos_procesados = 0
        self.total_facturado = 0.0
        
        print(f"[Agente Cajero {self.cajero_id}] Inicializado en sucursal {sucursal_id}")
        print(f"  Posición: {self.posicion}")
        print(f"  Estado: {self.estado}")
        print(f"  Productos en inventario: {len(self.inventario_precios)}")
    
    # ========== PERCEPCIÓN ==========
    
    def _cargar_inventario(self):
        """
        Carga el inventario de precios desde el archivo JSON.
        """
        ruta_inventario = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'data', 'inventario', f'{self.sucursal_id}.json'
        )
        
        try:
            with open(ruta_inventario, 'r', encoding='utf-8') as archivo:
                data = json.load(archivo)
                # Crear diccionario producto_id -> precio
                for producto in data.get('productos', []):
                    self.inventario_precios[producto['id']] = {
                        'nombre': producto['nombre'],
                        'precio': producto['precio'],
                        'categoria': producto['categoria']
                    }
        except FileNotFoundError:
            print(f"[ERROR Cajero {self.cajero_id}] Inventario no encontrado")
            self.inventario_precios = {}
        except json.JSONDecodeError:
            print(f"[ERROR Cajero {self.cajero_id}] Error al decodificar inventario")
            self.inventario_precios = {}
    
    def registrar_callback_respuesta(self, callback: Callable):
        """
        Registra el callback para enviar respuestas al comprador.
        
        Args:
            callback: Función que recibe (comprador_id, factura)
        """
        self.callback_respuesta = callback
    
    # ========== TABLA REAS (REGLAS CONDICIÓN-ACCIÓN) ==========
    
    def escuchar_mensaje(self, mensaje: Dict) -> Optional[Dict]:
        """
        Sensor principal: Escucha mensajes del canal de comunicación.
        Ejecuta las reglas REAS según la percepción.
        
        Args:
            mensaje: Mensaje recibido del canal
            
        Returns:
            Factura generada o None si no es para este cajero
        """
        # REGLA 1: Si el mensaje NO es para mí, ignorar
        if not self._mensaje_es_para_mi(mensaje):
            return self._ignorar_mensaje(mensaje)
        
        # REGLA 2: Si el mensaje ES para mí y estoy disponible, procesar
        if self.estado == "disponible":
            return self._procesar_pedido(mensaje)
        
        # REGLA 3: Si estoy procesando, rechazar (no debería pasar)
        if self.estado == "procesando":
            print(f"[Agente Cajero {self.cajero_id}] ⚠ Ya estoy procesando otro pedido")
            return None
    
    # ========== CONDICIONES (SENSORES) ==========
    
    def _mensaje_es_para_mi(self, mensaje: Dict) -> bool:
        """
        Condición: Detecta si el mensaje contiene mi ID.
        
        Args:
            mensaje: Mensaje recibido
            
        Returns:
            True si el mensaje es para este cajero
        """
        cajero_id_mensaje = mensaje.get('cajero_id')
        return cajero_id_mensaje == self.cajero_id
    
    def _productos_son_validos(self, productos: list) -> tuple[bool, Optional[int]]:
        """
        Condición: Verifica si todos los productos existen en inventario.
        
        Args:
            productos: Lista de productos a validar
            
        Returns:
            Tupla (validos, producto_id_invalido)
        """
        for item in productos:
            producto_id = item.get('producto_id')
            if producto_id not in self.inventario_precios:
                return False, producto_id
        return True, None
    
    # ========== ACCIONES ==========
    
    def _ignorar_mensaje(self, mensaje: Dict) -> None:
        """
        Acción: Ignorar mensaje que no es para este cajero.
        
        Args:
            mensaje: Mensaje ignorado
        """
        # Simple Reflex Agent: no hace nada si la percepción no coincide
        pass
    
    def _procesar_pedido(self, mensaje: Dict) -> Optional[Dict]:
        """
        Acción: Procesa el pedido del comprador.
        
        Secuencia REAS:
        1. Cambiar estado a "procesando"
        2. Validar productos
        3. Si válidos: calcular_total() → generar_factura()
        4. Si inválidos: generar_error()
        5. Enviar respuesta
        6. Cambiar estado a "disponible"
        
        Args:
            mensaje: Mensaje del comprador con lista de productos
            
        Returns:
            Factura generada
        """
        print(f"\n[Agente Cajero {self.cajero_id}] Mensaje recibido de {mensaje.get('comprador_id')}")
        
        # Acción 1: Cambiar estado
        self.estado = "procesando"
        
        comprador_id = mensaje.get('comprador_id')
        productos = mensaje.get('productos', [])
        
        print(f"  Procesando {len(productos)} productos...")
        
        # Acción 2: Validar productos
        productos_validos, producto_invalido = self._productos_son_validos(productos)
        
        if not productos_validos:
            # Acción 3a: Generar error
            return self._generar_error(comprador_id, producto_invalido)
        
        # Acción 3b: Calcular total y generar factura
        factura = self._generar_factura(comprador_id, productos)
        
        # Acción 4: Enviar respuesta
        if self.callback_respuesta:
            self.callback_respuesta(comprador_id, factura)
        
        # Acción 5: Cambiar estado a disponible
        self.estado = "disponible"
        
        # Actualizar estadísticas
        self.pedidos_procesados += 1
        self.total_facturado += factura['total']
        
        print(f"  ✓ Factura generada: {factura['total']} Bs.")
        print(f"  Estado: {self.estado}")
        
        return factura
    
    def _generar_factura(self, comprador_id: str, productos: list) -> Dict:
        """
        Acción: Genera la factura con los productos procesados.
        
        Args:
            comprador_id: ID del comprador
            productos: Lista de productos recolectados
            
        Returns:
            Factura completa
        """
        items = []
        total = 0.0
        
        for item in productos:
            producto_id = item.get('producto_id')
            cantidad = item.get('cantidad', 1)
            
            # Obtener información del inventario
            info_producto = self.inventario_precios[producto_id]
            precio_unitario = info_producto['precio']
            subtotal = precio_unitario * cantidad
            
            items.append({
                "producto_id": producto_id,
                "nombre": info_producto['nombre'],
                "categoria": info_producto['categoria'],
                "cantidad": cantidad,
                "precio_unitario": precio_unitario,
                "subtotal": round(subtotal, 2)
            })
            
            total += subtotal
            
            print(f"    • {info_producto['nombre']} x{cantidad} = {subtotal:.2f} Bs.")
        
        factura = {
            "tipo": "factura",
            "cajero_id": self.cajero_id,
            "comprador_id": comprador_id,
            "sucursal_id": self.sucursal_id,
            "items": items,
            "total": round(total, 2),
            "cantidad_items": len(items)
        }
        
        return factura
    
    def _generar_error(self, comprador_id: str, producto_id: int) -> Dict:
        """
        Acción: Genera mensaje de error cuando producto no existe.
        
        Args:
            comprador_id: ID del comprador
            producto_id: ID del producto que causó error
            
        Returns:
            Mensaje de error
        """
        print(f"  ✗ ERROR: Producto {producto_id} no encontrado en inventario")
        
        # Cambiar estado a disponible
        self.estado = "disponible"
        
        error = {
            "tipo": "error",
            "cajero_id": self.cajero_id,
            "comprador_id": comprador_id,
            "mensaje": f"Producto {producto_id} no encontrado en inventario",
            "producto_id": producto_id
        }
        
        # Enviar error
        if self.callback_respuesta:
            self.callback_respuesta(comprador_id, error)
        
        return error
    
    # ========== MÉTODOS DE ESTADO ==========
    
    def obtener_estado(self) -> Dict:
        """
        Obtiene el estado actual del cajero.
        
        Returns:
            Estado completo del cajero
        """
        return {
            "cajero_id": self.cajero_id,
            "sucursal_id": self.sucursal_id,
            "posicion": {
                "fila": self.posicion[0],
                "columna": self.posicion[1]
            },
            "estado": self.estado,
            "pedidos_procesados": self.pedidos_procesados,
            "total_facturado": round(self.total_facturado, 2),
            "productos_en_inventario": len(self.inventario_precios)
        }
    
    def reiniciar_estadisticas(self):
        """
        Reinicia las estadísticas del cajero.
        """
        self.pedidos_procesados = 0
        self.total_facturado = 0.0
        print(f"[Agente Cajero {self.cajero_id}] Estadísticas reiniciadas")


# ========== IMPLEMENTACIÓN ALTERNATIVA: LOOP EXPLÍCITO ==========

class AgenteCajeroConLoop(AgenteCajero):
    """
    Versión alternativa del cajero con loop explícito de percepción-acción.
    Útil para entender mejor el ciclo REAS.
    """
    
    def __init__(self, cajero_id: str, sucursal_id: str, posicion: Dict):
        super().__init__(cajero_id, sucursal_id, posicion)
        self.activo = False
        self.cola_mensajes = []
    
    def agregar_mensaje_a_cola(self, mensaje: Dict):
        """
        Agrega un mensaje a la cola de percepción.
        
        Args:
            mensaje: Mensaje a procesar
        """
        self.cola_mensajes.append(mensaje)
    
    def ejecutar_ciclo_reas(self):
        """
        Ciclo explícito del agente reflexivo simple:
        
        loop:
            percepcion = PERCIBIR()
            accion = REGLA_CORRESPONDIENTE(percepcion)
            EJECUTAR(accion)
        """
        while self.activo:
            # PERCIBIR
            if not self.cola_mensajes:
                # Sin mensajes, esperar
                continue
            
            mensaje = self.cola_mensajes.pop(0)
            
            # APLICAR REGLAS
            if self._mensaje_es_para_mi(mensaje):
                if self.estado == "disponible":
                    # EJECUTAR ACCIÓN
                    self._procesar_pedido(mensaje)
            else:
                # EJECUTAR ACCIÓN
                self._ignorar_mensaje(mensaje)
    
    def iniciar(self):
        """Inicia el ciclo del agente"""
        self.activo = True
        print(f"[Agente Cajero {self.cajero_id}] Ciclo REAS iniciado")
    
    def detener(self):
        """Detiene el ciclo del agente"""
        self.activo = False
        print(f"[Agente Cajero {self.cajero_id}] Ciclo REAS detenido")
