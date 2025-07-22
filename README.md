# Sistema de Análisis Electoral Completo 🗳️

Un sistema integral para el análisis del comportamiento electoral, segmentación demográfica, análisis de redes sociales y predicción de resultados electorales.

## 🎯 Características Principales

### 1. Análisis del Comportamiento Electoral y Segmentación
- **Segmentación demográfica** usando algoritmos de clustering K-means
- **Análisis de patrones de voto** por segmento poblacional
- **Predicción de participación electoral** por grupo demográfico
- **Perfiles detallados** de cada segmento identificado

### 2. Análisis de Redes Sociales
- **Monitoreo de Twitter y Facebook** de todos los candidatos
- **Análisis de sentimiento** en tiempo real del contenido
- **Métricas de engagement** y alcance
- **Score de influencia** digital
- **Comparación entre candidatos** en plataformas sociales

### 3. Predicción del Ganador
- **Modelos de Machine Learning** (Random Forest, Gradient Boosting, Regresión Logística)
- **Predicción ensemble** combinando múltiples modelos
- **Análisis de factores clave** que influyen en el resultado
- **Niveles de confianza** para cada predicción

## 🚀 Instalación y Configuración

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación

1. **Clonar el repositorio:**
```bash
git clone <repository-url>
cd electoral-analysis
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Configurar variables de entorno (opcional):**
```bash
cp .env.example .env
# Editar .env con tus credenciales de APIs de redes sociales
```

## 📊 Uso del Sistema

### Análisis Completo (Línea de Comandos)

Ejecutar el análisis completo con datos simulados:

```bash
python main_electoral_analysis.py
```

Este comando ejecutará:
1. Carga y análisis de datos electorales
2. Segmentación demográfica de votantes
3. Análisis de redes sociales de candidatos
4. Predicción electoral usando múltiples modelos
5. Generación de reportes detallados

### Dashboard Interactivo

Lanzar el dashboard web interactivo:

```bash
streamlit run dashboard_electoral.py
```

El dashboard incluye:
- **Resumen General**: Vista panorámica de resultados
- **Segmentación Demográfica**: Análisis detallado de segmentos
- **Redes Sociales**: Métricas y comparaciones de candidatos
- **Predicción Electoral**: Resultados de modelos predictivos
- **Comparación de Modelos**: Evaluación de rendimiento

## 📁 Estructura del Proyecto

```
electoral_analysis/
├── data/                          # Gestión de datos
│   ├── data_manager.py           # Carga y procesamiento de datos
│   └── demographic_segmentation.py # Segmentación demográfica
├── social_media/                 # Análisis de redes sociales
│   ├── social_media_analyzer.py  # Analizador principal
│   ├── twitter_analyzer.py       # Análisis de Twitter
│   ├── facebook_analyzer.py      # Análisis de Facebook
│   └── sentiment_analyzer.py     # Análisis de sentimiento
├── models/                       # Modelos predictivos
│   └── prediction_engine.py      # Motor de predicción
└── visualization/                # Visualización de datos
    └── electoral_visualizer.py   # Generador de gráficos

