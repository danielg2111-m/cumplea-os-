import pandas as pd
import json
from datetime import datetime, timedelta
import os
from bot_ventas_integration import SalesBot
from dotenv import load_dotenv

load_dotenv()

class UserManager:
    """Gestión avanzada de usuarios y análisis"""
    
    def __init__(self):
        self.bot = SalesBot()
    
    def export_users_to_excel(self, filename: str = None):
        """Exportar usuarios a Excel"""
        if not filename:
            filename = f"usuarios_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        try:
            users = self.bot.appsheet.get_users()
            df = pd.DataFrame(users)
            df.to_excel(filename, index=False)
            print(f"✅ Usuarios exportados a {filename}")
            return filename
        except Exception as e:
            print(f"❌ Error exportando usuarios: {e}")
            return None
    
    def get_user_analytics(self):
        """Obtener analíticas de usuarios"""
        try:
            users = self.bot.appsheet.get_users()
            if not users:
                return {}
            
            df = pd.DataFrame(users)
            
            analytics = {
                'total_users': len(df),
                'new_users_today': len(df[df['registration_date'] >= datetime.now().date().isoformat()]),
                'users_by_source': df['source'].value_counts().to_dict() if 'source' in df.columns else {},
                'users_by_status': df['status'].value_counts().to_dict() if 'status' in df.columns else {},
                'registration_trend': self._get_registration_trend(df)
            }
            
            return analytics
        except Exception as e:
            print(f"❌ Error obteniendo analíticas: {e}")
            return {}
    
    def _get_registration_trend(self, df):
        """Obtener tendencia de registros por día"""
        if 'registration_date' not in df.columns:
            return {}
        
        df['date'] = pd.to_datetime(df['registration_date']).dt.date
        trend = df['date'].value_counts().sort_index()
        return {str(date): count for date, count in trend.items()}
    
    def send_bulk_message(self, user_filter: dict, message_template: str):
        """Enviar mensaje masivo a usuarios filtrados"""
        try:
            users = self.bot.appsheet.get_users()
            filtered_users = self._filter_users(users, user_filter)
            
            sent_count = 0
            for user in filtered_users:
                message = message_template.format(**user)
                if self.bot.messaging.send_whatsapp_message(user.get('phone', ''), message):
                    sent_count += 1
            
            print(f"✅ Mensajes enviados: {sent_count}/{len(filtered_users)}")
            return sent_count
        except Exception as e:
            print(f"❌ Error enviando mensajes masivos: {e}")
            return 0
    
    def _filter_users(self, users: list, filters: dict):
        """Filtrar usuarios según criterios"""
        filtered = users.copy()
        
        for key, value in filters.items():
            if key == 'registration_date_after':
                filtered = [u for u in filtered if u.get('registration_date', '') >= value]
            elif key == 'registration_date_before':
                filtered = [u for u in filtered if u.get('registration_date', '') <= value]
            elif key == 'source':
                filtered = [u for u in filtered if u.get('source') == value]
            elif key == 'status':
                filtered = [u for u in filtered if u.get('status') == value]
        
        return filtered
    
    def identify_inactive_users(self, days_threshold: int = 7):
        """Identificar usuarios inactivos"""
        try:
            users = self.bot.appsheet.get_users()
            threshold_date = (datetime.now() - timedelta(days=days_threshold)).isoformat()
            
            inactive_users = [
                user for user in users 
                if user.get('last_activity', user.get('registration_date', '')) < threshold_date
            ]
            
            return inactive_users
        except Exception as e:
            print(f"❌ Error identificando usuarios inactivos: {e}")
            return []
    
    def reactivation_campaign(self, days_threshold: int = 7):
        """Campaña de reactivación para usuarios inactivos"""
        inactive_users = self.identify_inactive_users(days_threshold)
        
        reactivation_message = """
¡Hola {name}! 👋

Te extrañamos en nuestra plataforma. 😔

¿Sabías que tenemos contenido nuevo esperándote?

🎁 Oferta especial para ti:
• 30% de descuento en cualquier plan
• Acceso gratuito a contenido premium
• Soporte personalizado

¿Te gustaría que te ayude a encontrar algo que te interese?

¡Vuelve cuando quieras! 💙
        """
        
        return self.send_bulk_message(
            {'status': 'inactive'}, 
            reactivation_message
        )

def main():
    """Función principal para gestión de usuarios"""
    manager = UserManager()
    
    print("📊 Analíticas de usuarios:")
    analytics = manager.get_user_analytics()
    print(json.dumps(analytics, indent=2, ensure_ascii=False))
    
    print("\n📁 Exportando usuarios a Excel...")
    manager.export_users_to_excel()
    
    print("\n🔍 Identificando usuarios inactivos...")
    inactive = manager.identify_inactive_users()
    print(f"Usuarios inactivos: {len(inactive)}")
    
    # Opcional: ejecutar campaña de reactivación
    # print("\n📧 Ejecutando campaña de reactivación...")
    # manager.reactivation_campaign()

if __name__ == "__main__":
    main()
