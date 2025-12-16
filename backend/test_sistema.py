"""
Script de prueba para verificar el funcionamiento del sistema multi-agente.
Ejecuta un proceso completo de compra.
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"


def imprimir_seccion(titulo):
    """Imprime un título de sección"""
    print("\n" + "="*70)
    print(f"  {titulo}")
    print("="*70 + "\n")


def probar_sistema_completo():
    """Prueba el sistema con un proceso completo de compra"""
    
    imprimir_seccion("PRUEBA DEL SISTEMA MULTI-AGENTE DE SUPERMERCADO")
    
    comprador_id = "COMP_TEST_001"
    sucursal_id = "SUC001"
    presupuesto = 150.0
    
    try:
        # Verificar que el servidor está activo
        print("🔍 Verificando servidor...")
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Servidor activo")
        else:
            print("❌ Servidor no responde correctamente")
            return
        
        # ===== PROCESO COMPLETO =====
        imprimir_seccion("EJECUTANDO PROCESO COMPLETO")
        
        print(f"Comprador ID: {comprador_id}")
        print(f"Sucursal: {sucursal_id}")
        print(f"Presupuesto: {presupuesto} Bs.\n")
        
        response = requests.post(f"{BASE_URL}/api/comprador/proceso-completo", json={
            "comprador_id": comprador_id,
            "sucursal_id": sucursal_id,
            "presupuesto": presupuesto,
            "tipo_lista": "exacta"
        })
        
        if response.status_code != 200:
            print(f"❌ Error: {response.json()}")
            return
        
        resultado = response.json()
        proceso = resultado['proceso']
        
        # Mostrar resultados
        imprimir_seccion("RESULTADOS DEL PROCESO")
        
        print("1. INGRESO A SUCURSAL")
        print(f"   ✅ Ingresó en posición: {proceso['ingreso']['posicion']}")
        print(f"   ✅ Productos disponibles: {proceso['ingreso']['productos_disponibles']}")
        
        print("\n2. LISTAS GENERADAS")
        listas = proceso['listas_generadas']
        print(f"   • Lista exacta: {listas['lista_exacta']['total']} Bs. ({listas['lista_exacta']['cantidad_items']} productos)")
        print(f"   • Lista superior: {listas['lista_superior']['total']} Bs. ({listas['lista_superior']['cantidad_items']} productos)")
        print(f"   • Lista inferior: {listas['lista_inferior']['total']} Bs. ({listas['lista_inferior']['cantidad_items']} productos)")
        
        print(f"\n3. LISTA SELECCIONADA: {proceso['lista_seleccionada']}")
        
        print("\n4. RECOLECCIÓN DE PRODUCTOS")
        print(f"   ✅ Productos recolectados: {proceso['recoleccion']['productos']}")
        print(f"   ✅ Distancia recorrida: {proceso['recoleccion']['distancia']} pasos")
        
        print(f"\n5. CAJERO")
        print(f"   ✅ Cajero seleccionado: {proceso['cajero']}")
        
        print("\n6. FACTURA GENERADA")
        factura = proceso['factura']
        print(f"   Cajero: {factura['cajero_id']}")
        print(f"   Total items: {factura['cantidad_items']}")
        print(f"   Total: {factura['total']} Bs.")
        print("\n   Detalle:")
        for item in factura['items']:
            print(f"   • {item['nombre']} x{item['cantidad']} = {item['subtotal']} Bs.")
        
        print("\n7. ESTADO FINAL")
        print(f"   ✅ Estado: {proceso['estado_final']['estado']}")
        print(f"   ✅ Distancia total: {proceso['estado_final']['distancia_total_recorrida']} pasos")
        
        imprimir_seccion("✅ PRUEBA COMPLETADA EXITOSAMENTE")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor")
        print("   Asegúrate de que el servidor esté ejecutándose (python app.py)")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")


def probar_paso_a_paso():
    """Prueba el sistema paso a paso"""
    
    imprimir_seccion("PRUEBA PASO A PASO DEL SISTEMA")
    
    comprador_id = "COMP_TEST_002"
    sucursal_id = "SUC002"
    presupuesto = 180.0
    
    try:
        # 1. Crear comprador
        print("1️⃣ Creando comprador...")
        response = requests.post(f"{BASE_URL}/api/comprador/crear", json={
            "comprador_id": comprador_id,
            "sucursal_id": sucursal_id,
            "presupuesto": presupuesto
        })
        print(f"   ✅ Comprador creado: {response.json()['comprador']['comprador_id']}")
        time.sleep(1)
        
        # 2. Generar listas
        print("\n2️⃣ Generando listas de compras...")
        response = requests.post(f"{BASE_URL}/api/comprador/generar-listas", json={
            "comprador_id": comprador_id
        })
        listas = response.json()['listas']
        print(f"   ✅ Lista exacta: {listas['lista_exacta']['total']} Bs.")
        print(f"   ✅ Lista superior: {listas['lista_superior']['total']} Bs.")
        print(f"   ✅ Lista inferior: {listas['lista_inferior']['total']} Bs.")
        time.sleep(1)
        
        # 3. Seleccionar lista
        print("\n3️⃣ Seleccionando lista superior...")
        response = requests.post(f"{BASE_URL}/api/comprador/seleccionar-lista", json={
            "comprador_id": comprador_id,
            "tipo_lista": "superior"
        })
        print(f"   ✅ Lista seleccionada")
        time.sleep(1)
        
        # 4. Recolectar productos
        print("\n4️⃣ Recolectando productos...")
        response = requests.post(f"{BASE_URL}/api/comprador/iniciar-recoleccion", json={
            "comprador_id": comprador_id
        })
        resultado = response.json()
        print(f"   ✅ Productos recolectados: {len(resultado['resultado']['productos_recolectados'])}")
        print(f"   ✅ Distancia: {resultado['resultado']['distancia_recorrida']} pasos")
        time.sleep(1)
        
        # 5. Ir a cajero
        print("\n5️⃣ Buscando cajero más cercano...")
        response = requests.post(f"{BASE_URL}/api/comprador/ir-a-cajero", json={
            "comprador_id": comprador_id
        })
        cajero_info = response.json()
        cajero_id = cajero_info['cajero']['cajero']['id']
        print(f"   ✅ Cajero encontrado: {cajero_id}")
        print(f"   ✅ Distancia al cajero: {cajero_info['cajero']['distancia_a_cajero']} pasos")
        time.sleep(1)
        
        # 6. Comunicar con cajero
        print("\n6️⃣ Comunicándose con el cajero...")
        response = requests.post(f"{BASE_URL}/api/comprador/comunicar-cajero", json={
            "comprador_id": comprador_id,
            "cajero_id": cajero_id
        })
        factura_resp = response.json()
        if factura_resp['success']:
            factura = factura_resp['factura']
            print(f"   ✅ Factura recibida")
            print(f"   💰 Total: {factura['total']} Bs.")
        else:
            print(f"   ❌ Error al procesar factura")
        
        imprimir_seccion("✅ PRUEBA PASO A PASO COMPLETADA")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def verificar_estado_sistema():
    """Verifica el estado general del sistema"""
    
    imprimir_seccion("ESTADO DEL SISTEMA")
    
    try:
        response = requests.get(f"{BASE_URL}/api/estado")
        estado = response.json()
        
        print(f"Compradores activos: {estado['compradores_activos']}")
        print(f"Cajeros activos: {estado['cajeros_activos']}")
        print("\nCanales de comunicación:")
        for sucursal, stats in estado['canales']['canales'].items():
            print(f"  • {sucursal}:")
            print(f"    - Cajeros registrados: {stats['cajeros_registrados']}")
            print(f"    - Cajeros disponibles: {stats['cajeros_disponibles']}")
            print(f"    - Mensajes totales: {stats['mensajes_totales']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def menu_principal():
    """Menú principal de pruebas"""
    
    while True:
        print("\n" + "="*70)
        print("  SISTEMA DE PRUEBAS - MULTI-AGENTE DE SUPERMERCADO")
        print("="*70)
        print("\n1. Prueba completa (proceso completo en una llamada)")
        print("2. Prueba paso a paso (proceso detallado)")
        print("3. Verificar estado del sistema")
        print("4. Salir")
        
        opcion = input("\nSelecciona una opción (1-4): ").strip()
        
        if opcion == "1":
            probar_sistema_completo()
        elif opcion == "2":
            probar_paso_a_paso()
        elif opcion == "3":
            verificar_estado_sistema()
        elif opcion == "4":
            print("\n👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida")
        
        input("\nPresiona Enter para continuar...")


if __name__ == "__main__":
    print("\n🚀 INICIANDO PRUEBAS DEL SISTEMA MULTI-AGENTE")
    print("📡 Asegúrate de que el servidor esté ejecutándose en http://localhost:5000")
    input("\nPresiona Enter para continuar...")
    
    menu_principal()
