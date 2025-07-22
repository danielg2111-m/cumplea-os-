# 🤖 Survey AI Analyzer

**Máquina de Inteligencia Artificial para Análisis de Datos de Encuestas**

Una aplicación completa que utiliza inteligencia artificial para analizar datos de encuestas, proporcionando insights automáticos, análisis de sentimientos, clustering, visualizaciones interactivas y recomendaciones basadas en IA.

## ✨ Características Principales

### 🧠 Análisis con IA
- **Análisis de Sentimientos**: Procesamiento de texto con modelos BERT multilingües
- **Clustering Automático**: Segmentación inteligente de respuestas
- **Detección de Patrones**: Identificación automática de tendencias y anomalías
- **Insights Automáticos**: Generación de hallazgos clave con IA

### 📊 Análisis Estadístico Avanzado
- Estadísticas descriptivas completas
- Análisis de correlaciones
- Detección de outliers
- Análisis de distribuciones
- Métricas de calidad de datos

### 📈 Visualizaciones Interactivas
- Gráficos de barras y pastel
- Histogramas y box plots
- Mapas de calor de correlaciones
- Nubes de palabras
- Gráficos de dispersión
- Visualizaciones de clusters

### 🔍 Capacidades de IA
- Procesamiento de lenguaje natural
- Análisis predictivo
- Recomendaciones automáticas
- Identificación de factores de riesgo
- Oportunidades de mejora

## 🚀 Inicio Rápido

### Opción 1: Script de Inicio Automático (Recomendado)

```bash
# Clonar el repositorio
git clone <repository-url>
cd survey-ai-analyzer

# Ejecutar script de inicio
./start.sh
```

El script automáticamente:
- Instala las dependencias de Python
- Descarga los modelos de IA necesarios
- Inicia el servidor backend (puerto 8000)
- Inicia el frontend React (puerto 3000)

### Opción 2: Instalación Manual

#### Backend (Python/FastAPI)

```bash
# Instalar dependencias
pip install -r requirements.txt

# Descargar modelos de NLTK
python -c "import nltk; nltk.download('punkt'); nltk.download('vader_lexicon')"

# Crear directorio de datos
mkdir -p data/surveys

# Iniciar servidor
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend (React)

```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar aplicación
npm start
```

### Opción 3: Docker

```bash
# Iniciar con Docker Compose
docker-compose up --build

# O solo el backend
docker build -t survey-ai .
docker run -p 8000:8000 survey-ai
```

## 📁 Estructura del Proyecto

```
survey-ai-analyzer/
├── main.py                    # Servidor FastAPI principal
├── requirements.txt           # Dependencias Python
├── start.sh                  # Script de inicio automático
├── docker-compose.yml        # Configuración Docker
├── Dockerfile               # Imagen Docker backend
├── 
├── src/                     # Código fuente backend
│   ├── analysis/           # Módulos de análisis
│   │   ├── sentiment_analyzer.py    # Análisis de sentimientos
│   │   ├── data_processor.py        # Procesamiento de datos
│   │   ├── visualizer.py           # Generación de gráficos
│   │   └── ai_insights.py          # Insights con IA
│   ├── models/             # Modelos de datos
│   │   └── survey_models.py        # Esquemas Pydantic
│   └── utils/              # Utilidades
│
├── frontend/               # Aplicación React
│   ├── public/            # Archivos públicos
│   ├── src/               # Código fuente frontend
│   │   ├── components/    # Componentes React
│   │   ├── pages/         # Páginas principales
│   │   ├── services/      # Servicios API
│   │   └── utils/         # Utilidades frontend
│   ├── package.json       # Dependencias Node.js
│   └── Dockerfile         # Imagen Docker frontend
│
└── data/                  # Datos y almacenamiento
    └── surveys/           # Encuestas procesadas
