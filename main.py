from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
import pandas as pd
import numpy as np
import json
import io
from typing import List, Dict, Any, Optional
import uvicorn
from datetime import datetime
import os

# Importar módulos de análisis
from src.analysis.sentiment_analyzer import SentimentAnalyzer
from src.analysis.data_processor import DataProcessor
from src.analysis.visualizer import Visualizer
from src.analysis.ai_insights import AIInsights
from src.models.survey_models import SurveyData, AnalysisRequest, AnalysisResponse

app = FastAPI(
    title="Survey AI Analyzer",
    description="Máquina de Inteligencia Artificial para Análisis de Datos de Encuestas",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar componentes de IA
sentiment_analyzer = SentimentAnalyzer()
data_processor = DataProcessor()
visualizer = Visualizer()
ai_insights = AIInsights()

@app.on_event("startup")
async def startup_event():
    """Inicializar la aplicación y cargar modelos de IA"""
    print("🚀 Iniciando Survey AI Analyzer...")
    await sentiment_analyzer.initialize()
    print("✅ Modelos de IA cargados correctamente")

@app.get("/")
async def root():
    return {
        "message": "Survey AI Analyzer - Máquina de IA para Análisis de Encuestas",
        "version": "1.0.0",
        "endpoints": {
            "upload": "/upload-survey",
            "analyze": "/analyze",
            "insights": "/ai-insights",
            "visualizations": "/visualizations"
        }
    }

@app.post("/upload-survey")
async def upload_survey(file: UploadFile = File(...)):
    """Subir archivo de encuesta (CSV, Excel, JSON)"""
    try:
        # Validar tipo de archivo
        if not file.filename.endswith(('.csv', '.xlsx', '.xls', '.json')):
            raise HTTPException(
                status_code=400, 
                detail="Formato no soportado. Use CSV, Excel o JSON"
            )
        
        # Leer contenido del archivo
        content = await file.read()
        
        # Procesar según el tipo de archivo
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.StringIO(content.decode('utf-8')))
        elif file.filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(io.BytesIO(content))
        elif file.filename.endswith('.json'):
            data = json.loads(content.decode('utf-8'))
            df = pd.DataFrame(data)
        
        # Procesar y validar datos
        processed_data = data_processor.process_survey_data(df)
        
        # Guardar datos temporalmente
        survey_id = f"survey_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        data_processor.save_survey_data(survey_id, processed_data)
        
        return {
            "survey_id": survey_id,
            "filename": file.filename,
            "rows": len(processed_data),
            "columns": list(processed_data.columns),
            "preview": processed_data.head().to_dict('records'),
            "data_types": data_processor.analyze_data_types(processed_data)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando archivo: {str(e)}")

@app.post("/analyze")
async def analyze_survey(request: AnalysisRequest):
    """Realizar análisis completo de la encuesta"""
    try:
        # Cargar datos de la encuesta
        survey_data = data_processor.load_survey_data(request.survey_id)
        
        if survey_data is None:
            raise HTTPException(status_code=404, detail="Encuesta no encontrada")
        
        # Realizar diferentes tipos de análisis
        results = {}
        
        # 1. Análisis descriptivo
        if "descriptive" in request.analysis_types:
            results["descriptive"] = data_processor.descriptive_analysis(survey_data)
        
        # 2. Análisis de sentimientos
        if "sentiment" in request.analysis_types:
            text_columns = data_processor.get_text_columns(survey_data)
            if text_columns:
                results["sentiment"] = await sentiment_analyzer.analyze_survey_sentiment(
                    survey_data, text_columns
                )
        
        # 3. Análisis de clustering
        if "clustering" in request.analysis_types:
            results["clustering"] = data_processor.perform_clustering(survey_data)
        
        # 4. Análisis de correlaciones
        if "correlation" in request.analysis_types:
            results["correlation"] = data_processor.correlation_analysis(survey_data)
        
        # 5. Detección de patrones
        if "patterns" in request.analysis_types:
            results["patterns"] = data_processor.detect_patterns(survey_data)
        
        return AnalysisResponse(
            survey_id=request.survey_id,
            analysis_timestamp=datetime.now(),
            results=results,
            summary=data_processor.generate_summary(results)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en análisis: {str(e)}")

@app.get("/ai-insights/{survey_id}")
async def get_ai_insights(survey_id: str):
    """Obtener insights generados por IA"""
    try:
        # Cargar datos y resultados de análisis
        survey_data = data_processor.load_survey_data(survey_id)
        if survey_data is None:
            raise HTTPException(status_code=404, detail="Encuesta no encontrada")
        
        # Generar insights con IA
        insights = await ai_insights.generate_insights(survey_data)
        
        return {
            "survey_id": survey_id,
            "insights": insights,
            "recommendations": ai_insights.generate_recommendations(insights),
            "key_findings": ai_insights.extract_key_findings(insights)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando insights: {str(e)}")

@app.get("/visualizations/{survey_id}")
async def get_visualizations(survey_id: str, chart_types: Optional[str] = None):
    """Generar visualizaciones de los datos"""
    try:
        survey_data = data_processor.load_survey_data(survey_id)
        if survey_data is None:
            raise HTTPException(status_code=404, detail="Encuesta no encontrada")
        
        # Tipos de gráficos solicitados
        requested_charts = chart_types.split(',') if chart_types else ['all']
        
        # Generar visualizaciones
        visualizations = visualizer.create_visualizations(survey_data, requested_charts)
        
        return {
            "survey_id": survey_id,
            "visualizations": visualizations,
            "available_charts": visualizer.get_available_chart_types()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando visualizaciones: {str(e)}")

@app.get("/surveys")
async def list_surveys():
    """Listar todas las encuestas cargadas"""
    try:
        surveys = data_processor.list_surveys()
        return {"surveys": surveys}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listando encuestas: {str(e)}")

@app.delete("/surveys/{survey_id}")
async def delete_survey(survey_id: str):
    """Eliminar una encuesta"""
    try:
        success = data_processor.delete_survey(survey_id)
        if success:
            return {"message": f"Encuesta {survey_id} eliminada correctamente"}
        else:
            raise HTTPException(status_code=404, detail="Encuesta no encontrada")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error eliminando encuesta: {str(e)}")

# Servir archivos estáticos del frontend
if os.path.exists("build"):
    app.mount("/static", StaticFiles(directory="build/static"), name="static")
    
    @app.get("/{path:path}")
    async def serve_frontend(path: str):
        if path and os.path.exists(f"build/{path}"):
            return StaticFiles(directory="build")(path)
        return HTMLResponse(open("build/index.html").read())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
