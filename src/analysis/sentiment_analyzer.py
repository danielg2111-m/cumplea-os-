import nltk
from textblob import TextBlob
import pandas as pd
import numpy as np
from typing import List, Dict, Any
import asyncio
from transformers import pipeline
import re

class SentimentAnalyzer:
    def __init__(self):
        self.sentiment_pipeline = None
        self.initialized = False
    
    async def initialize(self):
        """Inicializar modelos de análisis de sentimientos"""
        try:
            # Descargar recursos de NLTK si es necesario
            nltk.download('punkt', quiet=True)
            nltk.download('vader_lexicon', quiet=True)
            
            # Inicializar pipeline de transformers
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model="nlptown/bert-base-multilingual-uncased-sentiment",
                return_all_scores=True
            )
            
            self.initialized = True
            print("✅ Analizador de sentimientos inicializado")
            
        except Exception as e:
            print(f"⚠️ Error inicializando analizador: {e}")
            # Usar TextBlob como fallback
            self.initialized = True
    
    def clean_text(self, text: str) -> str:
        """Limpiar y preprocesar texto"""
        if pd.isna(text) or not isinstance(text, str):
            return ""
        
        # Remover caracteres especiales y normalizar
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip().lower()
    
    def analyze_text_sentiment(self, text: str) -> Dict[str, Any]:
        """Analizar sentimiento de un texto individual"""
        if not text or pd.isna(text):
            return {
                "sentiment": "neutral",
                "polarity": 0.0,
                "subjectivity": 0.0,
                "confidence": 0.0
            }
        
        cleaned_text = self.clean_text(text)
        
        try:
            # Usar modelo de transformers si está disponible
            if self.sentiment_pipeline:
                results = self.sentiment_pipeline(cleaned_text[:512])  # Limitar longitud
                
                # Procesar resultados
                sentiment_scores = {item['label']: item['score'] for item in results[0]}
                
                # Determinar sentimiento principal
                main_sentiment = max(sentiment_scores, key=sentiment_scores.get)
                confidence = max(sentiment_scores.values())
                
                # Mapear a polaridad
                polarity_map = {
                    'POSITIVE': 1.0,
                    'NEGATIVE': -1.0,
                    'NEUTRAL': 0.0,
                    '5 stars': 1.0,
                    '4 stars': 0.5,
                    '3 stars': 0.0,
                    '2 stars': -0.5,
                    '1 star': -1.0
                }
                
                polarity = polarity_map.get(main_sentiment, 0.0)
                
            else:
                # Fallback a TextBlob
                blob = TextBlob(cleaned_text)
                polarity = blob.sentiment.polarity
                subjectivity = blob.sentiment.subjectivity
                
                if polarity > 0.1:
                    main_sentiment = "positive"
                elif polarity < -0.1:
                    main_sentiment = "negative"
                else:
                    main_sentiment = "neutral"
                
                confidence = abs(polarity)
            
            return {
                "sentiment": main_sentiment.lower(),
                "polarity": polarity,
                "subjectivity": subjectivity if 'subjectivity' in locals() else 0.5,
                "confidence": confidence,
                "raw_scores": sentiment_scores if 'sentiment_scores' in locals() else {}
            }
            
        except Exception as e:
            print(f"Error analizando sentimiento: {e}")
            return {
                "sentiment": "neutral",
                "polarity": 0.0,
                "subjectivity": 0.0,
                "confidence": 0.0
            }
    
    async def analyze_survey_sentiment(self, df: pd.DataFrame, text_columns: List[str]) -> Dict[str, Any]:
        """Analizar sentimientos de toda la encuesta"""
        results = {
            "overall_sentiment": {},
            "column_analysis": {},
            "sentiment_distribution": {},
            "key_insights": []
        }
        
        all_sentiments = []
        all_polarities = []
        
        for column in text_columns:
            column_sentiments = []
            column_polarities = []
            
            # Analizar cada respuesta en la columna
            for text in df[column].dropna():
                sentiment_result = self.analyze_text_sentiment(str(text))
                column_sentiments.append(sentiment_result['sentiment'])
                column_polarities.append(sentiment_result['polarity'])
                
                all_sentiments.append(sentiment_result['sentiment'])
                all_polarities.append(sentiment_result['polarity'])
            
            # Estadísticas por columna
            if column_sentiments:
                sentiment_counts = pd.Series(column_sentiments).value_counts()
                avg_polarity = np.mean(column_polarities)
                
                results["column_analysis"][column] = {
                    "sentiment_distribution": sentiment_counts.to_dict(),
                    "average_polarity": avg_polarity,
                    "total_responses": len(column_sentiments),
                    "dominant_sentiment": sentiment_counts.index[0] if len(sentiment_counts) > 0 else "neutral"
                }
        
        # Análisis general
        if all_sentiments:
            overall_counts = pd.Series(all_sentiments).value_counts()
            overall_polarity = np.mean(all_polarities)
            
            results["overall_sentiment"] = {
                "distribution": overall_counts.to_dict(),
                "average_polarity": overall_polarity,
                "dominant_sentiment": overall_counts.index[0],
                "total_analyzed": len(all_sentiments)
            }
            
            # Generar insights
            results["key_insights"] = self.generate_sentiment_insights(results)
        
        return results
    
    def generate_sentiment_insights(self, sentiment_results: Dict[str, Any]) -> List[str]:
        """Generar insights clave del análisis de sentimientos"""
        insights = []
        
        overall = sentiment_results.get("overall_sentiment", {})
        if not overall:
            return insights
        
        # Insight sobre sentimiento dominante
        dominant = overall.get("dominant_sentiment", "neutral")
        polarity = overall.get("average_polarity", 0)
        
        if dominant == "positive":
            insights.append(f"La encuesta muestra un sentimiento general positivo (polaridad: {polarity:.2f})")
        elif dominant == "negative":
            insights.append(f"La encuesta revela un sentimiento general negativo (polaridad: {polarity:.2f})")
        else:
            insights.append(f"La encuesta presenta un sentimiento neutral (polaridad: {polarity:.2f})")
        
        # Insights por columnas
        column_analysis = sentiment_results.get("column_analysis", {})
        for column, data in column_analysis.items():
            col_dominant = data.get("dominant_sentiment", "neutral")
            col_polarity = data.get("average_polarity", 0)
            
            if abs(col_polarity) > 0.3:  # Sentimiento fuerte
                sentiment_desc = "muy positivo" if col_polarity > 0.3 else "muy negativo"
                insights.append(f"La pregunta '{column}' genera respuestas {sentiment_desc}")
        
        return insights
    
    def get_emotion_keywords(self, df: pd.DataFrame, text_columns: List[str]) -> Dict[str, List[str]]:
        """Extraer palabras clave emocionales"""
        emotion_keywords = {
            "positive": [],
            "negative": [],
            "neutral": []
        }
        
        positive_words = ['excelente', 'bueno', 'genial', 'perfecto', 'satisfecho', 'feliz', 'amor', 'increíble']
        negative_words = ['malo', 'terrible', 'horrible', 'odio', 'frustrado', 'enojado', 'triste', 'decepcionado']
        
        for column in text_columns:
            for text in df[column].dropna():
                text_lower = str(text).lower()
                
                for word in positive_words:
                    if word in text_lower:
                        emotion_keywords["positive"].append(word)
                
                for word in negative_words:
                    if word in text_lower:
                        emotion_keywords["negative"].append(word)
        
        # Contar frecuencias
        for sentiment in emotion_keywords:
            word_counts = pd.Series(emotion_keywords[sentiment]).value_counts()
            emotion_keywords[sentiment] = word_counts.head(10).to_dict()
        
        return emotion_keywords
