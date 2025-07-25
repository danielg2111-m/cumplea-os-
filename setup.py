#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

def install_requirements():
    """Instalar dependencias"""
    print("📦 Instalando dependencias...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencias instaladas correctamente")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False
    return True

def create_env_file():
    """Crear archivo .env si no existe"""
    if not Path(".env").exists():
        print("📝 Creando archivo .env...")
        with open(".env", "w") as f:
            f.write("""# Configuración de Bilderklo
BILDERKLO_API_KEY=tu_api_key_de_bilderklo
BILDERKLO_BASE_URL=https://api.bilderklo.com

# Configuración de AppSheet
APPSHEET_APP_ID=tu_app_id_de_appsheet
APPSHEET_ACCESS_TOKEN=tu_access_token_de_appsheet

# Configuración de Twilio para WhatsApp
TWILIO_SID=tu_twilio_sid
TWILIO_TOKEN=tu_twilio_token
TWILIO_PHONE=+1234567890

# URL base para webhooks (tu servidor público)
WEBHOOK_BASE_URL=https://tu-servidor.com

# Configuración del servidor
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=False

# Configuración de logging
LOG_LEVEL=INFO
""")
        print("✅ Archivo .env creado. ¡Recuerda configurar tus credenciales!")
    else:
        print("ℹ️ Archivo .env ya existe")

def create_directories():
    """Crear directorios necesarios"""
    directories = ["logs", "exports", "temp"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("✅ Directorios creados")

def setup_systemd_service():
    """Crear servicio systemd para el bot"""
    service_content = f"""[Unit]
Description=Bot de Ventas - Integración Bilderklo y AppSheet
After=network.target

[Service]
Type=simple
User={os.getenv('USER', 'ubuntu')}
WorkingDirectory={os.getcwd()}
Environment=PATH={os.getcwd()}/venv/bin
ExecStart={sys.executable} bot_ventas_integration.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
    
    service_path = "/etc/systemd/system/bot-ventas.service"
    print(f"📋 Para instalar como servicio del sistema, ejecuta:")
    print(f"sudo tee {service_path} << 'EOF'")
    print(service_content)
    print("EOF")
    print("sudo systemctl daemon-reload")
    print("sudo systemctl enable bot-ventas")
    print("sudo systemctl start bot-ventas")

def main():
    """Configuración principal"""
    print("🚀 Configurando Bot de Ventas - Integración Bilderklo y AppSheet")
    print("=" * 60)
    
    # Instalar dependencias
    if not install_requirements():
        return
    
    # Crear archivo .env
    create_env_file()
    
    # Crear directorios
    create_directories()
    
    # Mostrar información del servicio
    setup_systemd_service()
    
    print("\n" + "=" * 60)
    print("✅ Configuración completada!")
    print("\n📝 Pasos siguientes:")
    print("1. Edita el archivo .env con tus credenciales reales")
    print("2. Ejecuta 'python webhook_setup.py' para configurar webhooks")
    print("3. Ejecuta 'python bot_ventas_integration.py' para iniciar el bot")
    print("4. Opcional: Configura como servicio del sistema usando los comandos mostrados arriba")
    print("\n🔗 Endpoints disponibles:")
    print("- POST /webhook/new-user - Webhook para nuevos usuarios")
    print("- POST /webhook/user-activity - Webhook para actividad de usuarios")
    print("- GET /health - Estado del servicio")

if __name__ == "__main__":
    main()
