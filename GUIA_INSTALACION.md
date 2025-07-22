# 🚀 Guía de Instalación - Sistema de Análisis Electoral

## ✅ Estado del Sistema

**¡El sistema está completamente implementado y listo para usar!**

Todas las pruebas han pasado exitosamente:
- ✅ Estructura de archivos completa
- ✅ Módulos de análisis implementados
- ✅ Generación de datos funcionando
- ✅ Análisis básico operativo

## 📦 Componentes Implementados

### 1. **Análisis del Comportamiento Electoral y Segmentación** ✅
- **Archivo**: `electoral_analysis/data/demographic_segmentation.py`
- **Funcionalidades**:
  - Segmentación demográfica con K-means clustering
  - Análisis de patrones de voto por segmento
  - Predicción de participación electoral
  - Perfiles detallados de cada segmento

### 2. **Análisis de Redes Sociales de Candidatos** ✅
- **Archivos**: 
  - `electoral_analysis/social_media/social_media_analyzer.py`
  - `electoral_analysis/social_media/twitter_analyzer.py`
  - `electoral_analysis/social_media/facebook_analyzer.py`
  - `electoral_analysis/social_media/sentiment_analyzer.py`
- **Funcionalidades**:
  - Análisis de Twitter y Facebook
  - Análisis de sentimiento (TextBlob + VADER)
  - Métricas de engagement y alcance
  - Score de influencia digital
  - Comparación entre candidatos

### 3. **Predicción del Posible Ganador** ✅
- **Archivo**: `electoral_analysis/models/prediction_engine.py`
- **Funcionalidades**:
  - Modelos de Machine Learning (Random Forest, Gradient Boosting, Regresión Logística)
  - Predicción ensemble combinando múltiples modelos
  - Análisis de factores clave
  - Niveles de confianza para predicciones

## 🖥️ Interfaces de Usuario

### 1. **Aplicación de Línea de Comandos** ✅
- **Archivo**: `main_electoral_analysis.py`
- **Descripción**: Ejecuta análisis completo y genera reportes

### 2. **Dashboard Web Interactivo** ✅
- **Archivo**: `dashboard_electoral.py`
- **Descripción**: Interface web con Streamlit para visualización interactiva

## 📋 Instalación Paso a Paso

### Opción A: Instalación Completa (Recomendada)

```bash
# 1. Crear entorno virtual
python3 -m venv electoral_env
source electoral_env/bin/activate  # Linux/Mac
# o
electoral_env\Scripts\activate     # Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar análisis completo
python main_electoral_analysis.py

# 4. Lanzar dashboard interactivo
streamlit run dashboard_electoral.py
```

### Opción B: Instalación Mínima (Solo análisis básico)

```bash
# El sistema puede funcionar con Python estándar
# usando datos simulados sin APIs externas
python3 main_electoral_analysis.py
```

## 📊 Reportes Generados

El sistema genera automáticamente:

1. **`reporte_segmentacion.txt`**: Análisis demográfico detallado
2. **`reporte_redes_sociales.txt`**: Métricas de redes sociales  
3. **`reporte_prediccion_completo.txt`**: Predicción electoral completa
4. **`resumen_ejecutivo.txt`**: Resumen con conclusiones principales

## 🔧 Configuración Opcional

### APIs de Redes Sociales (Opcional)

Si tienes acceso a APIs reales, configura el archivo `.env`:

```env
# Twitter API
TWITTER_API_KEY=tu_api_key
TWITTER_API_SECRET=tu_api_secret
TWITTER_ACCESS_TOKEN=tu_access_token
TWITTER_ACCESS_TOKEN_SECRET=tu_access_token_secret
TWITTER_BEARER_TOKEN=tu_bearer_token

# Facebook API  
FACEBOOK_ACCESS_TOKEN=tu_access_token
FACEBOOK_APP_ID=tu_app_id
FACEBOOK_APP_SECRET=tu_app_secret
```

**Nota**: Sin APIs, el sistema usa datos simulados realistas.

## 🎯 Casos de Uso Implementados

### Para Analistas Políticos
```bash
# Análisis completo con segmentación
python main_electoral_analysis.py
```

### Para Medios de Comunicación
```bash
# Dashboard interactivo para reportajes
streamlit run dashboard_electoral.py
```

### Para Investigadores
```bash
# Acceso programático a todos los módulos
python -c "
from electoral_analysis.data import DataManager
from electoral_analysis.models import PredictionEngine
# Tu código de análisis aquí
"
```

## 📈 Funcionalidades Destacadas

### ✅ Análisis Demográfico
- 5 segmentos demográficos identificados automáticamente
- Patrones de preferencia por candidato
- Predicción de participación electoral

### ✅ Redes Sociales
- Análisis de Twitter y Facebook
- Score de influencia de 0-100
- Análisis de sentimiento positivo/negativo/neutral
- Ranking de candidatos por plataforma

### ✅ Predicción Electoral
- 3 modelos de ML diferentes
- Predicción ensemble con nivel de confianza
- Factores clave de influencia identificados
- Margen de victoria predicho

## 🚨 Resolución de Problemas

### Error: "ModuleNotFoundError"
```bash
# Instalar dependencias faltantes
pip install pandas numpy scikit-learn matplotlib seaborn
```

### Error: "Permission denied" al instalar
```bash
# Usar entorno virtual
python3 -m venv electoral_env
source electoral_env/bin/activate
pip install -r requirements.txt
```

### Error: APIs de redes sociales
```bash
# El sistema funciona sin APIs usando datos simulados
# No es necesario configurar APIs para demostración
```

## 📞 Soporte

- **Documentación completa**: Ver `README.md`
- **Código fuente**: Todos los archivos están comentados
- **Pruebas**: Ejecutar `python3 test_system.py`

## 🎉 ¡Listo para Usar!

El sistema está **100% funcional** y listo para:

1. **Análisis electoral completo** con datos simulados
2. **Segmentación demográfica** avanzada  
3. **Análisis de redes sociales** de candidatos
4. **Predicción de resultados** con múltiples modelos
5. **Visualización interactiva** en dashboard web

**¡Ejecuta `python3 main_electoral_analysis.py` para comenzar!**
