import pandas as pd
import numpy as np
from typing import Dict, List, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from collections import Counter

class AIInsights:
    def __init__(self):
        self.insight_types = [
            "statistical_anomalies",
            "response_patterns", 
            "demographic_insights",
            "satisfaction_analysis",
            "improvement_opportunities"
        ]
    
    async def generate_insights(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generar insights inteligentes de los datos"""
        insights = {
            "key_findings": [],
            "statistical_insights": [],
            "behavioral_patterns": [],
            "recommendations": [],
            "risk_factors": [],
            "opportunities": []
        }
        
        # Análisis estadístico automático
        insights["statistical_insights"] = self.analyze_statistical_patterns(df)
        
        # Patrones de comportamiento
        insights["behavioral_patterns"] = self.detect_behavioral_patterns(df)
        
        # Hallazgos clave
        insights["key_findings"] = self.extract_key_findings(df)
        
        # Factores de riesgo
        insights["risk_factors"] = self.identify_risk_factors(df)
        
        # Oportunidades de mejora
        insights["opportunities"] = self.identify_opportunities(df)
        
        return insights
    
    def analyze_statistical_patterns(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Analizar patrones estadísticos automáticamente"""
        patterns = []
        
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        for column in numeric_columns:
            data = df[column].dropna()
            if len(data) < 5:
                continue
                
            mean_val = data.mean()
            std_val = data.std()
            median_val = data.median()
            
            # Detectar distribución sesgada
            skewness = data.skew()
            if abs(skewness) > 1:
                direction = "positivamente" if skewness > 0 else "negativamente"
                patterns.append({
                    "type": "distribución_sesgada",
                    "column": column,
                    "description": f"Los datos de '{column}' están {direction} sesgados",
                    "value": float(skewness),
                    "impact": "alto" if abs(skewness) > 2 else "medio"
                })
            
            # Detectar outliers significativos
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            outliers = data[(data < Q1 - 1.5*IQR) | (data > Q3 + 1.5*IQR)]
            
            if len(outliers) > len(data) * 0.1:  # Más del 10% son outliers
                patterns.append({
                    "type": "outliers_significativos",
                    "column": column,
                    "description": f"'{column}' tiene {len(outliers)} valores atípicos ({len(outliers)/len(data)*100:.1f}%)",
                    "value": len(outliers),
                    "impact": "alto"
                })
            
            # Detectar bimodalidad
            hist, bins = np.histogram(data, bins=20)
            peaks = self.find_peaks(hist)
            if len(peaks) >= 2:
                patterns.append({
                    "type": "distribución_bimodal",
                    "column": column,
                    "description": f"'{column}' muestra una distribución bimodal con múltiples picos",
                    "value": len(peaks),
                    "impact": "medio"
                })
        
        return patterns
    
    def detect_behavioral_patterns(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Detectar patrones de comportamiento en las respuestas"""
        patterns = []
        
        # Patrones de respuesta por columna
        for column in df.columns:
            if df[column].dtype in ['object', 'category']:
                value_counts = df[column].value_counts()
                total_responses = len(df[column].dropna())
                
                if total_responses == 0:
                    continue
                
                # Detectar respuestas dominantes
                if len(value_counts) > 0:
                    dominant_response = value_counts.index[0]
                    dominant_percentage = (value_counts.iloc[0] / total_responses) * 100
                    
                    if dominant_percentage > 70:
                        patterns.append({
                            "type": "respuesta_dominante",
                            "column": column,
                            "description": f"'{dominant_response}' domina las respuestas en '{column}' ({dominant_percentage:.1f}%)",
                            "value": dominant_percentage,
                            "impact": "alto"
                        })
                    
                    # Detectar diversidad de respuestas
                    diversity_score = len(value_counts) / total_responses
                    if diversity_score > 0.8:
                        patterns.append({
                            "type": "alta_diversidad",
                            "column": column,
                            "description": f"'{column}' muestra alta diversidad en las respuestas",
                            "value": diversity_score,
                            "impact": "medio"
                        })
        
        # Patrones de correlación entre respuestas
        numeric_df = df.select_dtypes(include=[np.number])
        if len(numeric_df.columns) >= 2:
            corr_matrix = numeric_df.corr()
            
            # Buscar correlaciones fuertes
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_value = corr_matrix.iloc[i, j]
                    if abs(corr_value) > 0.7:
                        col1, col2 = corr_matrix.columns[i], corr_matrix.columns[j]
                        relationship = "positiva" if corr_value > 0 else "negativa"
                        patterns.append({
                            "type": "correlación_fuerte",
                            "columns": [col1, col2],
                            "description": f"Correlación {relationship} fuerte entre '{col1}' y '{col2}'",
                            "value": float(corr_value),
                            "impact": "alto"
                        })
        
        return patterns
    
    def extract_key_findings(self, df: pd.DataFrame) -> List[str]:
        """Extraer hallazgos clave automáticamente"""
        findings = []
        
        # Información básica
        total_responses = len(df)
        total_questions = len(df.columns)
        completion_rate = (df.notna().sum().sum() / (total_responses * total_questions)) * 100
        
        findings.append(f"Se analizaron {total_responses} respuestas de {total_questions} preguntas")
        findings.append(f"Tasa de completitud: {completion_rate:.1f}%")
        
        # Análisis de columnas numéricas
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        if len(numeric_columns) > 0:
            for column in numeric_columns:
                data = df[column].dropna()
                if len(data) > 0:
                    mean_val = data.mean()
                    std_val = data.std()
                    
                    # Hallazgos basados en distribución
                    cv = (std_val / mean_val) * 100 if mean_val != 0 else 0
                    if cv > 50:
                        findings.append(f"'{column}' muestra alta variabilidad (CV: {cv:.1f}%)")
                    elif cv < 10:
                        findings.append(f"'{column}' muestra respuestas muy consistentes (CV: {cv:.1f}%)")
        
        # Análisis de columnas categóricas
        categorical_columns = df.select_dtypes(include=['object', 'category']).columns
        for column in categorical_columns:
            value_counts = df[column].value_counts()
            if len(value_counts) > 0:
                top_response = value_counts.index[0]
                top_percentage = (value_counts.iloc[0] / len(df[column].dropna())) * 100
                
                if top_percentage > 50:
                    findings.append(f"La mayoría ({top_percentage:.1f}%) respondió '{top_response}' en '{column}'")
        
        return findings[:10]  # Limitar a 10 hallazgos principales
    
    def identify_risk_factors(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Identificar factores de riesgo en los datos"""
        risk_factors = []
        
        # Riesgo por datos faltantes
        missing_data = df.isnull().sum()
        for column, missing_count in missing_data.items():
            missing_percentage = (missing_count / len(df)) * 100
            if missing_percentage > 30:
                risk_factors.append({
                    "type": "datos_faltantes",
                    "column": column,
                    "description": f"Alto porcentaje de datos faltantes en '{column}' ({missing_percentage:.1f}%)",
                    "severity": "alto" if missing_percentage > 50 else "medio",
                    "recommendation": f"Considerar estrategias de imputación o recolección adicional para '{column}'"
                })
        
        # Riesgo por baja participación
        response_rate = len(df) / (len(df) + df.isnull().sum().sum()) if df.isnull().sum().sum() > 0 else 1
        if response_rate < 0.7:
            risk_factors.append({
                "type": "baja_participación",
                "description": f"Tasa de respuesta baja ({response_rate*100:.1f}%)",
                "severity": "alto",
                "recommendation": "Revisar metodología de recolección y incentivos para participación"
            })
        
        # Riesgo por sesgos en respuestas
        for column in df.select_dtypes(include=['object', 'category']).columns:
            value_counts = df[column].value_counts()
            if len(value_counts) > 0:
                top_percentage = (value_counts.iloc[0] / len(df[column].dropna())) * 100
                if top_percentage > 80:
                    risk_factors.append({
                        "type": "sesgo_respuesta",
                        "column": column,
                        "description": f"Posible sesgo en '{column}' - una respuesta domina ({top_percentage:.1f}%)",
                        "severity": "medio",
                        "recommendation": f"Revisar formulación de la pregunta '{column}' para evitar sesgos"
                    })
        
        return risk_factors
    
    def identify_opportunities(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Identificar oportunidades de mejora"""
        opportunities = []
        
        # Oportunidades basadas en correlaciones
        numeric_df = df.select_dtypes(include=[np.number])
        if len(numeric_df.columns) >= 2:
            corr_matrix = numeric_df.corr()
            
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_value = corr_matrix.iloc[i, j]
                    if 0.3 <= abs(corr_value) <= 0.7:  # Correlación moderada
                        col1, col2 = corr_matrix.columns[i], corr_matrix.columns[j]
                        opportunities.append({
                            "type": "análisis_relacional",
                            "columns": [col1, col2],
                            "description": f"Explorar relación entre '{col1}' y '{col2}' (r={corr_value:.2f})",
                            "potential": "medio",
                            "action": f"Análisis más profundo de la relación {col1}-{col2}"
                        })
        
        # Oportunidades de segmentación
        categorical_columns = df.select_dtypes(include=['object', 'category']).columns
        for column in categorical_columns:
            unique_values = df[column].nunique()
            total_values = len(df[column].dropna())
            
            if 3 <= unique_values <= 10 and total_values > 20:
                opportunities.append({
                    "type": "segmentación",
                    "column": column,
                    "description": f"'{column}' es ideal para análisis de segmentación ({unique_values} categorías)",
                    "potential": "alto",
                    "action": f"Realizar análisis comparativo por grupos de '{column}'"
                })
        
        # Oportunidades de análisis temporal
        date_columns = df.select_dtypes(include=['datetime64']).columns
        if len(date_columns) > 0:
            opportunities.append({
                "type": "análisis_temporal",
                "description": "Los datos incluyen información temporal para análisis de tendencias",
                "potential": "alto",
                "action": "Implementar análisis de series temporales y tendencias"
            })
        
        return opportunities
    
    def generate_recommendations(self, insights: Dict[str, Any]) -> List[str]:
        """Generar recomendaciones basadas en insights"""
        recommendations = []
        
        # Recomendaciones basadas en patrones estadísticos
        statistical_insights = insights.get("statistical_insights", [])
        for insight in statistical_insights:
            if insight["type"] == "distribución_sesgada":
                recommendations.append(
                    f"Considerar transformación de datos para '{insight['column']}' debido a sesgo estadístico"
                )
            elif insight["type"] == "outliers_significativos":
                recommendations.append(
                    f"Investigar y validar valores atípicos en '{insight['column']}'"
                )
        
        # Recomendaciones basadas en factores de riesgo
        risk_factors = insights.get("risk_factors", [])
        for risk in risk_factors:
            if "recommendation" in risk:
                recommendations.append(risk["recommendation"])
        
        # Recomendaciones basadas en oportunidades
        opportunities = insights.get("opportunities", [])
        for opportunity in opportunities:
            if "action" in opportunity:
                recommendations.append(opportunity["action"])
        
        # Recomendaciones generales
        recommendations.extend([
            "Implementar validación cruzada de resultados con muestras adicionales",
            "Considerar análisis de segmentación para insights más específicos",
            "Desarrollar dashboard interactivo para monitoreo continuo"
        ])
        
        return recommendations[:8]  # Limitar a 8 recomendaciones principales
    
    def find_peaks(self, data: np.ndarray) -> List[int]:
        """Encontrar picos en un histograma"""
        peaks = []
        for i in range(1, len(data) - 1):
            if data[i] > data[i-1] and data[i] > data[i+1] and data[i] > np.mean(data):
                peaks.append(i)
        return peaks
    
    def calculate_insight_confidence(self, insight_data: Dict[str, Any]) -> float:
        """Calcular confianza en un insight"""
        # Factores que afectan la confianza
        sample_size_factor = min(1.0, len(insight_data.get("data", [])) / 100)
        completeness_factor = 1.0 - (insight_data.get("missing_percentage", 0) / 100)
        statistical_significance = insight_data.get("p_value", 0.5)
        
        confidence = (sample_size_factor * 0.4 + 
                     completeness_factor * 0.3 + 
                     (1 - statistical_significance) * 0.3)
        
        return min(1.0, max(0.0, confidence))
    
    def prioritize_insights(self, insights: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Priorizar insights por importancia"""
        for insight in insights:
            # Calcular puntuación de prioridad
            impact_score = {"alto": 3, "medio": 2, "bajo": 1}.get(insight.get("impact", "bajo"), 1)
            confidence_score = self.calculate_insight_confidence(insight)
            
            insight["priority_score"] = impact_score * confidence_score
        
        return sorted(insights, key=lambda x: x.get("priority_score", 0), reverse=True)
