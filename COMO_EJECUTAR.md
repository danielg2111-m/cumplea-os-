# 🤖 Cómo Ejecutar el Bot de Ventas

## ✅ **El bot ya está configurado y funcionando!**

### **Método 1: Ejecutar Bot Simplificado (Recomendado)**

```bash
# 1. Activar entorno virtual
source bot_ventas_env/bin/activate

# 2. Ejecutar el bot
python3 bot_simple.py
```

### **Método 2: Ejecutar Bot Completo (Con todas las funciones)**

```bash
# 1. Activar entorno virtual
source bot_ventas_env/bin/activate

# 2. Configurar credenciales en .env (opcional)
# nano .env

# 3. Ejecutar bot completo
python3 bot_ventas_integration.py
```

## 🧪 **Probar el Bot**

### **Pruebas Automáticas:**
```bash
# Ejecutar todas las pruebas
echo "1" | python3 probar_bot.py
```

### **Pruebas Manuales:**
```bash
# 1. Verificar que está funcionando
curl http://localhost:5000/health

# 2. Probar webhook de usuario nuevo
curl -X POST -H "Content-Type: application/json" \
  -d '{"user_id":"test123","name":"Juan","email":"juan@test.com","phone":"+123456789"}' \
  http://localhost:5000/webhook/new-user

# 3. Probar webhook de actividad
curl -X POST -H "Content-Type: application/json" \
  -d '{"user_id":"test123","activity_type":"viewed_product"}' \
  http://localhost:5000/webhook/user-activity
```

## 🌐 **URLs Disponibles**

- **Dashboard Principal:** http://localhost:5000
- **Estado del Bot:** http://localhost:5000/health
- **Webhook Nuevos Usuarios:** http://localhost:5000/webhook/new-user
- **Webhook Actividad:** http://localhost:5000/webhook/user-activity

## 📱 **Configurar WhatsApp (Opcional)**

Para enviar mensajes reales por WhatsApp, edita el archivo `.env`:

```env
# Credenciales de Twilio
TWILIO_SID=tu_twilio_sid
TWILIO_TOKEN=tu_twilio_token
TWILIO_PHONE=+1234567890
```

## 🔧 **Funcionalidades del Bot**

✅ **Recibe webhooks** de nuevos usuarios
✅ **Procesa actividad** de usuarios  
✅ **Simula mensajes** de bienvenida
✅ **Registra usuarios** procesados
✅ **API REST** completa
✅ **Logs detallados** de actividad

## 🚀 **Para Producción**

1. **Configurar credenciales reales** en `.env`
2. **Usar bot completo:** `python3 bot_ventas_integration.py`
3. **Configurar webhooks** en Bilderklo y AppSheet
4. **Desplegar en servidor** con IP pública

## ❓ **Solución de Problemas**

### El bot no inicia:
```bash
# Verificar entorno virtual
source bot_ventas_env/bin/activate
pip install requests flask python-dotenv schedule
```

### Puerto ocupado:
```bash
# Cambiar puerto en el código o matar proceso
sudo lsof -i :5000
sudo kill -9 <PID>
```

### Error de dependencias:
```bash
# Reinstalar dependencias básicas
pip install requests flask python-dotenv schedule
```

---

## 🎉 **¡Tu Bot de Ventas está listo!**

El sistema está completamente funcional y listo para integrar con Bilderklo y AppSheet. Solo necesitas configurar las credenciales reales para producción.
