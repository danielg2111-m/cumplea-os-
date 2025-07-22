import os
import json
import requests
# import pandas as pd  # Comentado temporalmente
from datetime import datetime, timedelta
import schedule
import time
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import logging
from typing import Dict, List, Optional
import threading

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BilderkloBridge:
    """Clase para manejar la integración con Bilderklo"""
    
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    def get_user_data(self, user_id: str) -> Dict:
        """Obtener datos del usuario de Bilderklo"""
        try:
            response = requests.get(
                f"{self.base_url}/users/{user_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error obteniendo datos de usuario de Bilderklo: {e}")
            return {}
    
    def get_user_images(self, user_id: str) -> List[Dict]:
        """Obtener imágenes del usuario"""
        try:
            response = requests.get(
                f"{self.base_url}/users/{user_id}/images",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error obteniendo imágenes de usuario: {e}")
            return []

class AppSheetConnector:
    """Clase para manejar la integración con AppSheet"""
    
    def __init__(self, app_id: str, access_token: str):
        self.app_id = app_id
        self.access_token = access_token
        self.base_url = "https://api.appsheet.com/api/v2/apps"
        self.headers = {
            'ApplicationAccessKey': access_token,
            'Content-Type': 'application/json'
        }
    
    def add_user_to_sheet(self, user_data: Dict) -> bool:
        """Agregar usuario a AppSheet"""
        try:
            payload = {
                "Action": "Add",
                "Properties": {},
                "Rows": [user_data]
            }
            
            response = requests.post(
                f"{self.base_url}/{self.app_id}/tables/Users/Action",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            logger.info(f"Usuario agregado a AppSheet: {user_data.get('email', 'N/A')}")
            return True
        except Exception as e:
            logger.error(f"Error agregando usuario a AppSheet: {e}")
            return False
    
    def get_users(self) -> List[Dict]:
        """Obtener todos los usuarios de AppSheet"""
        try:
            payload = {
                "Action": "Find",
                "Properties": {},
                "Rows": []
            }
            
            response = requests.post(
                f"{self.base_url}/{self.app_id}/tables/Users/Action",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error obteniendo usuarios de AppSheet: {e}")
            return []

class MessagingBot:
    """Bot de mensajería instantánea para ventas"""
    
    def __init__(self, twilio_sid: str, twilio_token: str, twilio_phone: str):
        self.twilio_sid = twilio_sid
        self.twilio_token = twilio_token
        self.twilio_phone = twilio_phone
        
        # Plantillas de mensajes
        self.welcome_template = """
¡Hola {name}! 👋

¡Bienvenido/a a nuestra plataforma! 🎉

Hemos visto que te has registrado y queremos darte la bienvenida personalmente. 

Aquí tienes algunos beneficios especiales para nuevos usuarios:
• 20% de descuento en tu primera compra 🎁
• Acceso gratuito a contenido premium por 7 días ⭐
• Soporte prioritario 24/7 💬

¿Te gustaría que te ayude a configurar tu perfil o tienes alguna pregunta?

¡Estoy aquí para ayudarte! 🤖
        """
        
        self.follow_up_template = """
¡Hola {name}! 👋

Espero que estés disfrutando de nuestra plataforma. 

He notado que aún no has aprovechado tu descuento del 20%. 
¿Hay algo específico que te interese? 

Puedo ayudarte a encontrar:
• Contenido personalizado según tus gustos 🎯
• Ofertas especiales de la semana 💰
• Tutoriales para aprovechar al máximo la plataforma 📚

¿En qué puedo ayudarte hoy?
        """
    
    def send_whatsapp_message(self, phone: str, message: str) -> bool:
        """Enviar mensaje por WhatsApp usando Twilio"""
        try:
            from twilio.rest import Client
            client = Client(self.twilio_sid, self.twilio_token)
            
            message = client.messages.create(
                body=message,
                from_=f'whatsapp:{self.twilio_phone}',
                to=f'whatsapp:{phone}'
            )
            
            logger.info(f"Mensaje enviado a {phone}: {message.sid}")
            return True
        except Exception as e:
            logger.error(f"Error enviando WhatsApp a {phone}: {e}")
            return False
    
    def send_welcome_message(self, user_data: Dict) -> bool:
        """Enviar mensaje de bienvenida"""
        name = user_data.get('name', 'Usuario')
        phone = user_data.get('phone', '')
        
        if not phone:
            logger.warning("No se encontró número de teléfono para el usuario")
            return False
        
        message = self.welcome_template.format(name=name)
        return self.send_whatsapp_message(phone, message)
    
    def send_follow_up_message(self, user_data: Dict) -> bool:
        """Enviar mensaje de seguimiento"""
        name = user_data.get('name', 'Usuario')
        phone = user_data.get('phone', '')
        
        if not phone:
            logger.warning("No se encontró número de teléfono para seguimiento")
            return False
        
        message = self.follow_up_template.format(name=name)
        return self.send_whatsapp_message(phone, message)

class SalesBot:
    """Bot principal de ventas que integra todos los servicios"""
    
    def __init__(self):
        # Inicializar componentes
        self.bilderklo = BilderkloBridge(
            api_key=os.getenv('BILDERKLO_API_KEY'),
            base_url=os.getenv('BILDERKLO_BASE_URL', 'https://api.bilderklo.com')
        )
        
        self.appsheet = AppSheetConnector(
            app_id=os.getenv('APPSHEET_APP_ID'),
            access_token=os.getenv('APPSHEET_ACCESS_TOKEN')
        )
        
        self.messaging = MessagingBot(
            twilio_sid=os.getenv('TWILIO_SID'),
            twilio_token=os.getenv('TWILIO_TOKEN'),
            twilio_phone=os.getenv('TWILIO_PHONE')
        )
        
        # Flask app para webhooks
        self.app = Flask(__name__)
        self.setup_routes()
        
        # Lista de usuarios procesados para evitar duplicados
        self.processed_users = set()
    
    def setup_routes(self):
        """Configurar rutas de Flask para webhooks"""
        
        @self.app.route('/webhook/new-user', methods=['POST'])
        def handle_new_user():
            """Manejar webhook de nuevo usuario"""
            try:
                data = request.json
                logger.info(f"Nuevo usuario recibido: {data}")
                
                # Procesar nuevo usuario
                success = self.process_new_user(data)
                
                return jsonify({
                    'status': 'success' if success else 'error',
                    'message': 'Usuario procesado' if success else 'Error procesando usuario'
                })
            except Exception as e:
                logger.error(f"Error en webhook de nuevo usuario: {e}")
                return jsonify({'status': 'error', 'message': str(e)}), 500
        
        @self.app.route('/webhook/user-activity', methods=['POST'])
        def handle_user_activity():
            """Manejar webhook de actividad de usuario"""
            try:
                data = request.json
                logger.info(f"Actividad de usuario recibida: {data}")
                
                # Procesar actividad
                self.process_user_activity(data)
                
                return jsonify({'status': 'success', 'message': 'Actividad procesada'})
            except Exception as e:
                logger.error(f"Error en webhook de actividad: {e}")
                return jsonify({'status': 'error', 'message': str(e)}), 500
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """Endpoint de salud"""
            return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})
    
    def process_new_user(self, user_data: Dict) -> bool:
        """Procesar nuevo usuario registrado"""
        try:
            user_id = user_data.get('user_id')
            if user_id in self.processed_users:
                logger.info(f"Usuario {user_id} ya fue procesado")
                return True
            
            # Obtener datos adicionales de Bilderklo si es necesario
            if user_data.get('source') == 'bilderklo':
                bilderklo_data = self.bilderklo.get_user_data(user_id)
                user_data.update(bilderklo_data)
            
            # Agregar usuario a AppSheet
            appsheet_success = self.appsheet.add_user_to_sheet({
                'user_id': user_id,
                'name': user_data.get('name', ''),
                'email': user_data.get('email', ''),
                'phone': user_data.get('phone', ''),
                'registration_date': datetime.now().isoformat(),
                'source': user_data.get('source', 'unknown'),
                'status': 'new'
            })
            
            # Enviar mensaje de bienvenida
            message_success = self.messaging.send_welcome_message(user_data)
            
            # Programar mensaje de seguimiento para 24 horas después
            self.schedule_follow_up(user_data)
            
            # Marcar como procesado
            self.processed_users.add(user_id)
            
            logger.info(f"Usuario procesado exitosamente: {user_id}")
            return appsheet_success and message_success
            
        except Exception as e:
            logger.error(f"Error procesando nuevo usuario: {e}")
            return False
    
    def process_user_activity(self, activity_data: Dict):
        """Procesar actividad de usuario para bot de ventas"""
        try:
            user_id = activity_data.get('user_id')
            activity_type = activity_data.get('activity_type')
            
            # Lógica de bot de ventas basada en actividad
            if activity_type == 'viewed_product':
                self.handle_product_view(user_id, activity_data)
            elif activity_type == 'abandoned_cart':
                self.handle_cart_abandonment(user_id, activity_data)
            elif activity_type == 'no_activity':
                self.handle_inactive_user(user_id, activity_data)
                
        except Exception as e:
            logger.error(f"Error procesando actividad de usuario: {e}")
    
    def handle_product_view(self, user_id: str, data: Dict):
        """Manejar visualización de producto"""
        # Enviar mensaje personalizado sobre el producto visto
        pass
    
    def handle_cart_abandonment(self, user_id: str, data: Dict):
        """Manejar carrito abandonado"""
        # Enviar mensaje de recuperación de carrito
        pass
    
    def handle_inactive_user(self, user_id: str, data: Dict):
        """Manejar usuario inactivo"""
        # Enviar mensaje de reactivación
        pass
    
    def schedule_follow_up(self, user_data: Dict):
        """Programar mensaje de seguimiento"""
        def send_follow_up():
            self.messaging.send_follow_up_message(user_data)
        
        # Programar para 24 horas después
        schedule.every(24).hours.do(send_follow_up)
    
    def run_scheduled_tasks(self):
        """Ejecutar tareas programadas"""
        while True:
            schedule.run_pending()
            time.sleep(60)  # Verificar cada minuto
    
    def start_server(self, host='0.0.0.0', port=5000, debug=False):
        """Iniciar servidor Flask"""
        # Iniciar tareas programadas en un hilo separado
        scheduler_thread = threading.Thread(target=self.run_scheduled_tasks)
        scheduler_thread.daemon = True
        scheduler_thread.start()
        
        logger.info(f"Iniciando servidor en {host}:{port}")
        self.app.run(host=host, port=port, debug=debug)

def main():
    """Función principal"""
    # Verificar variables de entorno requeridas
    required_vars = [
        'BILDERKLO_API_KEY',
        'APPSHEET_APP_ID',
        'APPSHEET_ACCESS_TOKEN',
        'TWILIO_SID',
        'TWILIO_TOKEN',
        'TWILIO_PHONE'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        logger.error(f"Variables de entorno faltantes: {missing_vars}")
        logger.info("Por favor, configura estas variables en tu archivo .env")
        return
    
    # Crear e iniciar el bot
    bot = SalesBot()
    bot.start_server()

if __name__ == "__main__":
    main()
