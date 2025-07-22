import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class WebhookSetup:
    """Clase para configurar webhooks en Bilderklo y AppSheet"""
    
    def __init__(self):
        self.bilderklo_api_key = os.getenv('BILDERKLO_API_KEY')
        self.bilderklo_base_url = os.getenv('BILDERKLO_BASE_URL')
        self.appsheet_app_id = os.getenv('APPSHEET_APP_ID')
        self.appsheet_token = os.getenv('APPSHEET_ACCESS_TOKEN')
        self.webhook_url = os.getenv('WEBHOOK_BASE_URL', 'https://tu-servidor.com')
    
    def setup_bilderklo_webhooks(self):
        """Configurar webhooks en Bilderklo"""
        webhooks = [
            {
                'event': 'user.registered',
                'url': f'{self.webhook_url}/webhook/new-user',
                'method': 'POST'
            },
            {
                'event': 'user.activity',
                'url': f'{self.webhook_url}/webhook/user-activity',
                'method': 'POST'
            }
        ]
        
        headers = {
            'Authorization': f'Bearer {self.bilderklo_api_key}',
            'Content-Type': 'application/json'
        }
        
        for webhook in webhooks:
            try:
                response = requests.post(
                    f'{self.bilderklo_base_url}/webhooks',
                    headers=headers,
                    json=webhook
                )
                if response.status_code == 201:
                    print(f"✅ Webhook configurado: {webhook['event']}")
                else:
                    print(f"❌ Error configurando webhook {webhook['event']}: {response.text}")
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def setup_appsheet_webhooks(self):
        """Configurar webhooks en AppSheet"""
        # AppSheet usa un enfoque diferente para webhooks
        # Normalmente se configuran desde la interfaz web
        print("📝 Para AppSheet, configura los webhooks desde la interfaz web:")
        print(f"   - URL: {self.webhook_url}/webhook/new-user")
        print(f"   - Evento: Cuando se agrega una nueva fila")
        print(f"   - Método: POST")
    
    def test_webhooks(self):
        """Probar que los webhooks funcionan"""
        test_data = {
            'user_id': 'test_user_123',
            'name': 'Usuario de Prueba',
            'email': 'test@example.com',
            'phone': '+1234567890',
            'source': 'test'
        }
        
        try:
            response = requests.post(
                f'{self.webhook_url}/webhook/new-user',
                json=test_data
            )
            if response.status_code == 200:
                print("✅ Webhook de prueba funcionando")
            else:
                print(f"❌ Error en webhook de prueba: {response.text}")
        except Exception as e:
            print(f"❌ Error probando webhook: {e}")

def main():
    setup = WebhookSetup()
    
    print("🔧 Configurando webhooks...")
    setup.setup_bilderklo_webhooks()
    setup.setup_appsheet_webhooks()
    
    print("\n🧪 Probando webhooks...")
    setup.test_webhooks()

if __name__ == "__main__":
    main()
