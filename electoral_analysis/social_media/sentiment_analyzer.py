"""
Analizador de Sentimiento para Contenido Electoral
"""

from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np
from typing import Dict, List
import re

class SentimentAnalyzer:
    """
    Clase para análisis de sentimiento en contenido de redes sociales
    """
    
    def __init__(self):
        self.vader_analyzer = SentimentIntensityAnalyzer()
        
    def analyze_posts(self, posts: List[str]) -> Dict:
        """
        Analizar sentimiento de una lista de posts
        """
        if not posts:
            return {}
        
        sentiment_results = []
        
        for post in posts:
            # Limpiar texto
            cleaned_post = self._clean_text(post)
            
            # Análisis con TextBlob
            blob = TextBlob(cleaned_post)
            textblob_sentiment = blob.sentiment
            
            # Análisis con VADER
            vader_scores = self.vader_analyzer.polarity_scores(cleaned_post)
            
            # Combinar resultados
            sentiment_results.append({
                'text': post,
                'textblob_polarity': textblob_sentiment.polarity,
                'textblob_subjectivity': textblob_sentiment.subjectivity,
                'vader_positive': vader_scores['pos'],
                'vader_negative': vader_scores['neg'],
                'vader_neutral': vader_scores['neu'],
                'vader_compound': vader_scores['compound']
            })
        
        # Calcular estadísticas generales
        return self._calculate_overall_sentiment(sentiment_results)
    
    def _clean_text(self, text: str) -> str:
        """Limpiar texto para análisis de sentimiento"""
        # Remover URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remover menciones y hashtags para el análisis de sentimiento
        text = re.sub(r'@\w+|#\w+', '', text)
        
        # Remover caracteres especiales excepto puntuación básica
        text = re.sub(r'[^\w\s.,!?]', '', text)
        
        # Remover espacios extra
        text = ' '.join(text.split())
        
        return text.strip()
    
    def _calculate_overall_sentiment(self, sentiment_results: List[Dict]) -> Dict:
        """Calcular estadísticas generales de sentimiento"""
        if not sentiment_results:
            return {}
        
        # Extraer scores
        textblob_polarities = [r['textblob_polarity'] for r in sentiment_results]
        vader_compounds = [r['vader_compound'] for r in sentiment_results]
        
        # Clasificar sentimientos usando VADER compound score
        positive_count = sum(1 for score in vader_compounds if score >= 0.05)
        negative_count = sum(1 for score in vader_compounds if score <= -0.05)
        neutral_count = len(vader_compounds) - positive_count - negative_count
        
        total_posts = len(sentiment_results)
        
        # Calcular porcentajes
        positive_percentage = (positive_count / total_posts) * 100
        negative_percentage = (negative_count / total_posts) * 100
        neutral_percentage = (neutral_count / total_posts) * 100
        
        # Encontrar posts más positivos y negativos
        most_positive = max(sentiment_results, key=lambda x: x['vader_compound'])
        most_negative = min(sentiment_results, key=lambda x: x['vader_compound'])
        
        return {
            'total_posts_analyzed': total_posts,
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count': neutral_count,
            'positive_percentage': positive_percentage,
            'negative_percentage': negative_percentage,
            'neutral_percentage': neutral_percentage,
            'average_sentiment_textblob': np.mean(textblob_polarities),
            'average_sentiment_vader': np.mean(vader_compounds),
            'sentiment_std_deviation': np.std(vader_compounds),
            'most_positive_post': {
                'text': most_positive['text'][:100] + '...' if len(most_positive['text']) > 100 else most_positive['text'],
                'score': most_positive['vader_compound']
            },
            'most_negative_post': {
                'text': most_negative['text'][:100] + '...' if len(most_negative['text']) > 100 else most_negative['text'],
                'score': most_negative['vader_compound']
            },
            'detailed_results': sentiment_results
        }
    
    def analyze_sentiment_by_topic(self, posts: List[str], topics: Dict[str, List[str]]) -> Dict:
        """
        Analizar sentimiento por temas específicos
        """
        topic_sentiments = {}
        
        for topic, keywords in topics.items():
            topic_posts = []
            
            # Filtrar posts que contienen palabras clave del tema
            for post in posts:
                post_lower = post.lower()
                if any(keyword.lower() in post_lower for keyword in keywords):
                    topic_posts.append(post)
            
            # Analizar sentimiento del tema
            if topic_posts:
                topic_sentiments[topic] = self.analyze_posts(topic_posts)
            else:
                topic_sentiments[topic] = {
                    'total_posts_analyzed': 0,
                    'positive_percentage': 0,
                    'negative_percentage': 0,
                    'neutral_percentage': 0,
                    'average_sentiment_vader': 0
                }
        
        return topic_sentiments
    
    def get_sentiment_trends(self, posts_with_dates: List[Dict]) -> Dict:
        """
        Analizar tendencias de sentimiento a lo largo del tiempo
        """
        if not posts_with_dates:
            return {}
        
        # Ordenar por fecha
        sorted_posts = sorted(posts_with_dates, key=lambda x: x['created_at'])
        
        # Analizar sentimiento de cada post
        sentiment_timeline = []
        
        for post_data in sorted_posts:
            cleaned_text = self._clean_text(post_data['text'])
            vader_score = self.vader_analyzer.polarity_scores(cleaned_text)
            
            sentiment_timeline.append({
                'date': post_data['created_at'].date(),
                'sentiment_score': vader_score['compound'],
                'text': post_data['text'][:50] + '...' if len(post_data['text']) > 50 else post_data['text']
            })
        
        # Calcular promedios por día
        daily_sentiments = {}
        for entry in sentiment_timeline:
            date = entry['date']
            if date not in daily_sentiments:
                daily_sentiments[date] = []
            daily_sentiments[date].append(entry['sentiment_score'])
        
        # Calcular promedio diario
        daily_averages = {
            date: np.mean(scores) 
            for date, scores in daily_sentiments.items()
        }
        
        return {
            'sentiment_timeline': sentiment_timeline,
            'daily_averages': daily_averages,
            'trend_direction': self._calculate_trend_direction(list(daily_averages.values())),
            'most_positive_day': max(daily_averages, key=daily_averages.get) if daily_averages else None,
            'most_negative_day': min(daily_averages, key=daily_averages.get) if daily_averages else None
        }
    
    def _calculate_trend_direction(self, sentiment_scores: List[float]) -> str:
        """Calcular dirección de la tendencia de sentimiento"""
        if len(sentiment_scores) < 2:
            return "Insuficientes datos"
        
        # Calcular correlación con el tiempo
        x = list(range(len(sentiment_scores)))
        correlation = np.corrcoef(x, sentiment_scores)[0, 1]
        
        if correlation > 0.1:
            return "Mejorando"
        elif correlation < -0.1:
            return "Empeorando"
        else:
            return "Estable"
    
    def compare_candidate_sentiments(self, candidates_posts: Dict[str, List[str]]) -> Dict:
        """
        Comparar sentimiento entre múltiples candidatos
        """
        comparison = {}
        
        for candidate, posts in candidates_posts.items():
            sentiment_analysis = self.analyze_posts(posts)
            comparison[candidate] = {
                'positive_percentage': sentiment_analysis.get('positive_percentage', 0),
                'negative_percentage': sentiment_analysis.get('negative_percentage', 0),
                'average_sentiment': sentiment_analysis.get('average_sentiment_vader', 0),
                'total_posts': sentiment_analysis.get('total_posts_analyzed', 0)
            }
        
        # Ranking por sentimiento positivo
        positive_ranking = sorted(
            comparison.items(),
            key=lambda x: x[1]['positive_percentage'],
            reverse=True
        )
        
        return {
            'individual_analysis': comparison,
            'positive_sentiment_ranking': positive_ranking,
            'best_sentiment_candidate': positive_ranking[0][0] if positive_ranking else None,
            'worst_sentiment_candidate': positive_ranking[-1][0] if positive_ranking else None
        }