main_electoral_analysis.py        # Aplicación principal
dashboard_electoral.py            # Dashboard interactivo
requirements.txt                  # Dependencias del proyecto
.env.example                     # Plantilla de configuración
```

## 📈 Funcionalidades Detalladas

### Segmentación Demográfica
- Identifica **5 segmentos** demográficos distintos
- Analiza características por edad, género, educación, ingresos
- Calcula **patrones de preferencia** por candidato
- Predice **participación electoral** por segmento

### Análisis de Redes Sociales
- **Twitter**: Tweets, engagement, hashtags, menciones
- **Facebook**: Posts, likes, comentarios, shares
- **Sentimiento**: Análisis positivo/negativo/neutral
- **Influencia**: Score combinado de alcance y engagement

### Modelos Predictivos
- **Random Forest**: Modelo ensemble robusto
- **Gradient Boosting**: Optimización secuencial
- **Regresión Logística**: Modelo lineal interpretable
- **Ensemble**: Combinación ponderada de modelos

## 📊 Reportes Generados

El sistema genera automáticamente:

1. **reporte_segmentacion.txt**: Análisis demográfico detallado
2. **reporte_redes_sociales.txt**: Métricas de redes sociales
3. **reporte_prediccion_completo.txt**: Predicción electoral completa
4. **resumen_ejecutivo.txt**: Resumen con conclusiones principales

## 🔧 Configuración de APIs

### Twitter API (Opcional)
```env
TWITTER_API_KEY=tu_api_key
TWITTER_API_SECRET=tu_api_secret
TWITTER_ACCESS_TOKEN=tu_access_token
TWITTER_ACCESS_TOKEN_SECRET=tu_access_token_secret
TWITTER_BEARER_TOKEN=tu_bearer_token
```

### Facebook API (Opcional)
```env
FACEBOOK_ACCESS_TOKEN=tu_access_token
FACEBOOK_APP_ID=tu_app_id
FACEBOOK_APP_SECRET=tu_app_secret
```

**Nota**: Sin credenciales de API, el sistema usa datos simulados realistas para demostración.

## 📋 Ejemplos de Uso

### Análisis Básico
```python
from electoral_analysis.data import DataManager
from electoral_analysis.models import PredictionEngine

# Cargar datos
data_manager = DataManager()
data = data_manager.load_electoral_data()

# Realizar predicción
predictor = PredictionEngine()
results = predictor.generate_prediction_report(data)
```

### Análisis de Redes Sociales
```python
from electoral_analysis.social_media import SocialMediaAnalyzer

# Configurar analizador
analyzer = SocialMediaAnalyzer()
analyzer.add_candidate("Candidato", {"twitter": "@usuario"})

# Analizar
results = analyzer.analyze_all_candidates()
comparison = analyzer.compare_candidates()
```

## 🎯 Casos de Uso

### Para Analistas Políticos
- Segmentación de votantes para estrategias dirigidas
- Monitoreo de percepción en redes sociales
- Predicción de resultados electorales

### Para Medios de Comunicación
- Análisis de tendencias electorales
- Comparación objetiva de candidatos
- Visualizaciones para reportajes

### Para Candidatos y Partidos
- Análisis de su propia presencia digital
- Identificación de segmentos clave
- Optimización de estrategias de campaña

### Para Investigadores
- Estudio de comportamiento electoral
- Análisis de influencia de redes sociales
- Validación de modelos predictivos

## 🔍 Metodología

### Segmentación
1. **Clustering K-means** en variables demográficas
2. **Normalización** de características numéricas
3. **Codificación** de variables categóricas
4. **Validación** de segmentos resultantes

### Predicción
1. **Ingeniería de características** demográficas y sociales
2. **Entrenamiento** de múltiples modelos
3. **Validación cruzada** para evaluar rendimiento
4. **Ensemble** ponderado para predicción final

### Redes Sociales
1. **Extracción** de métricas de engagement
2. **Análisis de sentimiento** con VADER y TextBlob
3. **Cálculo de influencia** multifactorial
4. **Comparación** entre candidatos

## ⚠️ Limitaciones

- Los datos simulados son para **demostración** únicamente
- Las predicciones están sujetas a **cambios temporales**
- Factores externos (eventos, crisis) **no se consideran**
- Margen de error inherente a **modelos estadísticos**

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 📞 Soporte

Para preguntas, problemas o sugerencias:
- Abre un **Issue** en GitHub
- Contacta al equipo de desarrollo
- Revisa la documentación en el código

## 🔮 Próximas Características

- [ ] Integración con más plataformas sociales (Instagram, TikTok)
- [ ] Análisis de noticias y medios tradicionales
- [ ] Modelos de deep learning para predicción
- [ ] API REST para integración externa
- [ ] Análisis geoespacial por regiones
- [ ] Dashboard en tiempo real
- [ ] Alertas automáticas de cambios significativos

---

**Desarrollado con ❤️ para el análisis electoral moderno**
