#!/usr/bin/env python3
"""
Script de prueba para la integración Bilderklo-AppSheet-WhatsApp
"""
import requests
import json
import time
from datetime import datetime

def test_webhook_new_user():
    """Probar webhook de nuevo usuario"""
    print("🧪 Probando webhook de nuevo usuario...")
    
    test_data = {
        "user_id": f"test_user_{int(time.time())}",
        "name": "Usuario de Prueba",
        "email": "test@example.com",
        "phone": "+1234567890",  # Cambia por un número real para pruebas
        "source": "bilderklo",
        "registration_date": datetime.now().isoformat()
    }
    
    try:
        response = requests.post(
            "http://localhost:5000/webhook/new-user",
            json=test_data,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Webhook funcionando correctamente")
            print(f"Respuesta: {response.json()}")
        else:
            print(f"❌ Error en webhook: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor. ¿Está ejecutándose?")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

def test_health_endpoint():
    """Probar endpoint de salud"""
    print("🏥 Probando endpoint de salud...")
    
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        
        if response.status_code == 200:
            print("✅ Servidor saludable")
            print(f"Respuesta: {response.json()}")
        else:
            print(f"❌ Problema con el servidor: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Servidor no disponible")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_user_activity_webhook():
    """Probar webhook de actividad de usuario"""
    print("📊 Probando webhook de actividad...")
    
    test_data = {
        "user_id": "test_user_123",
        "activity_type": "viewed_product",
        "product_id": "product_456",
        "timestamp": datetime.now().isoformat()
    }
    
    try:
        response = requests.post(
            "http://localhost:5000/webhook/user-activity",
            json=test_data,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Webhook de actividad funcionando")
            print(f"Respuesta: {response.json()}")
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def simulate_user_journey():
    """Simular el journey completo de un usuario"""
    print("🎭 Simulando journey completo de usuario...")
    
    # 1. Nuevo usuario se registra
    print("1️⃣ Usuario se registra...")
    test_webhook_new_user()
    
    time.sleep(2)
    
    # 2. Usuario ve un producto
    print("2️⃣ Usuario ve un producto...")
    test_user_activity_webhook()
    
    time.sleep(1)
    
    # 3. Usuario abandona carrito (simulado)
    print("3️⃣ Usuario abandona carrito...")
    activity_data = {
        "user_id": "test_user_123",
        "activity_type": "abandoned_cart",
        "cart_value": 99.99,
        "timestamp": datetime.now().isoformat()
    }
    
    try:
        requests.post(
            "http://localhost:5000/webhook/user-activity",
            json=activity_data,
            timeout=10
        )
        print("✅ Simulación de carrito abandonado enviada")
    except Exception as e:
        print(f"❌ Error en simulación: {e}")

def main():
    """Función principal de pruebas"""
    print("🚀 Iniciando pruebas del sistema de integración")
    print("=" * 50)
    
    # Probar que el servidor esté corriendo
    test_health_endpoint()
    print()
    
    # Probar webhooks individuales
    test_webhook_new_user()
    print()
    
    test_user_activity_webhook()
    print()
    
    # Simular journey completo
    print("🎯 ¿Quieres simular un journey completo? (y/n): ", end="")
    if input().lower() == 'y':
        simulate_user_journey()
    
    print("\n" + "=" * 50)
    print("✅ Pruebas completadas")
    print("\n📝 Notas importantes:")
    print("- Asegúrate de que el servidor esté ejecutándose (python bot_ventas_integration.py)")
    print("- Configura un número de teléfono real en el test para probar WhatsApp")
    print("- Revisa los logs para ver el procesamiento detallado")

if __name__ == "__main__":
    main()
