# Bot de Ventas - Integración Bilderklo y AppSheet 🤖💬

Un sistema completo de automatización de ventas que integra Bilderklo y AppSheet con mensajería instantánea por WhatsApp.

## 🚀 **INICIO RÁPIDO**

### **Ejecutar el Bot (Método Más Fácil):**

```bash
# 1. Activar entorno virtual
source bot_ventas_env/bin/activate

# 2. Ejecutar bot simplificado
python3 bot_simple.py
```

### **Probar el Bot:**

```bash
# En otra terminal, ejecutar pruebas
python3 probar_bot.py
```

### **URLs del Bot:**
- **Dashboard:** http://localhost:5000
- **Salud:** http://localhost:5000/health
- **Webhook Usuarios:** http://localhost:5000/webhook/new-user
- **Webhook Actividad:** http://localhost:5000/webhook/user-activity

## 🚀 Características

- **Integración automática** entre Bilderklo y AppSheet
- **Mensajería instantánea** por WhatsApp usando Twilio
- **Bot de ventas inteligente** con mensajes personalizados
- **Webhooks en tiempo real** para nuevos registros
- **Seguimiento automático** de usuarios
- **Analíticas y reportes** de usuarios
- **Campañas de reactivación** automáticas
- **Exportación de datos** a Excel

## 📋 Requisitos

- Python 3.8+
- Cuenta de Twilio con WhatsApp Business API
- API de Bilderklo
- Acceso a AppSheet
- Servidor con IP pública para webhooks

## 🛠️ Instalación

1. **Clonar el repositorio:**
```bash
git clone <tu-repositorio>
cd bot-ventas-integration
```

2. **Ejecutar configuración automática:**
```bash
python setup.py
```

3. **Configurar credenciales:**
Edita el archivo `.env` con tus credenciales reales:
```env
BILDERKLO_API_KEY=tu_api_key_real
APPSHEET_APP_ID=tu_app_id_real
TWILIO_SID=tu_twilio_sid_real
# ... etc
```

4. **Configurar webhooks:**
```bash
python webhook_setup.py
```

5. **Iniciar el bot:**
```bash
python bot_ventas_integration.py
```

## 🔧 Configuración

### Variables de Entorno

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `BILDERKLO_API_KEY` | API Key de Bilderklo | `bk_1234567890abcdef` |
| `BILDERKLO_BASE_URL` | URL base de la API | `https://api.bilderklo.com` |
| `APPSHEET_APP_ID` | ID de la app de AppSheet | `12345678-1234-1234-1234-123456789012` |
| `APPSHEET_ACCESS_TOKEN` | Token de acceso | `V2-4Zxxx-xxx` |
| `TWILIO_SID` | SID de Twilio | `ACxxxxxxxxxxxxx` |
| `TWILIO_TOKEN` | Token de Twilio | `xxxxxxxxxxxxxxxx` |
| `TWILIO_PHONE` | Número de WhatsApp Business | `+1234567890` |
| `WEBHOOK_BASE_URL` | URL pública de tu servidor | `https://tu-servidor.com` |

### Configuración de AppSheet

1. Ve a tu app de AppSheet
2. Navega a `Automation > Bots`
3. Crea un nuevo bot con estos triggers:
   - **Evento:** Cuando se agrega una nueva fila a la tabla "Users"
   - **URL:** `https://tu-servidor.com/webhook/new-user`
   - **Método:** POST

### Configuración de Bilderklo

Los webhooks se configuran automáticamente ejecutando `webhook_setup.py`.

## 📡 API Endpoints

### POST /webhook/new-user
Recibe notificaciones de nuevos usuarios registrados.

**Payload de ejemplo:**
```json
{
  "user_id": "user_123",
  "name": "Juan Pérez",
  "email": "juan@example.com",
  "phone": "+1234567890",
  "source": "bilderklo"
}
```

