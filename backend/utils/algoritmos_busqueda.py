"""
Algoritmos de Búsqueda para Sistema Multi-Agente
Implementa los algoritmos de búsqueda utilizados por el agente comprador.
"""

import heapq
import math
import random
from typing import List, Dict, Tuple, Set, Optional, Callable


class Nodo:
    """
    Representa un nodo en el espacio de búsqueda.
    """
    def __init__(self, posicion: Tuple[int, int], g: float = 0, h: float = 0, padre=None):
        self.posicion = posicion  # (fila, columna)
        self.g = g  # Costo desde el inicio
        self.h = h  # Heurística hasta el objetivo
        self.f = g + h  # Costo total estimado
        self.padre = padre
    
    def __lt__(self, otro):
        """Comparación para la cola de prioridad"""
        return self.f < otro.f
    
    def __eq__(self, otro):
        """Igualdad basada en posición"""
        if not isinstance(otro, Nodo):
            return False
        return self.posicion == otro.posicion
    
    def __hash__(self):
        """Hash basado en posición para usar en conjuntos"""
        return hash(self.posicion)


class BusquedaAEstrella:
    """
    Implementación del algoritmo A* para navegación en el mapa.
    Encuentra el camino óptimo desde un punto inicial hasta un objetivo.
    """
    
    def __init__(self):
        """Inicializa el algoritmo A*"""
        self.camino_encontrado = []
        self.nodos_expandidos = 0
        self.costo_total = 0
    
    def heuristica_manhattan(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """
        Calcula la distancia Manhattan entre dos posiciones.
        
        Args:
            pos1: Posición inicial (fila, columna)
            pos2: Posición objetivo (fila, columna)
            
        Returns:
            Distancia Manhattan
        """
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def heuristica_euclidiana(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """
        Calcula la distancia Euclidiana entre dos posiciones.
        
        Args:
            pos1: Posición inicial (fila, columna)
            pos2: Posición objetivo (fila, columna)
            
        Returns:
            Distancia Euclidiana
        """
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
    
    def obtener_vecinos(
        self, 
        posicion: Tuple[int, int], 
        dimensiones: Tuple[int, int], 
        obstaculos: Set[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
        """
        Obtiene las posiciones vecinas válidas (arriba, abajo, izquierda, derecha).
        
        Args:
            posicion: Posición actual (fila, columna)
            dimensiones: Dimensiones del mapa (filas, columnas)
            obstaculos: Conjunto de posiciones con obstáculos
            
        Returns:
            Lista de posiciones vecinas válidas
        """
        fila, columna = posicion
        filas_max, columnas_max = dimensiones
        
        # Movimientos: arriba, abajo, izquierda, derecha
        movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        vecinos = []
        
        for df, dc in movimientos:
            nueva_fila = fila + df
            nueva_col = columna + dc
            nueva_pos = (nueva_fila, nueva_col)
            
            # Verificar límites
            if 0 <= nueva_fila < filas_max and 0 <= nueva_col < columnas_max:
                # Verificar que no sea obstáculo
                if nueva_pos not in obstaculos:
                    vecinos.append(nueva_pos)
        
        return vecinos
    
    def buscar(
        self,
        inicio: Tuple[int, int],
        objetivo: Tuple[int, int],
        dimensiones: Tuple[int, int],
        obstaculos: Set[Tuple[int, int]],
        usar_manhattan: bool = True
    ) -> Tuple[List[Tuple[int, int]], float]:
        """
        Ejecuta el algoritmo A* para encontrar el camino óptimo.
        
        Args:
            inicio: Posición inicial (fila, columna)
            objetivo: Posición objetivo (fila, columna)
            dimensiones: Dimensiones del mapa (filas, columnas)
            obstaculos: Conjunto de posiciones bloqueadas
            usar_manhattan: Si True usa Manhattan, si False usa Euclidiana
            
        Returns:
            Tupla (camino, costo) donde camino es lista de posiciones
        """
        # Inicializar estadísticas
        self.nodos_expandidos = 0
        self.camino_encontrado = []
        self.costo_total = 0
        
        # Elegir heurística
        heuristica = self.heuristica_manhattan if usar_manhattan else self.heuristica_euclidiana
        
        # Crear nodo inicial
        nodo_inicial = Nodo(inicio, g=0, h=heuristica(inicio, objetivo))
        
        # Cola de prioridad (open set)
        frontera = []
        heapq.heappush(frontera, nodo_inicial)
        
        # Conjuntos de nodos
        explorados = set()
        en_frontera = {inicio: nodo_inicial}
        
        while frontera:
            # Obtener nodo con menor f
            nodo_actual = heapq.heappop(frontera)
            
            # Remover de en_frontera
            if nodo_actual.posicion in en_frontera:
                del en_frontera[nodo_actual.posicion]
            
            # Verificar si llegamos al objetivo
            if nodo_actual.posicion == objetivo:
                # Reconstruir camino
                self.camino_encontrado = self._reconstruir_camino(nodo_actual)
                self.costo_total = nodo_actual.g
                return self.camino_encontrado, self.costo_total
            
            # Marcar como explorado
            explorados.add(nodo_actual.posicion)
            self.nodos_expandidos += 1
            
            # Expandir vecinos
            vecinos = self.obtener_vecinos(nodo_actual.posicion, dimensiones, obstaculos)
            
            for vecino_pos in vecinos:
                # Saltar si ya fue explorado
                if vecino_pos in explorados:
                    continue
                
                # Costo de moverse al vecino (siempre 1 en un grid)
                g_tentativo = nodo_actual.g + 1
                
                # Verificar si es un nuevo nodo o si encontramos un mejor camino
                if vecino_pos not in en_frontera:
                    # Nuevo nodo
                    h = heuristica(vecino_pos, objetivo)
                    nodo_vecino = Nodo(vecino_pos, g=g_tentativo, h=h, padre=nodo_actual)
                    heapq.heappush(frontera, nodo_vecino)
                    en_frontera[vecino_pos] = nodo_vecino
                else:
                    # Actualizar si encontramos mejor camino
                    nodo_vecino = en_frontera[vecino_pos]
                    if g_tentativo < nodo_vecino.g:
                        nodo_vecino.g = g_tentativo
                        nodo_vecino.f = g_tentativo + nodo_vecino.h
                        nodo_vecino.padre = nodo_actual
                        # Re-insertar en la cola (heapq no tiene decrease-key)
                        heapq.heappush(frontera, nodo_vecino)
        
        # No se encontró camino
        return [], float('inf')
    
    def _reconstruir_camino(self, nodo_final: Nodo) -> List[Tuple[int, int]]:
        """
        Reconstruye el camino desde el nodo final hasta el inicial.
        
        Args:
            nodo_final: Nodo objetivo alcanzado
            
        Returns:
            Lista de posiciones desde inicio hasta objetivo
        """
        camino = []
        nodo_actual = nodo_final
        
        while nodo_actual is not None:
            camino.append(nodo_actual.posicion)
            nodo_actual = nodo_actual.padre
        
        camino.reverse()
        return camino


class BusquedaCostoUniforme:
    """
    Implementación de Búsqueda de Costo Uniforme (Dijkstra).
    Encuentra el nodo más cercano que cumple una condición.
    """
    
    def __init__(self):
        """Inicializa el algoritmo"""
        self.camino_encontrado = []
        self.nodos_expandidos = 0
        self.costo_total = 0
    
    def buscar_mas_cercano(
        self,
        inicio: Tuple[int, int],
        objetivos: List[Tuple[int, int]],
        dimensiones: Tuple[int, int],
        obstaculos: Set[Tuple[int, int]]
    ) -> Tuple[Tuple[int, int], List[Tuple[int, int]], float]:
        """
        Busca el objetivo más cercano desde la posición inicial.
        
        Args:
            inicio: Posición inicial (fila, columna)
            objetivos: Lista de posiciones objetivo posibles
            dimensiones: Dimensiones del mapa (filas, columnas)
            obstaculos: Conjunto de posiciones bloqueadas
            
        Returns:
            Tupla (objetivo_encontrado, camino, costo)
        """
        self.nodos_expandidos = 0
        
        # Conjunto de objetivos para búsqueda rápida
        objetivos_set = set(objetivos)
        
        # Crear nodo inicial
        nodo_inicial = Nodo(inicio, g=0, h=0)
        
        # Cola de prioridad
        frontera = []
        heapq.heappush(frontera, (0, nodo_inicial))
        
        # Conjuntos de nodos
        explorados = set()
        en_frontera = {inicio: 0}
        
        while frontera:
            costo_actual, nodo_actual = heapq.heappop(frontera)
            
            # Si ya fue explorado con menor costo, saltar
            if nodo_actual.posicion in explorados:
                continue
            
            # Verificar si es uno de los objetivos
            if nodo_actual.posicion in objetivos_set:
                self.camino_encontrado = self._reconstruir_camino(nodo_actual)
                self.costo_total = nodo_actual.g
                return nodo_actual.posicion, self.camino_encontrado, self.costo_total
            
            # Marcar como explorado
            explorados.add(nodo_actual.posicion)
            self.nodos_expandidos += 1
            
            # Expandir vecinos
            vecinos = self._obtener_vecinos(nodo_actual.posicion, dimensiones, obstaculos)
            
            for vecino_pos in vecinos:
                if vecino_pos in explorados:
                    continue
                
                g_tentativo = nodo_actual.g + 1
                
                # Agregar o actualizar en frontera
                if vecino_pos not in en_frontera or g_tentativo < en_frontera[vecino_pos]:
                    en_frontera[vecino_pos] = g_tentativo
                    nodo_vecino = Nodo(vecino_pos, g=g_tentativo, h=0, padre=nodo_actual)
                    heapq.heappush(frontera, (g_tentativo, nodo_vecino))
        
        # No se encontró ningún objetivo
        return None, [], float('inf')
    
    def _obtener_vecinos(
        self,
        posicion: Tuple[int, int],
        dimensiones: Tuple[int, int],
        obstaculos: Set[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
        """Obtiene vecinos válidos"""
        fila, columna = posicion
        filas_max, columnas_max = dimensiones
        
        movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        vecinos = []
        
        for df, dc in movimientos:
            nueva_fila = fila + df
            nueva_col = columna + dc
            nueva_pos = (nueva_fila, nueva_col)
            
            if 0 <= nueva_fila < filas_max and 0 <= nueva_col < columnas_max:
                if nueva_pos not in obstaculos:
                    vecinos.append(nueva_pos)
        
        return vecinos
    
    def _reconstruir_camino(self, nodo_final: Nodo) -> List[Tuple[int, int]]:
        """Reconstruye el camino"""
        camino = []
        nodo_actual = nodo_final
        
        while nodo_actual is not None:
            camino.append(nodo_actual.posicion)
            nodo_actual = nodo_actual.padre
        
        camino.reverse()
        return camino


class TempleSimulado:
    """
    Implementación del algoritmo de Temple Simulado para optimización de listas de compras.
    Genera listas que maximizan variedad y se ajustan al presupuesto.
    """
    
    def __init__(
        self,
        temperatura_inicial: float = 1000.0,
        temperatura_minima: float = 1.0,
        factor_enfriamiento: float = 0.95,
        iteraciones_por_temperatura: int = 100
    ):
        """
        Inicializa el algoritmo de Temple Simulado.
        
        Args:
            temperatura_inicial: Temperatura inicial
            temperatura_minima: Temperatura mínima de parada
            factor_enfriamiento: Factor de enfriamiento (0-1)
            iteraciones_por_temperatura: Iteraciones por nivel de temperatura
        """
        self.temperatura_inicial = temperatura_inicial
        self.temperatura_minima = temperatura_minima
        self.factor_enfriamiento = factor_enfriamiento
        self.iteraciones_por_temperatura = iteraciones_por_temperatura
        self.mejor_costo = float('inf')
        self.iteraciones_totales = 0
    
    def generar_solucion_inicial(
        self,
        productos: List[Dict],
        presupuesto_objetivo: float
    ) -> List[Tuple[Dict, int]]:
        """
        Genera una solución inicial aleatoria válida.
        
        Args:
            productos: Lista de productos disponibles
            presupuesto_objetivo: Presupuesto objetivo
            
        Returns:
            Lista de tuplas (producto, cantidad)
        """
        solucion = []
        total = 0.0
        productos_usados = set()
        productos_disponibles = productos.copy()
        random.shuffle(productos_disponibles)
        
        # Agregar productos hasta acercarse al presupuesto
        for producto in productos_disponibles:
            if total >= presupuesto_objetivo * 0.95:
                break
            
            # Determinar cantidad que cabe en el presupuesto
            precio = producto['precio']
            cantidad_maxima = int((presupuesto_objetivo - total) / precio)
            
            if cantidad_maxima > 0:
                # Preferir cantidad 1 para maximizar variedad
                cantidad = 1 if precio <= presupuesto_objetivo - total else 0
                
                if cantidad > 0:
                    solucion.append((producto, cantidad))
                    total += precio * cantidad
                    productos_usados.add(producto['id'])
        
        return solucion
    
    def calcular_costo(
        self,
        solucion: List[Tuple[Dict, int]],
        presupuesto_objetivo: float,
        tipo_lista: str = "exacta"
    ) -> float:
        """
        Calcula el costo de una solución (menor es mejor).
        
        Args:
            solucion: Lista de tuplas (producto, cantidad)
            presupuesto_objetivo: Presupuesto objetivo
            tipo_lista: Tipo de lista ("exacta", "superior", "inferior")
            
        Returns:
            Valor de costo
        """
        if not solucion:
            return float('inf')
        
        # Calcular total
        total = sum(prod['precio'] * cant for prod, cant in solucion)
        
        # Definir rangos según tipo de lista
        if tipo_lista == "exacta":
            objetivo_min = presupuesto_objetivo * 0.998
            objetivo_max = presupuesto_objetivo * 1.002
        elif tipo_lista == "superior":
            objetivo_min = presupuesto_objetivo * 1.00
            objetivo_max = presupuesto_objetivo * 1.05
        elif tipo_lista == "inferior":
            objetivo_min = presupuesto_objetivo * 0.95
            objetivo_max = presupuesto_objetivo * 1.00
        else:
            objetivo_min = presupuesto_objetivo * 0.95
            objetivo_max = presupuesto_objetivo * 1.05
        
        # 1. Penalización por estar fuera del rango (peso muy alto)
        penalizacion_presupuesto = 0.0
        if total < objetivo_min:
            penalizacion_presupuesto = (objetivo_min - total) ** 2 * 100
        elif total > objetivo_max:
            penalizacion_presupuesto = (total - objetivo_max) ** 2 * 100
        
        # 2. Penalización por baja variedad (queremos muchos productos diferentes)
        num_productos_diferentes = len(solucion)
        penalizacion_variedad = 0.0
        if num_productos_diferentes < 5:
            penalizacion_variedad = (5 - num_productos_diferentes) * 50
        
        # 3. Penalización por repetición de productos
        penalizacion_repeticion = 0.0
        for producto, cantidad in solucion:
            if cantidad > 1:
                # Penalizar ligeramente la repetición
                penalizacion_repeticion += (cantidad - 1) * 10
        
        # 4. Bonificación por diversidad de categorías
        categorias = set(prod['categoria'] for prod, _ in solucion)
        bonus_categorias = len(categorias) * (-5)  # Negativo porque queremos minimizar
        
        # Costo total
        costo = (
            penalizacion_presupuesto +
            penalizacion_variedad +
            penalizacion_repeticion +
            bonus_categorias
        )
        
        return costo
    
    def generar_vecino(
        self,
        solucion: List[Tuple[Dict, int]],
        productos: List[Dict]
    ) -> List[Tuple[Dict, int]]:
        """
        Genera una solución vecina mediante una modificación aleatoria.
        
        Args:
            solucion: Solución actual
            productos: Lista de todos los productos disponibles
            
        Returns:
            Nueva solución vecina
        """
        if not solucion:
            return self.generar_solucion_inicial(productos, 100.0)
        
        vecino = [tupla for tupla in solucion]  # Copiar
        
        # Elegir operación aleatoria
        operacion = random.choice(['agregar', 'quitar', 'aumentar', 'disminuir', 'reemplazar'])
        
        if operacion == 'agregar' and len(productos) > len(vecino):
            # Agregar un producto nuevo
            ids_usados = {prod['id'] for prod, _ in vecino}
            productos_disponibles = [p for p in productos if p['id'] not in ids_usados]
            if productos_disponibles:
                nuevo_producto = random.choice(productos_disponibles)
                vecino.append((nuevo_producto, 1))
        
        elif operacion == 'quitar' and len(vecino) > 1:
            # Quitar un producto aleatorio
            idx = random.randint(0, len(vecino) - 1)
            vecino.pop(idx)
        
        elif operacion == 'aumentar' and vecino:
            # Aumentar cantidad de un producto
            idx = random.randint(0, len(vecino) - 1)
            producto, cantidad = vecino[idx]
            vecino[idx] = (producto, cantidad + 1)
        
        elif operacion == 'disminuir' and vecino:
            # Disminuir cantidad de un producto
            idx = random.randint(0, len(vecino) - 1)
            producto, cantidad = vecino[idx]
            if cantidad > 1:
                vecino[idx] = (producto, cantidad - 1)
            else:
                vecino.pop(idx)
        
        elif operacion == 'reemplazar' and vecino:
            # Reemplazar un producto por otro
            idx = random.randint(0, len(vecino) - 1)
            ids_usados = {prod['id'] for prod, _ in vecino}
            productos_disponibles = [p for p in productos if p['id'] not in ids_usados]
            if productos_disponibles:
                nuevo_producto = random.choice(productos_disponibles)
                _, cantidad = vecino[idx]
                vecino[idx] = (nuevo_producto, cantidad)
        
        return vecino
    
    def optimizar(
        self,
        productos: List[Dict],
        presupuesto_objetivo: float,
        tipo_lista: str = "exacta"
    ) -> Tuple[List[Tuple[Dict, int]], float, int]:
        """
        Ejecuta el algoritmo de Temple Simulado.
        
        Args:
            productos: Lista de productos disponibles
            presupuesto_objetivo: Presupuesto objetivo
            tipo_lista: Tipo de lista a generar
            
        Returns:
            Tupla (mejor_solucion, mejor_costo, iteraciones)
        """
        # Generar solución inicial
        solucion_actual = self.generar_solucion_inicial(productos, presupuesto_objetivo)
        costo_actual = self.calcular_costo(solucion_actual, presupuesto_objetivo, tipo_lista)
        
        mejor_solucion = [tupla for tupla in solucion_actual]
        mejor_costo = costo_actual
        
        temperatura = self.temperatura_inicial
        self.iteraciones_totales = 0
        iteraciones_sin_mejora = 0
        max_iteraciones_sin_mejora = 50
        
        while temperatura > self.temperatura_minima:
            for _ in range(self.iteraciones_por_temperatura):
                # Generar vecino
                vecino = self.generar_vecino(solucion_actual, productos)
                costo_vecino = self.calcular_costo(vecino, presupuesto_objetivo, tipo_lista)
                
                # Calcular delta
                delta = costo_vecino - costo_actual
                
                # Decidir si aceptar el vecino
                if delta < 0:
                    # Mejor solución, siempre aceptar
                    solucion_actual = vecino
                    costo_actual = costo_vecino
                    iteraciones_sin_mejora = 0
                    
                    # Actualizar mejor solución global
                    if costo_actual < mejor_costo:
                        mejor_solucion = [tupla for tupla in solucion_actual]
                        mejor_costo = costo_actual
                else:
                    # Peor solución, aceptar con probabilidad
                    probabilidad = math.exp(-delta / temperatura)
                    if random.random() < probabilidad:
                        solucion_actual = vecino
                        costo_actual = costo_vecino
                
                self.iteraciones_totales += 1
                iteraciones_sin_mejora += 1
                
                # Criterio de parada adicional
                if iteraciones_sin_mejora >= max_iteraciones_sin_mejora:
                    break
            
            # Enfriar
            temperatura *= self.factor_enfriamiento
            
            # Parada anticipada si no hay mejoras
            if iteraciones_sin_mejora >= max_iteraciones_sin_mejora:
                break
        
        self.mejor_costo = mejor_costo
        return mejor_solucion, mejor_costo, self.iteraciones_totales
