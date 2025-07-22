"""
Analizador de Twitter para Candidatos
"""

import tweepy
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os
import re

class TwitterAnalyzer:
    """
    Clase para analizar cuentas de Twitter de candidatos
    """
    
    def __init__(self):
        self.api = self._setup_twitter_api()
        self.rate_limit_delay = 1  # segundos entre requests
    
    def _setup_twitter_api(self):
        """Configurar API de Twitter"""
        try:
            # Intentar configurar con credenciales reales
            api_key = os.getenv('TWITTER_API_KEY')
            api_secret = os.getenv('TWITTER_API_SECRET')
            access_token = os.getenv('TWITTER_ACCESS_TOKEN')
            access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
            bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
            
            if all([api_key, api_secret, access_token, access_token_secret]):
                auth = tweepy.OAuthHandler(api_key, api_secret)
                auth.set_access_token(access_token, access_token_secret)
                api = tweepy.API(auth, wait_on_rate_limit=True)
                
                # Verificar credenciales
                api.verify_credentials()
                return api
            else:
                print("Credenciales de Twitter no configuradas. Usando datos simulados.")
                return None
                
        except Exception as e:
            print(f"Error configurando Twitter API: {e}")
            return None
    
    def analyze_account(self, username: str, days_back: int = 30) -> Dict:
        """
        Analizar cuenta de Twitter de un candidato
        """
        if self.api:
            return self._analyze_real_account(username, days_back)
        else:
            return self._generate_simulated_data(username, days_back)
    
    def _analyze_real_account(self, username: str, days_back: int) -> Dict:
        """Analizar cuenta real usando Twitter API"""
        try:
            # Remover @ si está presente
            username = username.replace('@', '')
            
            # Obtener información del usuario
            user = self.api.get_user(screen_name=username)
            
            # Obtener tweets recientes
            tweets = []
            for tweet in tweepy.Cursor(
                self.api.user_timeline,
                screen_name=username,
                tweet_mode='extended',
                include_rts=False,
                exclude_replies=True
            ).items(200):  # Máximo 200 tweets
                
                # Filtrar por fecha
                if tweet.created_at > datetime.now() - timedelta(days=days_back):
                    tweets.append(tweet)
            
            # Procesar tweets
            posts_data = []
            total_likes = 0
            total_retweets = 0
            total_replies = 0
            
            for tweet in tweets:
                post_data = {
                    'text': tweet.full_text,
                    'created_at': tweet.created_at,
                    'likes': tweet.favorite_count,
                    'retweets': tweet.retweet_count,
                    'replies': tweet.reply_count if hasattr(tweet, 'reply_count') else 0
                }
                posts_data.append(post_data)
                
                total_likes += tweet.favorite_count
                total_retweets += tweet.retweet_count
                total_replies += post_data['replies']
            
            # Compilar métricas
            metrics = {
                'followers': user.followers_count,
                'following': user.friends_count,
                'posts_count': len(posts_data),
                'total_likes': total_likes,
                'total_shares': total_retweets,
                'total_comments': total_replies,
                'account_age_days': (datetime.now() - user.created_at).days,
                'verified': user.verified
            }
            
            return {
                'metrics': metrics,
                'posts': [post['text'] for post in posts_data],
                'posts_data': posts_data,
                'user_info': {
                    'name': user.name,
                    'description': user.description,
                    'location': user.location,
                    'verified': user.verified
                }
            }
            
        except Exception as e:
            print(f"Error analizando cuenta de Twitter {username}: {e}")
            return self._generate_simulated_data(username, days_back)
    
    def _generate_simulated_data(self, username: str, days_back: int) -> Dict:
        """Generar datos simulados para demostración"""
        np.random.seed(hash(username) % 2**32)  # Seed basado en username para consistencia
        
        # Generar métricas simuladas
        base_followers = np.random.randint(1000, 100000)
        posts_count = np.random.randint(10, 50)
        
        # Generar posts simulados
        sample_posts = [
            "Trabajaremos juntos por un futuro mejor para nuestro país. #Elecciones2024",
            "La educación es la base del desarrollo. Invertiremos en nuestros jóvenes.",
            "Propuestas concretas para mejorar la economía y generar empleo.",
            "Escuchando a los ciudadanos en nuestro recorrido por la región.",
            "Transparencia y honestidad serán pilares de nuestro gobierno.",
            "La salud pública es una prioridad. Fortaleceremos el sistema sanitario.",
            "Unidos podemos lograr el cambio que necesitamos. #VotaConsciente",
            "Defendemos los derechos de todos los ciudadanos sin excepción.",
            "Infraestructura moderna para conectar a todas las comunidades.",
            "El medio ambiente es responsabilidad de todos. Políticas verdes ya."
        ]
        
        posts = np.random.choice(sample_posts, posts_count, replace=True).tolist()
        
        # Generar datos de engagement
        posts_data = []
        total_likes = 0
        total_retweets = 0
        total_replies = 0
        
        for i, post in enumerate(posts):
            likes = np.random.poisson(base_followers * 0.02)  # 2% engagement promedio
            retweets = np.random.poisson(likes * 0.1)
            replies = np.random.poisson(likes * 0.05)
            
            post_data = {
                'text': post,
                'created_at': datetime.now() - timedelta(days=np.random.randint(0, days_back)),
                'likes': likes,
                'retweets': retweets,
                'replies': replies
            }
            posts_data.append(post_data)
            
            total_likes += likes
            total_retweets += retweets
            total_replies += replies
        
        metrics = {
            'followers': base_followers,
            'following': np.random.randint(100, 5000),
            'posts_count': posts_count,
            'total_likes': total_likes,
            'total_shares': total_retweets,
            'total_comments': total_replies,
            'account_age_days': np.random.randint(365, 2000),
            'verified': np.random.choice([True, False], p=[0.7, 0.3])  # 70% verificados
        }
        
        return {
            'metrics': metrics,
            'posts': posts,
            'posts_data': posts_data,
            'user_info': {
                'name': username.replace('@', '').title(),
                'description': f"Candidato/a presidencial comprometido/a con el cambio",
                'location': "País",
                'verified': metrics['verified']
            }
        }
    
    def analyze_hashtags(self, posts: List[str]) -> Dict:
        """Analizar hashtags más utilizados"""
        hashtag_pattern = r'#\w+'
        hashtags = []
        
        for post in posts:
            found_hashtags = re.findall(hashtag_pattern, post.lower())
            hashtags.extend(found_hashtags)
        
        # Contar frecuencia
        hashtag_counts = {}
        for hashtag in hashtags:
            hashtag_counts[hashtag] = hashtag_counts.get(hashtag, 0) + 1
        
        # Ordenar por frecuencia
        sorted_hashtags = sorted(hashtag_counts.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'total_hashtags': len(hashtags),
            'unique_hashtags': len(hashtag_counts),
            'top_hashtags': sorted_hashtags[:10],
            'hashtag_frequency': hashtag_counts
        }
    
    def analyze_mentions(self, posts: List[str]) -> Dict:
        """Analizar menciones (@usuario) en los posts"""
        mention_pattern = r'@\w+'
        mentions = []
        
        for post in posts:
            found_mentions = re.findall(mention_pattern, post.lower())
            mentions.extend(found_mentions)
        
        # Contar frecuencia
        mention_counts = {}
        for mention in mentions:
            mention_counts[mention] = mention_counts.get(mention, 0) + 1
        
        # Ordenar por frecuencia
        sorted_mentions = sorted(mention_counts.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'total_mentions': len(mentions),
            'unique_mentions': len(mention_counts),
            'top_mentions': sorted_mentions[:10],
            'mention_frequency': mention_counts
        }
    
    def calculate_posting_patterns(self, posts_data: List[Dict]) -> Dict:
        """Analizar patrones de publicación"""
        if not posts_data:
            return {}
        
        # Extraer horas y días de la semana
        hours = []
        weekdays = []
        
        for post in posts_data:
            created_at = post['created_at']
            hours.append(created_at.hour)
            weekdays.append(created_at.weekday())  # 0=Lunes, 6=Domingo
        
        # Calcular distribuciones
        hour_distribution = {}
        for hour in range(24):
            hour_distribution[hour] = hours.count(hour)
        
        weekday_names = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        weekday_distribution = {}
        for i, day_name in enumerate(weekday_names):
            weekday_distribution[day_name] = weekdays.count(i)
        
        # Encontrar picos de actividad
        peak_hour = max(hour_distribution, key=hour_distribution.get)
        peak_day = max(weekday_distribution, key=weekday_distribution.get)
        
        return {
            'posts_per_hour': hour_distribution,
            'posts_per_weekday': weekday_distribution,
            'peak_posting_hour': peak_hour,
            'peak_posting_day': peak_day,
            'total_posts_analyzed': len(posts_data)
        }
    
    def get_engagement_trends(self, posts_data: List[Dict]) -> Dict:
        """Analizar tendencias de engagement a lo largo del tiempo"""
        if not posts_data:
            return {}
        
        # Ordenar posts por fecha
        sorted_posts = sorted(posts_data, key=lambda x: x['created_at'])
        
        # Calcular engagement por post
        engagement_data = []
        for post in sorted_posts:
            total_engagement = post['likes'] + post['retweets'] + post['replies']
            engagement_data.append({
                'date': post['created_at'].date(),
                'engagement': total_engagement,
                'likes': post['likes'],
                'retweets': post['retweets'],
                'replies': post['replies']
            })
        
        # Calcular promedios
        if engagement_data:
            avg_engagement = np.mean([e['engagement'] for e in engagement_data])
            avg_likes = np.mean([e['likes'] for e in engagement_data])
            avg_retweets = np.mean([e['retweets'] for e in engagement_data])
            avg_replies = np.mean([e['replies'] for e in engagement_data])
            
            # Encontrar el post con mayor engagement
            best_post = max(engagement_data, key=lambda x: x['engagement'])
        else:
            avg_engagement = avg_likes = avg_retweets = avg_replies = 0
            best_post = {}
        
        return {
            'engagement_timeline': engagement_data,
            'average_engagement': avg_engagement,
            'average_likes': avg_likes,
            'average_retweets': avg_retweets,
            'average_replies': avg_replies,
            'best_performing_post': best_post
        }