### POST /webhook/user-activity
Recibe notificaciones de actividad de usuarios.

### GET /health
Endpoint de salud del servicio.

## 🤖 Funcionalidades del Bot

### Mensajes Automáticos

1. **Mensaje de Bienvenida:** Se envía inmediatamente al registrarse
2. **Mensaje de Seguimiento:** Se envía 24 horas después del registro
3. **Mensajes de Reactivación:** Para usuarios inactivos
4. **Mensajes de Carrito Abandonado:** Cuando detecta abandono

### Plantillas de Mensajes

Los mensajes están personalizados e incluyen:
- Saludo personalizado con el nombre del usuario
- Ofertas especiales para nuevos usuarios
- Descuentos y promociones
- Enlaces a contenido relevante
- Call-to-action claros

## 📊 Gestión de Usuarios

### Analíticas

Ejecuta `user_management.py` para obtener:
- Total de usuarios registrados
- Usuarios nuevos por día
- Distribución por fuente de registro
- Tendencias de registro
- Usuarios inactivos

### Exportación de Datos

```bash
python user_management.py
```

Esto generará un archivo Excel con todos los usuarios y sus datos.

### Campañas de Reactivación

El sistema identifica automáticamente usuarios inactivos y puede enviar campañas de reactivación:

```python
from user_management import UserManager
manager = UserManager()
manager.reactivation_campaign(days_threshold=7)
```

## 🔄 Flujo de Trabajo

1. **Usuario se registra** en Bilderklo
2. **Webhook notifica** al bot
3. **Bot procesa** la información del usuario
4. **Datos se sincronizan** con AppSheet
5. **Mensaje de bienvenida** se envía por WhatsApp
6. **Seguimiento automático** se programa
7. **Analíticas se actualizan** en tiempo real

## 🚦 Monitoreo

### Logs

Los logs se guardan en el directorio `logs/` con información detallada sobre:
- Webhooks recibidos
- Mensajes enviados
- Errores y excepciones
- Actividad de usuarios

### Health Check

Verifica el estado del servicio:
```bash
curl http://localhost:5000/health
```

## 🐳 Despliegue

### Como Servicio del Sistema

```bash
# Crear el servicio
sudo cp bot-ventas.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable bot-ventas
sudo systemctl start bot-ventas

# Verificar estado
sudo systemctl status bot-ventas
```

### Con Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "bot_ventas_integration.py"]
```

### En la Nube

Recomendaciones para despliegue:
- **Heroku:** Fácil despliegue con git
- **DigitalOcean App Platform:** Escalable y económico
- **AWS EC2:** Control total del servidor
- **Google Cloud Run:** Serverless y escalable

## 🔒 Seguridad

- Todas las credenciales se manejan via variables de entorno
- Los webhooks incluyen validación de origen
- Los logs no exponen información sensible
- Comunicación HTTPS requerida para webhooks

## 🐛 Solución de Problemas

### Error: "Missing environment variables"
Asegúrate de que todas las variables en `.env` estén configuradas correctamente.

### Error: "Webhook not receiving data"
1. Verifica que tu servidor sea accesible públicamente
2. Confirma que los webhooks estén configurados correctamente
3. Revisa los logs del servidor

### Error: "WhatsApp messages not sending"
1. Verifica las credenciales de Twilio
2. Confirma que el número de WhatsApp Business esté aprobado
3. Revisa el formato de los números de teléfono

## 📞 Soporte

Para soporte técnico:
1. Revisa los logs en `logs/`
2. Verifica la configuración en `.env`
3. Ejecuta `python webhook_setup.py` para verificar webhooks
4. Contacta al administrador del sistema

## 🔄 Actualizaciones

Para actualizar el sistema:
```bash
git pull origin main
pip install -r requirements.txt
sudo systemctl restart bot-ventas
```

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

---

**¡Tu bot de ventas está listo para aumentar las conversiones! 🚀💰**
