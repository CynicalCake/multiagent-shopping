"""
Servidor Flask para Sistema Multi-Agente de Supermercado
Gestiona la comunicación entre frontend y los agentes comprador y cajero.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Agregar directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.agente_comprador import AgenteComprador
from models.agente_cajero import AgenteCajero
from utils.canal_comunicacion import gestor_canales_global

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supermercado_multiagente_2025'
CORS(app)

# Diccionarios para mantener agentes activos
agentes_compradores = {}  # {comprador_id: instancia}
agentes_cajeros = {}  # {cajero_id: instancia}

# Diccionario para almacenar facturas recibidas
facturas_recibidas = {}  # {comprador_id: factura}


def inicializar_cajeros():
    """
    Inicializa los cajeros automáticamente leyendo los mapas JSON.
    """
    import os
    import json
    
    print("\n" + "="*70)
    print("INICIALIZANDO SISTEMA MULTI-AGENTE DE SUPERMERCADO")
    print("="*70)
    
    cajeros_config = []
    mapas_dir = os.path.join(os.path.dirname(__file__), 'data', 'mapas')
    
    # Buscar todos los archivos de mapas y cargar cajeros
    if os.path.exists(mapas_dir):
        for filename in sorted(os.listdir(mapas_dir)):
            if filename.endswith('.json'):
                try:
                    filepath = os.path.join(mapas_dir, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        mapa_data = json.load(f)
                    
                    sucursal_id = mapa_data.get('sucursal_id')
                    cajeros = mapa_data.get('cajeros', [])
                    
                    # Agregar cada cajero del mapa a la configuración
                    for cajero in cajeros:
                        cajeros_config.append({
                            "cajero_id": cajero['id'],
                            "sucursal_id": sucursal_id,
                            "posicion": {
                                "fila": cajero['fila'],
                                "columna": cajero['columna']
                            }
                        })
                    
                    print(f"✓ Cargados {len(cajeros)} cajeros de {sucursal_id} ({mapa_data.get('nombre', '')})")
                except Exception as e:
                    print(f"✗ Error al cargar cajeros del mapa {filename}: {e}")
    
    print(f"\n📊 Total cajeros a inicializar: {len(cajeros_config)}\n")
    
    for config in cajeros_config:
        try:
            # Crear agente cajero
            cajero = AgenteCajero(
                cajero_id=config["cajero_id"],
                sucursal_id=config["sucursal_id"],
                posicion=config["posicion"]
            )
            
            # Registrar en el canal de comunicación
            gestor_canales_global.registrar_cajero_en_sucursal(
                config["sucursal_id"],
                cajero
            )
            
            # Guardar referencia
            key = f"{config['sucursal_id']}_{config['cajero_id']}"
            agentes_cajeros[key] = cajero
            
            print(f"✓ Cajero {config['cajero_id']} activo en {config['sucursal_id']}")
            
        except Exception as e:
            print(f"✗ Error al inicializar cajero {config['cajero_id']}: {e}")
    
    print("="*70)
    print(f"Total de cajeros activos: {len(agentes_cajeros)}")
    print("="*70 + "\n")


# ========== RUTAS DE INFORMACIÓN GENERAL ==========

@app.route('/')
def index():
    """Ruta principal con información del sistema"""
    return jsonify({
        "sistema": "Multi-Agente de Supermercado",
        "version": "2.0",
        "agentes": {
            "compradores_activos": len(agentes_compradores),
            "cajeros_activos": len(agentes_cajeros)
        },
        "endpoints": {
            "comprador": "/api/comprador/*",
            "cajero": "/api/cajero/*",
            "sucursal": "/api/sucursal/*"
        }
    })


@app.route('/api/estado', methods=['GET'])
def obtener_estado_general():
    """Obtiene el estado general del sistema"""
    return jsonify({
        "compradores_activos": len(agentes_compradores),
        "cajeros_activos": len(agentes_cajeros),
        "canales": gestor_canales_global.obtener_estadisticas_global()
    })


# ========== RUTAS DEL AGENTE COMPRADOR ==========

@app.route('/api/comprador/crear', methods=['POST'])
def crear_comprador():
    """
    Crea un nuevo agente comprador y lo hace ingresar a la sucursal.
    
    Body: {
        "comprador_id": str,
        "sucursal_id": str,
        "presupuesto": float
    }
    """
    try:
        data = request.get_json()
        comprador_id = data.get('comprador_id')
        sucursal_id = data.get('sucursal_id')
        presupuesto = data.get('presupuesto')
        
        if not all([comprador_id, sucursal_id, presupuesto]):
            return jsonify({"error": "Faltan parámetros requeridos"}), 400
        
        # Crear agente comprador
        comprador = AgenteComprador(comprador_id)
        
        # Obtener canal de comunicación
        canal = gestor_canales_global.obtener_canal(sucursal_id)
        
        # Registrar callback para recibir facturas
        def callback_factura(factura):
            facturas_recibidas[comprador_id] = factura
            print(f"[API] Factura recibida para {comprador_id}")
        
        gestor_canales_global.registrar_comprador_en_sucursal(
            sucursal_id,
            comprador_id,
            callback_factura
        )
        
        # Ingresar a sucursal
        resultado = comprador.ingresar_a_sucursal(sucursal_id, presupuesto, canal)
        
        # Guardar referencia
        agentes_compradores[comprador_id] = comprador
        
        return jsonify({
            "success": True,
            "comprador": resultado
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/comprador/generar-listas', methods=['POST'])
def generar_listas():
    """
    Genera las tres listas de compras para el comprador.
    
    Body: {
        "comprador_id": str
    }
    """
    try:
        data = request.get_json()
        comprador_id = data.get('comprador_id')
        
        if comprador_id not in agentes_compradores:
            return jsonify({"error": "Comprador no encontrado"}), 404
        
        comprador = agentes_compradores[comprador_id]
        resultado = comprador.generar_listas_compras()
        
        return jsonify({
            "success": True,
            "listas": resultado
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/comprador/seleccionar-lista', methods=['POST'])
def seleccionar_lista():
    """
    Usuario selecciona una de las tres listas.
    
    Body: {
        "comprador_id": str,
        "tipo_lista": str  # "exacta", "superior", "inferior"
    }
    """
    try:
        data = request.get_json()
        comprador_id = data.get('comprador_id')
        tipo_lista = data.get('tipo_lista')
        
        if comprador_id not in agentes_compradores:
            return jsonify({"error": "Comprador no encontrado"}), 404
        
        comprador = agentes_compradores[comprador_id]
        resultado = comprador.seleccionar_lista(tipo_lista)
        
        return jsonify({
            "success": True,
            "seleccion": resultado
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/comprador/iniciar-recoleccion', methods=['POST'])
def iniciar_recoleccion():
    """
    Inicia y ejecuta la recolección de productos.
    
    Body: {
        "comprador_id": str
    }
    """
    try:
        data = request.get_json()
        comprador_id = data.get('comprador_id')
        
        if comprador_id not in agentes_compradores:
            return jsonify({"error": "Comprador no encontrado"}), 404
        
        comprador = agentes_compradores[comprador_id]
        
        # Planificar recolección
        plan = comprador.iniciar_recoleccion()
        
        # Ejecutar recolección
        resultado = comprador.ejecutar_recoleccion(plan['plan_recoleccion'])
        
        return jsonify({
            "success": True,
            "plan": plan,
            "resultado": resultado
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/comprador/ir-a-cajero', methods=['POST'])
def ir_a_cajero():
    """
    Busca el cajero más cercano y se mueve hacia él.
    
    Body: {
        "comprador_id": str
    }
    """
    try:
        data = request.get_json()
        comprador_id = data.get('comprador_id')
        
        if comprador_id not in agentes_compradores:
            return jsonify({"error": "Comprador no encontrado"}), 404
        
        comprador = agentes_compradores[comprador_id]
        
        # Buscar cajero más cercano
        info_cajero = comprador.buscar_cajero_mas_cercano()
        
        # Moverse al cajero
        resultado = comprador.moverse_a_cajero(info_cajero['ruta_a_cajero'])
        
        return jsonify({
            "success": True,
            "cajero": info_cajero,
            "movimiento": resultado
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/comprador/comunicar-cajero', methods=['POST'])
def comunicar_cajero():
    """
    Comprador se comunica con el cajero para procesar productos.
    
    Body: {
        "comprador_id": str,
        "cajero_id": str
    }
    """
    try:
        data = request.get_json()
        comprador_id = data.get('comprador_id')
        cajero_id = data.get('cajero_id')
        
        if comprador_id not in agentes_compradores:
            return jsonify({"error": "Comprador no encontrado"}), 404
        
        comprador = agentes_compradores[comprador_id]
        
        # Enviar mensaje al cajero
        mensaje = comprador.comunicar_con_cajero(cajero_id)
        
        # Esperar factura (en una implementación real sería asíncrono)
        import time
        time.sleep(0.5)  # Dar tiempo al cajero para procesar
        
        # Obtener factura
        factura = facturas_recibidas.get(comprador_id)
        
        if factura:
            resultado = comprador.recibir_factura(factura)
            return jsonify({
                "success": True,
                "mensaje": mensaje,
                "factura": factura,
                "estado_final": resultado
            })
        else:
            return jsonify({
                "success": False,
                "error": "No se recibió factura del cajero"
            }), 500
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/comprador/estado/<comprador_id>', methods=['GET'])
def obtener_estado_comprador(comprador_id):
    """Obtiene el estado actual del comprador"""
    try:
        if comprador_id not in agentes_compradores:
            return jsonify({"error": "Comprador no encontrado"}), 404
        
        comprador = agentes_compradores[comprador_id]
        estado = comprador.obtener_estado()
        
        return jsonify({
            "success": True,
            "estado": estado
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/comprador/proceso-completo', methods=['POST'])
def proceso_completo():
    """
    Ejecuta el proceso completo de compra de principio a fin.
    
    Body: {
        "comprador_id": str,
        "sucursal_id": str,
        "presupuesto": float,
        "tipo_lista": str  # "exacta", "superior", "inferior"
    }
    """
    try:
        data = request.get_json()
        comprador_id = data.get('comprador_id')
        sucursal_id = data.get('sucursal_id')
        presupuesto = data.get('presupuesto')
        tipo_lista = data.get('tipo_lista', 'exacta')
        
        # 1. Crear comprador e ingresar a sucursal
        comprador = AgenteComprador(comprador_id)
        canal = gestor_canales_global.obtener_canal(sucursal_id)
        
        def callback_factura(factura):
            facturas_recibidas[comprador_id] = factura
        
        gestor_canales_global.registrar_comprador_en_sucursal(
            sucursal_id, comprador_id, callback_factura
        )
        
        resultado_ingreso = comprador.ingresar_a_sucursal(sucursal_id, presupuesto, canal)
        agentes_compradores[comprador_id] = comprador
        
        # 2. Generar listas
        listas = comprador.generar_listas_compras()
        
        # 3. Seleccionar lista
        seleccion = comprador.seleccionar_lista(tipo_lista)
        
        # 4. Recolectar productos
        plan = comprador.iniciar_recoleccion()
        recoleccion = comprador.ejecutar_recoleccion(plan['plan_recoleccion'])
        
        # 5. Ir a cajero
        info_cajero = comprador.buscar_cajero_mas_cercano()
        movimiento_cajero = comprador.moverse_a_cajero(info_cajero['ruta_a_cajero'])
        
        # 6. Comunicar con cajero
        mensaje = comprador.comunicar_con_cajero(info_cajero['cajero']['id'])
        
        import time
        time.sleep(0.5)
        
        factura = facturas_recibidas.get(comprador_id)
        estado_final = comprador.recibir_factura(factura) if factura else None
        
        return jsonify({
            "success": True,
            "proceso": {
                "ingreso": resultado_ingreso,
                "listas_generadas": listas,
                "lista_seleccionada": tipo_lista,
                "recoleccion": {
                    "productos": len(recoleccion['productos_recolectados']),
                    "distancia": recoleccion['distancia_recorrida']
                },
                "cajero": info_cajero['cajero']['id'],
                "factura": factura,
                "estado_final": estado_final
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ========== RUTAS DEL CAJERO ==========

@app.route('/api/cajero/estado/<sucursal_id>/<cajero_id>', methods=['GET'])
def obtener_estado_cajero(sucursal_id, cajero_id):
    """Obtiene el estado de un cajero específico"""
    try:
        key = f"{sucursal_id}_{cajero_id}"
        
        if key not in agentes_cajeros:
            return jsonify({"error": "Cajero no encontrado"}), 404
        
        cajero = agentes_cajeros[key]
        estado = cajero.obtener_estado()
        
        return jsonify({
            "success": True,
            "estado": estado
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ========== RUTAS DE SUCURSAL ==========

@app.route('/api/sucursal/<sucursal_id>/estado', methods=['GET'])
def obtener_estado_sucursal(sucursal_id):
    """Obtiene el estado completo de una sucursal"""
    try:
        # Obtener cajeros de la sucursal
        cajeros = []
        for key, cajero in agentes_cajeros.items():
            if cajero.sucursal_id == sucursal_id:
                cajeros.append(cajero.obtener_estado())
        
        # Obtener compradores en la sucursal
        compradores = []
        for comp_id, comprador in agentes_compradores.items():
            if comprador.sucursal_id == sucursal_id:
                compradores.append(comprador.obtener_estado())
        
        # Estadísticas del canal
        canal = gestor_canales_global.obtener_canal(sucursal_id)
        stats_canal = canal.obtener_estadisticas()
        
        return jsonify({
            "success": True,
            "sucursal_id": sucursal_id,
            "cajeros": cajeros,
            "compradores": compradores,
            "canal": stats_canal
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ========== ENDPOINTS DE MAPAS ==========

@app.route('/api/mapas/<sucursal_id>', methods=['GET'])
def obtener_mapa(sucursal_id):
    """
    Obtiene el mapa de una sucursal.
    """
    try:
        import json
        ruta_mapa = os.path.join('data', 'mapas', f'{sucursal_id}.json')
        
        if not os.path.exists(ruta_mapa):
            return jsonify({
                "success": False,
                "error": f"Mapa {sucursal_id} no encontrado"
            }), 404
        
        with open(ruta_mapa, 'r', encoding='utf-8') as f:
            mapa = json.load(f)
        
        return jsonify({
            "success": True,
            "mapa": mapa
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/mapas', methods=['GET'])
def listar_mapas():
    """
    Lista todos los mapas disponibles.
    """
    try:
        import json
        mapas_dir = os.path.join('data', 'mapas')
        archivos = [f for f in os.listdir(mapas_dir) if f.endswith('.json')]
        
        mapas = []
        for archivo in archivos:
            with open(os.path.join(mapas_dir, archivo), 'r', encoding='utf-8') as f:
                mapa = json.load(f)
                mapas.append({
                    "sucursal_id": mapa.get("sucursal_id"),
                    "nombre": mapa.get("nombre"),
                    "dimensiones": mapa.get("dimensiones")
                })
        
        return jsonify({
            "success": True,
            "mapas": mapas
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/inventarios/<sucursal_id>', methods=['GET'])
def obtener_inventario(sucursal_id):
    """
    Obtiene el inventario de una sucursal.
    """
    try:
        import json
        ruta_inventario = os.path.join('data', 'inventario', f'{sucursal_id}.json')
        
        if not os.path.exists(ruta_inventario):
            return jsonify({
                "success": False,
                "error": f"Inventario {sucursal_id} no encontrado"
            }), 404
        
        with open(ruta_inventario, 'r', encoding='utf-8') as f:
            inventario = json.load(f)
        
        return jsonify({
            "success": True,
            "inventario": inventario
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/mapas/<sucursal_id>', methods=['POST'])
def guardar_mapa(sucursal_id):
    """
    Guarda o actualiza un mapa de sucursal.
    """
    try:
        import json
        datos = request.get_json()
        
        # Validar datos mínimos
        if not datos.get('nombre') or not datos.get('dimensiones'):
            return jsonify({
                "success": False,
                "error": "Faltan datos requeridos: nombre y dimensiones"
            }), 400
        
        # Asegurar que tiene sucursal_id
        datos['sucursal_id'] = sucursal_id
        
        # Guardar archivo
        ruta_mapa = os.path.join('data', 'mapas', f'{sucursal_id}.json')
        with open(ruta_mapa, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        
        return jsonify({
            "success": True,
            "mensaje": f"Mapa {sucursal_id} guardado exitosamente"
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ========== INICIALIZACIÓN Y EJECUCIÓN ==========

if __name__ == '__main__':
    # Inicializar cajeros al arrancar el servidor
    inicializar_cajeros()
    
    # Ejecutar servidor
    print("\n🚀 Servidor Flask iniciado")
    print("📡 Escuchando en http://localhost:5000")
    print("📚 Documentación en http://localhost:5000\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