```

## 🎯 Uso de la Aplicación

### 1. Subir Encuesta
- Formatos soportados: CSV, Excel (.xlsx, .xls), JSON
- Carga automática y validación de datos
- Preview de datos y tipos detectados

### 2. Configurar Análisis
Selecciona los tipos de análisis deseados:
- **Descriptivo**: Estadísticas básicas y distribuciones
- **Sentimientos**: Análisis de emociones en texto
- **Clustering**: Agrupación de respuestas similares
- **Correlaciones**: Relaciones entre variables
- **Patrones**: Detección automática de tendencias

### 3. Revisar Resultados
- **Dashboard Interactivo**: Métricas clave y visualizaciones
- **Insights de IA**: Hallazgos automáticos y recomendaciones
- **Visualizaciones**: Gráficos interactivos y exportables
- **Reportes**: Resúmenes ejecutivos generados automáticamente

## 🛠️ Tecnologías Utilizadas

### Backend
- **FastAPI**: Framework web moderno y rápido
- **Pandas**: Manipulación y análisis de datos
- **Scikit-learn**: Machine learning y clustering
- **NLTK & TextBlob**: Procesamiento de lenguaje natural
- **Transformers**: Modelos BERT para análisis de sentimientos
- **Plotly**: Visualizaciones interactivas
- **WordCloud**: Nubes de palabras

### Frontend
- **React 18**: Biblioteca de interfaz de usuario
- **Material-UI**: Componentes de diseño moderno
- **Plotly.js**: Gráficos interactivos
- **Axios**: Cliente HTTP
- **React Router**: Navegación SPA

### Infraestructura
- **Docker**: Containerización
- **PostgreSQL**: Base de datos (opcional)
- **Uvicorn**: Servidor ASGI

## 📊 Ejemplos de Análisis

### Análisis de Sentimientos
```python
# Automáticamente detecta:
- Sentimiento positivo/negativo/neutral
- Polaridad emocional (-1 a +1)
- Palabras clave emocionales
- Distribución de sentimientos por pregunta
```

### Clustering Inteligente
```python
# Identifica grupos automáticamente:
- Segmentación de respondentes
- Características de cada cluster
- Visualización PCA 2D
- Estadísticas por grupo
```

### Insights Automáticos
```python
# Genera automáticamente:
- Hallazgos clave estadísticos
- Patrones de comportamiento
- Factores de riesgo
- Oportunidades de mejora
- Recomendaciones accionables
```

## 🔧 Configuración Avanzada

### Variables de Entorno
Crea un archivo `.env` basado en `.env.example`:

```bash
# APIs externas (opcional)
OPENAI_API_KEY=tu-clave-openai
HUGGINGFACE_TOKEN=tu-token-huggingface

# Base de datos (opcional)
DATABASE_URL=postgresql://user:pass@localhost/surveyai

# Configuración
DEBUG=True
SECRET_KEY=tu-clave-secreta
```

### Personalización de Modelos
```python
# En src/analysis/sentiment_analyzer.py
# Cambiar modelo de sentimientos:
self.sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="tu-modelo-personalizado"
)
```

## 📖 API Documentation

Una vez iniciado el servidor, la documentación interactiva está disponible en:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints Principales

- `POST /upload-survey`: Subir archivo de encuesta
- `POST /analyze`: Realizar análisis completo
- `GET /ai-insights/{survey_id}`: Obtener insights de IA
- `GET /visualizations/{survey_id}`: Generar visualizaciones
- `GET /surveys`: Listar encuestas guardadas

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🆘 Soporte

Si encuentras algún problema o tienes preguntas:

1. Revisa la documentación
2. Busca en los issues existentes
3. Crea un nuevo issue con detalles del problema

## 🎉 Características Futuras

- [ ] Análisis de series temporales
- [ ] Integración con APIs de encuestas (SurveyMonkey, Google Forms)
- [ ] Exportación de reportes en PDF
- [ ] Análisis comparativo entre encuestas
- [ ] Dashboard en tiempo real
- [ ] Análisis de texto más avanzado con GPT
- [ ] Predicciones y forecasting
- [ ] Integración con herramientas de BI

---

**¡Transforma tus datos de encuestas en insights accionables con el poder de la IA! 🚀**
