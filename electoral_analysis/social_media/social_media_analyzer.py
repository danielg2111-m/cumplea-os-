"""
Analizador Principal de Redes Sociales para Candidatos
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
from .twitter_analyzer import TwitterAnalyzer
from .facebook_analyzer import FacebookAnalyzer
from .sentiment_analyzer import SentimentAnalyzer

class SocialMediaAnalyzer:
    """
    Clase principal para análisis de redes sociales de candidatos electorales
    """
    
    def __init__(self):
        self.twitter_analyzer = TwitterAnalyzer()
        self.facebook_analyzer = FacebookAnalyzer()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.logger = self._setup_logger()
        self.candidates_data = {}
        
    def _setup_logger(self) -> logging.Logger:
        """Configurar logging"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def add_candidate(self, name: str, social_accounts: Dict[str, str]):
        """
        Agregar candidato con sus cuentas de redes sociales
        
        Args:
            name: Nombre del candidato
            social_accounts: Dict con cuentas {'twitter': '@usuario', 'facebook': 'pagina'}
        """
        self.candidates_data[name] = {
            'accounts': social_accounts,
            'metrics': {},
            'sentiment': {},
            'engagement': {},
            'content_analysis': {}
        }
        self.logger.info(f"Candidato agregado: {name}")
    
    def analyze_all_candidates(self, days_back: int = 30) -> Dict:
        """
        Analizar todas las redes sociales de todos los candidatos
        """
        results = {}
        
        for candidate_name in self.candidates_data.keys():
            self.logger.info(f"Analizando candidato: {candidate_name}")
            results[candidate_name] = self.analyze_candidate(candidate_name, days_back)
        
        return results
    
    def analyze_candidate(self, candidate_name: str, days_back: int = 30) -> Dict:
        """
        Analizar redes sociales de un candidato específico
        """
        if candidate_name not in self.candidates_data:
            self.logger.error(f"Candidato {candidate_name} no encontrado")
            return {}
        
        candidate_info = self.candidates_data[candidate_name]
        accounts = candidate_info['accounts']
        
        analysis_results = {
            'twitter_analysis': {},
            'facebook_analysis': {},
            'overall_sentiment': {},
            'engagement_metrics': {},
            'content_themes': {},
            'influence_score': 0
        }
        
        # Análisis de Twitter
        if 'twitter' in accounts:
            twitter_handle = accounts['twitter']
            analysis_results['twitter_analysis'] = self.twitter_analyzer.analyze_account(
                twitter_handle, days_back
            )
        
        # Análisis de Facebook
        if 'facebook' in accounts:
            facebook_page = accounts['facebook']
            analysis_results['facebook_analysis'] = self.facebook_analyzer.analyze_page(
                facebook_page, days_back
            )
        
        # Análisis de sentimiento general
        all_posts = self._collect_all_posts(analysis_results)
        if all_posts:
            analysis_results['overall_sentiment'] = self.sentiment_analyzer.analyze_posts(all_posts)
        
        # Métricas de engagement
        analysis_results['engagement_metrics'] = self._calculate_engagement_metrics(analysis_results)
        
        # Análisis de contenido y temas
        analysis_results['content_themes'] = self._analyze_content_themes(all_posts)
        
        # Calcular score de influencia
        analysis_results['influence_score'] = self._calculate_influence_score(analysis_results)
        
        # Guardar resultados
        self.candidates_data[candidate_name].update(analysis_results)
        
        return analysis_results
    
    def _collect_all_posts(self, analysis_results: Dict) -> List[str]:
        """Recopilar todos los posts de todas las plataformas"""
        all_posts = []
        
        # Posts de Twitter
        if 'twitter_analysis' in analysis_results and 'posts' in analysis_results['twitter_analysis']:
            all_posts.extend(analysis_results['twitter_analysis']['posts'])
        
        # Posts de Facebook
        if 'facebook_analysis' in analysis_results and 'posts' in analysis_results['facebook_analysis']:
            all_posts.extend(analysis_results['facebook_analysis']['posts'])
        
        return all_posts
    
    def _calculate_engagement_metrics(self, analysis_results: Dict) -> Dict:
        """Calcular métricas de engagement combinadas"""
        metrics = {
            'total_followers': 0,
            'total_posts': 0,
            'avg_likes_per_post': 0,
            'avg_shares_per_post': 0,
            'avg_comments_per_post': 0,
            'engagement_rate': 0,
            'posting_frequency': 0
        }
        
        platforms_data = []
        
        # Datos de Twitter
        if 'twitter_analysis' in analysis_results:
            twitter_data = analysis_results['twitter_analysis']
            if 'metrics' in twitter_data:
                platforms_data.append(twitter_data['metrics'])
        
        # Datos de Facebook
        if 'facebook_analysis' in analysis_results:
            facebook_data = analysis_results['facebook_analysis']
            if 'metrics' in facebook_data:
                platforms_data.append(facebook_data['metrics'])
        
        # Calcular métricas combinadas
        if platforms_data:
            metrics['total_followers'] = sum(data.get('followers', 0) for data in platforms_data)
            metrics['total_posts'] = sum(data.get('posts_count', 0) for data in platforms_data)
            
            if metrics['total_posts'] > 0:
                total_likes = sum(data.get('total_likes', 0) for data in platforms_data)
                total_shares = sum(data.get('total_shares', 0) for data in platforms_data)
                total_comments = sum(data.get('total_comments', 0) for data in platforms_data)
                
                metrics['avg_likes_per_post'] = total_likes / metrics['total_posts']
                metrics['avg_shares_per_post'] = total_shares / metrics['total_posts']
                metrics['avg_comments_per_post'] = total_comments / metrics['total_posts']
                
                # Calcular engagement rate
                total_engagement = total_likes + total_shares + total_comments
                if metrics['total_followers'] > 0:
                    metrics['engagement_rate'] = total_engagement / metrics['total_followers']
        
        return metrics
    
    def _analyze_content_themes(self, posts: List[str]) -> Dict:
        """Analizar temas principales en el contenido"""
        if not posts:
            return {}
        
        # Palabras clave por tema político
        themes = {
            'economia': ['economía', 'empleo', 'trabajo', 'empresa', 'negocio', 'dinero', 'precio'],
            'educacion': ['educación', 'escuela', 'universidad', 'estudiante', 'maestro', 'profesor'],
            'salud': ['salud', 'hospital', 'médico', 'medicina', 'enfermedad', 'covid'],
            'seguridad': ['seguridad', 'delincuencia', 'policía', 'crimen', 'violencia'],
            'medio_ambiente': ['ambiente', 'clima', 'contaminación', 'verde', 'sostenible'],
            'infraestructura': ['carretera', 'transporte', 'construcción', 'vivienda', 'agua'],
            'corrupcion': ['corrupción', 'transparencia', 'honestidad', 'ética', 'justicia']
        }
        
        theme_counts = {theme: 0 for theme in themes}
        total_posts = len(posts)
        
        for post in posts:
            post_lower = post.lower()
            for theme, keywords in themes.items():
                if any(keyword in post_lower for keyword in keywords):
                    theme_counts[theme] += 1
        
        # Convertir a porcentajes
        theme_percentages = {
            theme: (count / total_posts) * 100 
            for theme, count in theme_counts.items()
        }
        
        return {
            'temas_principales': theme_percentages,
            'tema_dominante': max(theme_percentages, key=theme_percentages.get),
            'diversidad_tematica': len([t for t in theme_percentages.values() if t > 5])
        }
    
    def _calculate_influence_score(self, analysis_results: Dict) -> float:
        """Calcular score de influencia del candidato (0-100)"""
        score = 0
        
        # Peso por seguidores (30%)
        engagement = analysis_results.get('engagement_metrics', {})
        followers = engagement.get('total_followers', 0)
        if followers > 0:
            # Normalizar logarítmicamente
            score += min(np.log10(followers) * 10, 30)
        
        # Peso por engagement rate (25%)
        engagement_rate = engagement.get('engagement_rate', 0)
        score += min(engagement_rate * 2500, 25)
        
        # Peso por frecuencia de posts (15%)
        posts_count = engagement.get('total_posts', 0)
        score += min(posts_count * 0.5, 15)
        
        # Peso por sentimiento positivo (20%)
        sentiment = analysis_results.get('overall_sentiment', {})
        positive_sentiment = sentiment.get('positive_percentage', 0)
        score += positive_sentiment * 0.2
        
        # Peso por diversidad temática (10%)
        content = analysis_results.get('content_themes', {})
        diversity = content.get('diversidad_tematica', 0)
        score += min(diversity * 2, 10)
        
        return min(score, 100)
    
    def compare_candidates(self) -> Dict:
        """Comparar todos los candidatos analizados"""
        if not self.candidates_data:
            return {}
        
        comparison = {
            'ranking_influencia': [],
            'ranking_engagement': [],
            'ranking_sentimiento': [],
            'comparacion_temas': {},
            'resumen_general': {}
        }
        
        # Ranking por influencia
        influence_scores = []
        for name, data in self.candidates_data.items():
            influence_score = data.get('influence_score', 0)
            influence_scores.append((name, influence_score))
        
        comparison['ranking_influencia'] = sorted(influence_scores, key=lambda x: x[1], reverse=True)
        
        # Ranking por engagement
        engagement_scores = []
        for name, data in self.candidates_data.items():
            engagement = data.get('engagement_metrics', {})
            engagement_rate = engagement.get('engagement_rate', 0)
            engagement_scores.append((name, engagement_rate))
        
        comparison['ranking_engagement'] = sorted(engagement_scores, key=lambda x: x[1], reverse=True)
        
        # Ranking por sentimiento
        sentiment_scores = []
        for name, data in self.candidates_data.items():
            sentiment = data.get('overall_sentiment', {})
            positive_rate = sentiment.get('positive_percentage', 0)
            sentiment_scores.append((name, positive_rate))
        
        comparison['ranking_sentimiento'] = sorted(sentiment_scores, key=lambda x: x[1], reverse=True)
        
        # Comparación de temas
        all_themes = set()
        for name, data in self.candidates_data.items():
            themes = data.get('content_themes', {}).get('temas_principales', {})
            all_themes.update(themes.keys())
        
        for theme in all_themes:
            comparison['comparacion_temas'][theme] = {}
            for name, data in self.candidates_data.items():
                themes = data.get('content_themes', {}).get('temas_principales', {})
                comparison['comparacion_temas'][theme][name] = themes.get(theme, 0)
        
        return comparison
    
    def generate_social_media_report(self, file_path: str = 'social_media_report.txt'):
        """Generar reporte completo de análisis de redes sociales"""
        comparison = self.compare_candidates()
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("REPORTE DE ANÁLISIS DE REDES SOCIALES\n")
            f.write("=" * 50 + "\n\n")
            
            # Ranking de influencia
            f.write("RANKING DE INFLUENCIA\n")
            f.write("-" * 25 + "\n")
            for i, (name, score) in enumerate(comparison['ranking_influencia'], 1):
                f.write(f"{i}. {name}: {score:.1f} puntos\n")
            f.write("\n")
            
            # Ranking de engagement
            f.write("RANKING DE ENGAGEMENT\n")
            f.write("-" * 25 + "\n")
            for i, (name, rate) in enumerate(comparison['ranking_engagement'], 1):
                f.write(f"{i}. {name}: {rate:.3f} tasa de engagement\n")
            f.write("\n")
            
            # Ranking de sentimiento
            f.write("RANKING DE SENTIMIENTO POSITIVO\n")
            f.write("-" * 35 + "\n")
            for i, (name, sentiment) in enumerate(comparison['ranking_sentimiento'], 1):
                f.write(f"{i}. {name}: {sentiment:.1f}% sentimiento positivo\n")
            f.write("\n")
            
            # Análisis detallado por candidato
            f.write("ANÁLISIS DETALLADO POR CANDIDATO\n")
            f.write("=" * 40 + "\n\n")
            
            for name, data in self.candidates_data.items():
                f.write(f"{name.upper()}\n")
                f.write("-" * len(name) + "\n")
                
                # Métricas de engagement
                engagement = data.get('engagement_metrics', {})
                f.write(f"Seguidores totales: {engagement.get('total_followers', 0):,}\n")
                f.write(f"Posts analizados: {engagement.get('total_posts', 0)}\n")
                f.write(f"Promedio likes por post: {engagement.get('avg_likes_per_post', 0):.1f}\n")
                f.write(f"Tasa de engagement: {engagement.get('engagement_rate', 0):.3f}\n")
                
                # Sentimiento
                sentiment = data.get('overall_sentiment', {})
                f.write(f"Sentimiento positivo: {sentiment.get('positive_percentage', 0):.1f}%\n")
                f.write(f"Sentimiento negativo: {sentiment.get('negative_percentage', 0):.1f}%\n")
                
                # Tema dominante
                content = data.get('content_themes', {})
                dominant_theme = content.get('tema_dominante', 'N/A')
                f.write(f"Tema dominante: {dominant_theme}\n")
                
                f.write(f"Score de influencia: {data.get('influence_score', 0):.1f}/100\n")
                f.write("\n")
        
        print(f"Reporte de redes sociales exportado a: {file_path}")
    
    def get_winner_prediction_social_media(self) -> Dict:
        """Predecir ganador basado en análisis de redes sociales"""
        if not self.candidates_data:
            return {}
        
        # Calcular score combinado para cada candidato
        candidate_scores = {}
        
        for name, data in self.candidates_data.items():
            # Factores para la predicción
            influence_score = data.get('influence_score', 0)
            
            engagement = data.get('engagement_metrics', {})
            engagement_rate = engagement.get('engagement_rate', 0)
            followers = engagement.get('total_followers', 0)
            
            sentiment = data.get('overall_sentiment', {})
            positive_sentiment = sentiment.get('positive_percentage', 0)
            
            # Score combinado (ponderado)
            combined_score = (
                influence_score * 0.4 +  # 40% influencia
                min(engagement_rate * 1000, 30) * 0.3 +  # 30% engagement
                positive_sentiment * 0.3  # 30% sentimiento positivo
            )
            
            candidate_scores[name] = {
                'score_combinado': combined_score,
                'factores': {
                    'influencia': influence_score,
                    'engagement': engagement_rate,
                    'sentimiento_positivo': positive_sentiment,
                    'seguidores': followers
                }
            }
        
        # Ordenar por score
        sorted_candidates = sorted(
            candidate_scores.items(), 
            key=lambda x: x[1]['score_combinado'], 
            reverse=True
        )
        
        return {
            'prediccion_ganador': sorted_candidates[0][0] if sorted_candidates else None,
            'ranking_completo': sorted_candidates,
            'metodologia': 'Basado en influencia (40%), engagement (30%) y sentimiento positivo (30%)'
        }
