#!/usr/bin/env python3
"""
Script de inicio fácil para el Bot de Ventas
"""
import subprocess
import sys
import os

def main():
    print("🤖 Bot de Ventas - Integración Bilderklo y AppSheet")
    print("=" * 60)
    
    # Verificar si estamos en el entorno virtual
    if 'bot_ventas_env' not in sys.executable:
        print("⚠️  Activando entorno virtual...")
        os.system("source bot_ventas_env/bin/activate")
    
    print("🚀 Iniciando Bot de Ventas...")
    print("📡 El bot estará disponible en: http://localhost:5000")
    print("🔗 Endpoints disponibles:")
    print("   • GET  /health - Estado del bot")
    print("   • POST /webhook/new-user - Nuevos usuarios")
    print("   • POST /webhook/user-activity - Actividad de usuarios")
    print("=" * 60)
    print("💡 Para detener el bot, presiona Ctrl+C")
    print("=" * 60)
    
    try:
        # Ejecutar el bot
        subprocess.run([sys.executable, "bot_simple.py"])
    except KeyboardInterrupt:
        print("\n👋 Bot detenido correctamente")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
