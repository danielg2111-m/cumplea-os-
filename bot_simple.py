#!/usr/bin/env python3
"""
Bot de Ventas Simplificado - Versión de Prueba
"""
import os
import json
import requests
from datetime import datetime, timedelta
import time
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import logging

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimpleSalesBot:
    """Bot de ventas simplificado para pruebas"""
    
    def __init__(self):
        # Flask app para webhooks
        self.app = Flask(__name__)
        self.setup_routes()
        
        # Lista de usuarios procesados
        self.processed_users = set()
        
        logger.info("Bot de ventas inicializado")
    
    def setup_routes(self):
        """Configurar rutas de Flask"""
        
        @self.app.route('/webhook/new-user', methods=['POST'])
        def handle_new_user():
            """Manejar webhook de nuevo usuario"""
            try:
                data = request.json
                logger.info(f"🆕 Nuevo usuario recibido: {data}")
                
                # Simular procesamiento
                success = self.process_new_user(data)
                
                return jsonify({
                    'status': 'success' if success else 'error',
                    'message': 'Usuario procesado correctamente' if success else 'Error procesando usuario',
                    'timestamp': datetime.now().isoformat(),
                    'user_data': data
                })
            except Exception as e:
                logger.error(f"❌ Error en webhook: {e}")
                return jsonify({'status': 'error', 'message': str(e)}), 500
        
        @self.app.route('/webhook/user-activity', methods=['POST'])
        def handle_user_activity():
            """Manejar webhook de actividad"""
            try:
                data = request.json
                logger.info(f"📊 Actividad recibida: {data}")
                
                return jsonify({
                    'status': 'success', 
                    'message': 'Actividad procesada',
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                logger.error(f"❌ Error en actividad: {e}")
                return jsonify({'status': 'error', 'message': str(e)}), 500
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """Endpoint de salud"""
            return jsonify({
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'version': '1.0.0',
                'users_processed': len(self.processed_users)
            })
        
        @self.app.route('/', methods=['GET'])
        def home():
            """Página de inicio"""
            return jsonify({
                'message': '🤖 Bot de Ventas - Integración Bilderklo y AppSheet',
                'status': 'running',
                'endpoints': {
                    'health': '/health',
                    'new_user': '/webhook/new-user',
                    'user_activity': '/webhook/user-activity'
                },
                'timestamp': datetime.now().isoformat()
            })
    
    def process_new_user(self, user_data):
        """Procesar nuevo usuario (versión simplificada)"""
        try:
            user_id = user_data.get('user_id', 'unknown')
            
            if user_id in self.processed_users:
                logger.info(f"👤 Usuario {user_id} ya fue procesado")
                return True
            
            # Simular procesamiento
            logger.info(f"✅ Procesando usuario: {user_data.get('name', 'Sin nombre')}")
            logger.info(f"📧 Email: {user_data.get('email', 'Sin email')}")
            logger.info(f"📱 Teléfono: {user_data.get('phone', 'Sin teléfono')}")
            
            # Simular envío de mensaje de bienvenida
            self.send_welcome_message(user_data)
            
            # Marcar como procesado
            self.processed_users.add(user_id)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error procesando usuario: {e}")
            return False
    
    def send_welcome_message(self, user_data):
        """Simular envío de mensaje de bienvenida"""
        name = user_data.get('name', 'Usuario')
        phone = user_data.get('phone', '')
        
        message = f"""
¡Hola {name}! 👋

¡Bienvenido/a a nuestra plataforma! 🎉

Mensaje de bienvenida enviado a: {phone}

Beneficios especiales:
• 20% de descuento en tu primera compra 🎁
• Acceso gratuito a contenido premium por 7 días ⭐
• Soporte prioritario 24/7 💬

¡Estamos aquí para ayudarte! 🤖
        """
        
        logger.info(f"📨 Mensaje de bienvenida enviado a {name}")
        logger.info(f"📄 Contenido: {message.strip()}")
        
        return True
    
    def start_server(self, host='0.0.0.0', port=5000, debug=False):
        """Iniciar servidor Flask"""
        logger.info(f"🚀 Iniciando Bot de Ventas en {host}:{port}")
        logger.info("📡 Endpoints disponibles:")
        logger.info("   GET  / - Información del bot")
        logger.info("   GET  /health - Estado del servicio")
        logger.info("   POST /webhook/new-user - Nuevos usuarios")
        logger.info("   POST /webhook/user-activity - Actividad de usuarios")
        
        self.app.run(host=host, port=port, debug=debug)

def main():
    """Función principal"""
    print("🤖 Bot de Ventas - Integración Bilderklo y AppSheet")
    print("=" * 60)
    
    # Crear e iniciar el bot
    bot = SimpleSalesBot()
    
    try:
        bot.start_server()
    except KeyboardInterrupt:
        print("\n👋 Bot detenido por el usuario")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
