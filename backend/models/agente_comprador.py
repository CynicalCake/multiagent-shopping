"""
Agente Comprador (Goal-Based Agent)
Agente inteligente que genera listas de compras, navega por la sucursal
recolectando productos y se comunica con cajeros.
"""

import json
import os
from typing import List, Dict, Tuple, Optional
from utils.algoritmos_busqueda import BusquedaAEstrella, BusquedaCostoUniforme, TempleSimulado


class AgenteComprador:
    """
    Agente basado en objetivos que:
    1. Genera tres listas de compras usando Temple Simulado
    2. Navega por la sucursal usando A*
    3. Recolecta productos según la lista seleccionada
    4. Se comunica con el cajero más cercano usando Búsqueda de Costo Uniforme
    
    PEAS:
    - Performance: Minimizar distancia, maximizar variedad, cumplir presupuesto
    - Environment: Mapa de sucursal, inventario, cajeros, vale
    - Actuators: Moverse, recolectar productos, enviar mensajes
    - Sensors: Posición actual, inventario, ubicaciones, presupuesto
    """
    
    def __init__(self, comprador_id: str):
        """
        Inicializa el agente comprador.
        
        Args:
            comprador_id: Identificador único del comprador
        """
        self.comprador_id = comprador_id
        
        # Estado interno del agente
        self.sucursal_id = None
        self.vale_presupuesto = None
        self.posicion_actual = None
        
        # Datos del entorno
        self.mapa_sucursal = None
        self.inventario_sucursal = None
        self.dimensiones = None
        self.obstaculos = set()
        
        # Listas generadas
        self.lista_exacta = None
        self.lista_superior = None
        self.lista_inferior = None
        self.lista_seleccionada = None
        
        # Estado de recolección
        self.productos_recolectados = []
        self.productos_pendientes = []
        self.ruta_actual = []
        self.distancia_total_recorrida = 0
        
        # Objetivos y estado
        self.objetivo_actual = "disponible"  # disponible, planificando, esperando_usuario, recolectando, buscando_cajero, en_caja, finalizado
        self.estado_planificacion = {
            "listas_generadas": False,
            "lista_seleccionada": False,
            "productos_recolectados": False,
            "cajero_contactado": False
        }
        
        # Algoritmos de búsqueda
        self.a_estrella = BusquedaAEstrella()
        self.busqueda_costo_uniforme = BusquedaCostoUniforme()
        self.temple_simulado = TempleSimulado(
            temperatura_inicial=1000.0,
            temperatura_minima=1.0,
            factor_enfriamiento=0.95,
            iteraciones_por_temperatura=100
        )
        
        # Canal de comunicación (se asigna cuando entra a sucursal)
        self.canal_comunicacion = None
        
        print(f"[Agente Comprador {self.comprador_id}] Inicializado y disponible")
    
    # ========== PERCEPCIÓN DEL ENTORNO ==========
    
    def _cargar_mapa(self, sucursal_id: str) -> Dict:
        """
        Sensor: Percibe el mapa de la sucursal.
        
        Args:
            sucursal_id: ID de la sucursal
            
        Returns:
            Diccionario con información del mapa
        """
        ruta_mapa = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'data', 'mapas', f'{sucursal_id}.json'
        )
        
        try:
            with open(ruta_mapa, 'r', encoding='utf-8') as archivo:
                return json.load(archivo)
        except FileNotFoundError:
            raise ValueError(f"Mapa no encontrado para sucursal {sucursal_id}")
        except json.JSONDecodeError:
            raise ValueError(f"Error al decodificar mapa de {sucursal_id}")
    
    def _cargar_inventario(self, sucursal_id: str) -> Dict:
        """
        Sensor: Percibe el inventario de la sucursal.
        
        Args:
            sucursal_id: ID de la sucursal
            
        Returns:
            Diccionario con información del inventario
        """
        ruta_inventario = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'data', 'inventario', f'{sucursal_id}.json'
        )
        
        try:
            with open(ruta_inventario, 'r', encoding='utf-8') as archivo:
                return json.load(archivo)
        except FileNotFoundError:
            raise ValueError(f"Inventario no encontrado para sucursal {sucursal_id}")
        except json.JSONDecodeError:
            raise ValueError(f"Error al decodificar inventario de {sucursal_id}")
    
    def _procesar_mapa(self):
        """
        Procesa el mapa para extraer información relevante.
        """
        # Extraer dimensiones
        self.dimensiones = (
            self.mapa_sucursal['dimensiones']['filas'],
            self.mapa_sucursal['dimensiones']['columnas']
        )
        
        # Extraer obstáculos
        self.obstaculos = set()
        if 'obstaculos' in self.mapa_sucursal:
            for obs in self.mapa_sucursal['obstaculos']:
                self.obstaculos.add((obs['fila'], obs['columna']))
        
        # Extraer entrada
        entrada = self.mapa_sucursal['entrada']
        self.posicion_entrada = (entrada['fila'], entrada['columna'])
    
    # ========== ACCIONES (ACTUADORES) ==========
    
    def ingresar_a_sucursal(
        self, 
        sucursal_id: str, 
        presupuesto: float,
        canal_comunicacion=None
    ) -> Dict:
        """
        Acción: El comprador ingresa a la sucursal con un vale.
        
        Args:
            sucursal_id: ID de la sucursal
            presupuesto: Presupuesto del vale en Bs.
            canal_comunicacion: Canal para comunicarse con cajeros
            
        Returns:
            Estado del agente tras ingresar
        """
        print(f"\n[Agente Comprador {self.comprador_id}] Ingresando a sucursal {sucursal_id}")
        print(f"  Presupuesto del vale: {presupuesto} Bs.")
        
        # Actualizar estado
        self.sucursal_id = sucursal_id
        self.vale_presupuesto = presupuesto
        self.canal_comunicacion = canal_comunicacion
        
        # Cargar mapa e inventario (percepción)
        self.mapa_sucursal = self._cargar_mapa(sucursal_id)
        self.inventario_sucursal = self._cargar_inventario(sucursal_id)
        self._procesar_mapa()
        
        # Posicionarse en la entrada
        self.posicion_actual = self.posicion_entrada
        
        # Cambiar objetivo
        self.objetivo_actual = "en_sucursal"
        
        print(f"  Posición inicial: {self.posicion_actual}")
        print(f"  Productos disponibles: {len(self.inventario_sucursal['productos'])}")
        
        return {
            "comprador_id": self.comprador_id,
            "sucursal_id": self.sucursal_id,
            "posicion": self.posicion_actual,
            "estado": self.objetivo_actual,
            "productos_disponibles": len(self.inventario_sucursal['productos'])
        }
    
    def generar_listas_compras(self) -> Dict:
        """
        Acción: Genera tres listas de compras usando Temple Simulado.
        
        Planificación:
        - Lista exacta: 100% del presupuesto (±0.2%)
        - Lista superior: 100-105% del presupuesto
        - Lista inferior: 95-100% del presupuesto
        
        Returns:
            Diccionario con las tres listas generadas
        """
        print(f"\n[Agente Comprador {self.comprador_id}] Generando listas de compras...")
        print(f"  Presupuesto: {self.vale_presupuesto} Bs.")
        
        self.objetivo_actual = "planificando"
        productos = self.inventario_sucursal['productos']
        
        # Generar lista exacta
        print("  Generando lista exacta...")
        lista_exacta_raw, costo_exacta, iter_exacta = self.temple_simulado.optimizar(
            productos, self.vale_presupuesto, tipo_lista="exacta"
        )
        self.lista_exacta = self._formatear_lista(lista_exacta_raw)
        print(f"    ✓ Costo: {costo_exacta:.2f}, Iteraciones: {iter_exacta}")
        
        # Generar lista superior
        print("  Generando lista superior...")
        lista_superior_raw, costo_superior, iter_superior = self.temple_simulado.optimizar(
            productos, self.vale_presupuesto, tipo_lista="superior"
        )
        self.lista_superior = self._formatear_lista(lista_superior_raw)
        print(f"    ✓ Costo: {costo_superior:.2f}, Iteraciones: {iter_superior}")
        
        # Generar lista inferior
        print("  Generando lista inferior...")
        lista_inferior_raw, costo_inferior, iter_inferior = self.temple_simulado.optimizar(
            productos, self.vale_presupuesto, tipo_lista="inferior"
        )
        self.lista_inferior = self._formatear_lista(lista_inferior_raw)
        print(f"    ✓ Costo: {costo_inferior:.2f}, Iteraciones: {iter_inferior}")
        
        # Actualizar estado de planificación
        self.estado_planificacion["listas_generadas"] = True
        self.objetivo_actual = "esperando_usuario"
        
        print(f"\n  Listas generadas exitosamente")
        print(f"    Lista exacta: {self.lista_exacta['total']} Bs. ({len(self.lista_exacta['productos'])} productos)")
        print(f"    Lista superior: {self.lista_superior['total']} Bs. ({len(self.lista_superior['productos'])} productos)")
        print(f"    Lista inferior: {self.lista_inferior['total']} Bs. ({len(self.lista_inferior['productos'])} productos)")
        
        return {
            "comprador_id": self.comprador_id,
            "lista_exacta": self.lista_exacta,
            "lista_superior": self.lista_superior,
            "lista_inferior": self.lista_inferior,
            "presupuesto": self.vale_presupuesto
        }
    
    def _formatear_lista(self, lista_raw: List[Tuple[Dict, int]]) -> Dict:
        """
        Formatea la lista raw del Temple Simulado a formato presentable.
        
        Args:
            lista_raw: Lista de tuplas (producto, cantidad)
            
        Returns:
            Diccionario formateado con productos y total
        """
        productos_formateados = []
        total = 0.0
        
        for producto, cantidad in lista_raw:
            subtotal = producto['precio'] * cantidad
            productos_formateados.append({
                "producto_id": producto['id'],
                "nombre": producto['nombre'],
                "precio": producto['precio'],
                "cantidad": cantidad,
                "subtotal": subtotal,
                "categoria": producto['categoria']
            })
            total += subtotal
        
        return {
            "productos": productos_formateados,
            "total": round(total, 2),
            "cantidad_items": len(productos_formateados)
        }
    
    def seleccionar_lista(self, tipo_lista: str) -> Dict:
        """
        Acción: Usuario selecciona una de las tres listas.
        
        Args:
            tipo_lista: "exacta", "superior" o "inferior"
            
        Returns:
            Lista seleccionada y productos a recolectar
        """
        print(f"\n[Agente Comprador {self.comprador_id}] Usuario seleccionó lista: {tipo_lista}")
        
        if tipo_lista == "exacta":
            self.lista_seleccionada = self.lista_exacta
        elif tipo_lista == "superior":
            self.lista_seleccionada = self.lista_superior
        elif tipo_lista == "inferior":
            self.lista_seleccionada = self.lista_inferior
        else:
            raise ValueError(f"Tipo de lista inválido: {tipo_lista}")
        
        # Preparar lista de productos pendientes
        self.productos_pendientes = self.lista_seleccionada['productos'].copy()
        self.estado_planificacion["lista_seleccionada"] = True
        self.objetivo_actual = "listo_para_recolectar"
        
        print(f"  Total a recolectar: {len(self.productos_pendientes)} productos")
        print(f"  Monto total: {self.lista_seleccionada['total']} Bs.")
        
        return {
            "comprador_id": self.comprador_id,
            "lista_seleccionada": self.lista_seleccionada,
            "productos_pendientes": len(self.productos_pendientes)
        }
    
    def iniciar_recoleccion(self) -> Dict:
        """
        Acción: Inicia el proceso de recolección de productos.
        Planifica las rutas usando A*.
        
        Returns:
            Plan de recolección con rutas
        """
        print(f"\n[Agente Comprador {self.comprador_id}] Iniciando recolección de productos...")
        
        self.objetivo_actual = "recolectando"
        plan_recoleccion = []
        distancia_total_planificada = 0
        
        posicion_origen = self.posicion_actual
        
        for idx, producto_item in enumerate(self.productos_pendientes):
            producto_id = producto_item['producto_id']
            cantidad = producto_item['cantidad']
            
            # Encontrar ubicación del producto
            ubicacion_producto = self._buscar_ubicacion_producto(producto_id)
            
            if ubicacion_producto is None:
                print(f"  ⚠ Producto {producto_id} no encontrado en mapa, omitiendo...")
                continue
            
            # Calcular ruta con A*
            print(f"  [{idx + 1}/{len(self.productos_pendientes)}] Planificando ruta a {producto_item['nombre']}...")
            ruta, distancia = self.a_estrella.buscar(
                inicio=posicion_origen,
                objetivo=ubicacion_producto,
                dimensiones=self.dimensiones,
                obstaculos=self.obstaculos,
                usar_manhattan=True
            )
            
            if not ruta:
                print(f"    ✗ No se encontró ruta al producto")
                continue
            
            print(f"    ✓ Ruta encontrada: {distancia} pasos")
            
            plan_recoleccion.append({
                "producto_id": producto_id,
                "nombre": producto_item['nombre'],
                "cantidad": cantidad,
                "ubicacion": ubicacion_producto,
                "ruta": ruta,
                "distancia": distancia,
                "origen": posicion_origen,
                "destino": ubicacion_producto
            })
            
            distancia_total_planificada += distancia
            posicion_origen = ubicacion_producto  # Siguiente origen
        
        print(f"\n  Plan de recolección completado")
        print(f"  Productos en ruta: {len(plan_recoleccion)}")
        print(f"  Distancia total estimada: {distancia_total_planificada} pasos")
        
        return {
            "comprador_id": self.comprador_id,
            "plan_recoleccion": plan_recoleccion,
            "distancia_total_planificada": distancia_total_planificada,
            "productos_en_plan": len(plan_recoleccion)
        }
    
    def ejecutar_recoleccion(self, plan_recoleccion: List[Dict]) -> Dict:
        """
        Acción: Ejecuta el plan de recolección (simula movimiento y recolección).
        
        Args:
            plan_recoleccion: Plan generado por iniciar_recoleccion
            
        Returns:
            Resultado de la recolección
        """
        print(f"\n[Agente Comprador {self.comprador_id}] Ejecutando recolección...")
        
        self.productos_recolectados = []
        self.distancia_total_recorrida = 0
        
        for idx, item in enumerate(plan_recoleccion):
            print(f"  [{idx + 1}/{len(plan_recoleccion)}] Recolectando {item['nombre']}...")
            
            # Simular movimiento por la ruta
            for posicion in item['ruta']:
                self.posicion_actual = posicion
                self.distancia_total_recorrida += 1
            
            # Recolectar producto
            self.productos_recolectados.append({
                "producto_id": item['producto_id'],
                "nombre": item['nombre'],
                "cantidad": item['cantidad'],
                "ubicacion_recoleccion": item['ubicacion']
            })
            
            print(f"    ✓ Recolectado en posición {item['ubicacion']}")
        
        self.estado_planificacion["productos_recolectados"] = True
        self.objetivo_actual = "productos_completos"
        
        print(f"\n  Recolección completada")
        print(f"  Productos recolectados: {len(self.productos_recolectados)}")
        print(f"  Distancia recorrida: {self.distancia_total_recorrida} pasos")
        
        return {
            "comprador_id": self.comprador_id,
            "productos_recolectados": self.productos_recolectados,
            "distancia_recorrida": self.distancia_total_recorrida,
            "posicion_actual": self.posicion_actual
        }
    
    def buscar_cajero_mas_cercano(self) -> Dict:
        """
        Acción: Busca el cajero más cercano usando Búsqueda de Costo Uniforme.
        
        Returns:
            Información del cajero más cercano y ruta
        """
        print(f"\n[Agente Comprador {self.comprador_id}] Buscando cajero más cercano...")
        
        self.objetivo_actual = "buscando_cajero"
        
        # Obtener posiciones de cajeros
        cajeros = self.mapa_sucursal.get('cajeros', [])
        if not cajeros:
            raise ValueError("No hay cajeros disponibles en la sucursal")
        
        posiciones_cajeros = [(c['fila'], c['columna']) for c in cajeros]
        
        # Buscar cajero más cercano con Búsqueda de Costo Uniforme
        cajero_pos, ruta, distancia = self.busqueda_costo_uniforme.buscar_mas_cercano(
            inicio=self.posicion_actual,
            objetivos=posiciones_cajeros,
            dimensiones=self.dimensiones,
            obstaculos=self.obstaculos
        )
        
        if cajero_pos is None:
            raise ValueError("No se pudo encontrar ruta a ningún cajero")
        
        # Identificar cajero
        cajero_seleccionado = None
        for cajero in cajeros:
            if (cajero['fila'], cajero['columna']) == cajero_pos:
                cajero_seleccionado = cajero
                break
        
        print(f"  ✓ Cajero más cercano: {cajero_seleccionado['id']}")
        print(f"  Distancia: {distancia} pasos")
        print(f"  Posición: {cajero_pos}")
        
        return {
            "comprador_id": self.comprador_id,
            "cajero": cajero_seleccionado,
            "ruta_a_cajero": ruta,
            "distancia_a_cajero": distancia
        }
    
    def moverse_a_cajero(self, ruta_a_cajero: List[Tuple[int, int]]) -> Dict:
        """
        Acción: Se mueve hasta el cajero seleccionado.
        
        Args:
            ruta_a_cajero: Ruta calculada al cajero
            
        Returns:
            Estado tras llegar al cajero
        """
        print(f"\n[Agente Comprador {self.comprador_id}] Moviéndose al cajero...")
        
        # Simular movimiento
        distancia_recorrida = 0
        for posicion in ruta_a_cajero:
            self.posicion_actual = posicion
            distancia_recorrida += 1
        
        self.distancia_total_recorrida += distancia_recorrida
        self.objetivo_actual = "en_cajero"
        
        print(f"  ✓ Llegó al cajero")
        print(f"  Posición: {self.posicion_actual}")
        print(f"  Distancia total recorrida en sucursal: {self.distancia_total_recorrida} pasos")
        
        return {
            "comprador_id": self.comprador_id,
            "posicion_actual": self.posicion_actual,
            "distancia_total": self.distancia_total_recorrida,
            "estado": self.objetivo_actual
        }
    
    def comunicar_con_cajero(self, cajero_id: str) -> Dict:
        """
        Acción: Envía mensaje al cajero específico con la lista de productos.
        
        Args:
            cajero_id: ID del cajero a contactar
            
        Returns:
            Mensaje enviado
        """
        print(f"\n[Agente Comprador {self.comprador_id}] Comunicándose con {cajero_id}...")
        
        # Preparar mensaje para el cajero
        mensaje = {
            "tipo": "pedido_procesamiento",
            "comprador_id": self.comprador_id,
            "cajero_id": cajero_id,
            "productos": self.productos_recolectados,
            "total_esperado": self.lista_seleccionada['total']
        }
        
        # Enviar mensaje por el canal
        if self.canal_comunicacion:
            self.canal_comunicacion.enviar_mensaje(cajero_id, mensaje)
        
        self.estado_planificacion["cajero_contactado"] = True
        self.objetivo_actual = "esperando_cajero"
        
        print(f"  ✓ Mensaje enviado a {cajero_id}")
        print(f"  Productos en mensaje: {len(self.productos_recolectados)}")
        
        return mensaje
    
    def recibir_factura(self, factura: Dict) -> Dict:
        """
        Sensor: Recibe la factura del cajero.
        
        Args:
            factura: Factura generada por el cajero
            
        Returns:
            Estado final del comprador
        """
        print(f"\n[Agente Comprador {self.comprador_id}] Factura recibida")
        print(f"  Total facturado: {factura['total']} Bs.")
        print(f"  Cajero: {factura['cajero_id']}")
        
        self.objetivo_actual = "finalizado"
        
        return {
            "comprador_id": self.comprador_id,
            "estado": "finalizado",
            "factura": factura,
            "productos_comprados": len(factura['items']),
            "distancia_total_recorrida": self.distancia_total_recorrida
        }
    
    # ========== MÉTODOS AUXILIARES ==========
    
    def _buscar_ubicacion_producto(self, producto_id: int) -> Optional[Tuple[int, int]]:
        """
        Busca la ubicación de un producto en el mapa.
        
        Args:
            producto_id: ID del producto
            
        Returns:
            Tupla (fila, columna) o None si no se encuentra
        """
        # Buscar en zonas_productos del mapa
        zonas = self.mapa_sucursal.get('zonas_productos', {})
        
        for zona_nombre, zona_info in zonas.items():
            if producto_id in zona_info.get('productos', []):
                return (zona_info['fila'], zona_info['columna'])
        
        # Buscar en el inventario si tiene ubicación directa
        for producto in self.inventario_sucursal['productos']:
            if producto['id'] == producto_id:
                if 'ubicacion' in producto:
                    return (producto['ubicacion']['fila'], producto['ubicacion']['columna'])
        
        return None
    
    def obtener_estado(self) -> Dict:
        """
        Obtiene el estado completo del agente.
        
        Returns:
            Estado completo
        """
        return {
            "comprador_id": self.comprador_id,
            "sucursal_id": self.sucursal_id,
            "objetivo_actual": self.objetivo_actual,
            "posicion_actual": self.posicion_actual,
            "productos_recolectados": len(self.productos_recolectados),
            "productos_pendientes": len(self.productos_pendientes),
            "distancia_recorrida": self.distancia_total_recorrida,
            "estado_planificacion": self.estado_planificacion
        }
