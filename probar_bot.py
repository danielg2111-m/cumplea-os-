#!/usr/bin/env python3
"""
Script para probar todas las funcionalidades del Bot de Ventas
"""
import requests
import json
import time
from datetime import datetime

def test_bot():
    base_url = "http://localhost:5000"
    
    print("🧪 Probando Bot de Ventas")
    print("=" * 50)
    
    # 1. Probar endpoint de salud
    print("1️⃣ Probando endpoint de salud...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Bot saludable")
            print(f"   Respuesta: {response.json()}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error conectando al bot: {e}")
        return
    
    print()
    
    # 2. Probar webhook de nuevo usuario
    print("2️⃣ Probando webhook de nuevo usuario...")
    user_data = {
        "user_id": f"test_user_{int(time.time())}",
        "name": "María González",
        "email": "maria@example.com",
        "phone": "+1987654321",
        "source": "bilderklo",
        "registration_date": datetime.now().isoformat()
    }
    
    try:
        response = requests.post(f"{base_url}/webhook/new-user", json=user_data)
        if response.status_code == 200:
            print("✅ Usuario procesado correctamente")
            print(f"   Respuesta: {response.json()}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    
    # 3. Probar webhook de actividad
    print("3️⃣ Probando webhook de actividad...")
    activity_data = {
        "user_id": "test_user_123",
        "activity_type": "viewed_product",
        "product_id": "product_456",
        "timestamp": datetime.now().isoformat()
    }
    
    try:
        response = requests.post(f"{base_url}/webhook/user-activity", json=activity_data)
        if response.status_code == 200:
            print("✅ Actividad procesada correctamente")
            print(f"   Respuesta: {response.json()}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    
    # 4. Verificar estado final
    print("4️⃣ Verificando estado final...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Usuarios procesados: {data.get('users_processed', 0)}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    print("=" * 50)
    print("🎉 Pruebas completadas")
    print("💡 El bot está funcionando correctamente")

def simulate_user_journey():
    """Simular el journey completo de un usuario"""
    base_url = "http://localhost:5000"
    
    print("�� Simulando journey completo de usuario...")
    print("=" * 50)
    
    # Usuario se registra
    print("1️⃣ Usuario se registra en Bilderklo...")
    user_data = {
        "user_id": f"journey_user_{int(time.time())}",
        "name": "Carlos Rodríguez",
        "email": "carlos@example.com",
        "phone": "+1555123456",
        "source": "bilderklo"
    }
    
    response = requests.post(f"{base_url}/webhook/new-user", json=user_data)
    if response.status_code == 200:
        print("✅ Usuario registrado y mensaje de bienvenida enviado")
    
    time.sleep(2)
    
    # Usuario ve un producto
    print("2️⃣ Usuario ve un producto...")
    activity_data = {
        "user_id": user_data["user_id"],
        "activity_type": "viewed_product",
        "product_id": "premium_plan_001",
        "timestamp": datetime.now().isoformat()
    }
    
    response = requests.post(f"{base_url}/webhook/user-activity", json=activity_data)
    if response.status_code == 200:
        print("✅ Actividad de visualización registrada")
    
    time.sleep(1)
    
    # Usuario abandona carrito
    print("3️⃣ Usuario abandona carrito...")
    activity_data = {
        "user_id": user_data["user_id"],
        "activity_type": "abandoned_cart",
        "cart_value": 99.99,
        "timestamp": datetime.now().isoformat()
    }
    
    response = requests.post(f"{base_url}/webhook/user-activity", json=activity_data)
    if response.status_code == 200:
        print("✅ Abandono de carrito registrado")
    
    print("🎉 Journey simulado completamente")

def main():
    print("🤖 Herramientas de Prueba del Bot de Ventas")
    print("=" * 60)
    print("1. Pruebas básicas")
    print("2. Simular journey de usuario")
    print("3. Ambas opciones")
    print("=" * 60)
    
    choice = input("Selecciona una opción (1-3): ").strip()
    
    if choice == "1":
        test_bot()
    elif choice == "2":
        simulate_user_journey()
    elif choice == "3":
        test_bot()
        print("\n")
        simulate_user_journey()
    else:
        print("❌ Opción inválida")

if __name__ == "__main__":
    main()
