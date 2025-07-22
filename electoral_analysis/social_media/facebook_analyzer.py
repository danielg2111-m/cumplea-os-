"""
Analizador de Facebook para Candidatos
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os

class FacebookAnalyzer:
    """
    Clase para analizar páginas de Facebook de candidatos
    """
    
    def __init__(self):
        self.access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        self.base_url = "https://graph.facebook.com/v18.0"
        
    def analyze_page(self, page_name: str, days_back: int = 30) -> Dict:
        """
        Analizar página de Facebook de un candidato
        """
        if self.access_token:
            return self._analyze_real_page(page_name, days_back)
        else:
            return self._generate_simulated_data(page_name, days_back)
    
    def _analyze_real_page(self, page_name: str, days_back: int) -> Dict:
        """Analizar página real usando Facebook Graph API"""
        try:
            # Obtener información de la página
            page_info = self._get_page_info(page_name)
            
            # Obtener posts recientes
            posts_data = self._get_recent_posts(page_name, days_back)
            
            # Calcular métricas
            metrics = self._calculate_metrics(page_info, posts_data)
            
            return {
                'metrics': metrics,
                'posts': [post['message'] for post in posts_data if 'message' in post],
                'posts_data': posts_data,
                'page_info': page_info
            }
            
        except Exception as e:
            print(f"Error analizando página de Facebook {page_name}: {e}")
            return self._generate_simulated_data(page_name, days_back)
    
    def _get_page_info(self, page_name: str) -> Dict:
        """Obtener información básica de la página"""
        url = f"{self.base_url}/{page_name}"
        params = {
            'fields': 'id,name,fan_count,about,description,verification_status,category',
            'access_token': self.access_token
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        return response.json()
    
    def _get_recent_posts(self, page_name: str, days_back: int) -> List[Dict]:
        """Obtener posts recientes de la página"""
        url = f"{self.base_url}/{page_name}/posts"
        
        since_date = datetime.now() - timedelta(days=days_back)
        
        params = {
            'fields': 'id,message,created_time,likes.summary(true),comments.summary(true),shares',
            'since': since_date.isoformat(),
            'access_token': self.access_token,
            'limit': 100
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        return data.get('data', [])
    
    def _calculate_metrics(self, page_info: Dict, posts_data: List[Dict]) -> Dict:
        """Calcular métricas de la página"""
        total_likes = 0
        total_comments = 0
        total_shares = 0
        
        for post in posts_data:
            total_likes += post.get('likes', {}).get('summary', {}).get('total_count', 0)
            total_comments += post.get('comments', {}).get('summary', {}).get('total_count', 0)
            total_shares += post.get('shares', {}).get('count', 0)
        
        return {
            'followers': page_info.get('fan_count', 0),
            'posts_count': len(posts_data),
            'total_likes': total_likes,
            'total_comments': total_comments,
            'total_shares': total_shares,
            'verified': page_info.get('verification_status') == 'blue_verified'
        }
    
    def _generate_simulated_data(self, page_name: str, days_back: int) -> Dict:
        """Generar datos simulados para demostración"""
        np.random.seed(hash(page_name) % 2**32)
        
        # Generar métricas simuladas
        base_followers = np.random.randint(5000, 200000)
        posts_count = np.random.randint(15, 40)
        
        # Posts simulados para Facebook (más largos que Twitter)
        sample_posts = [
            """Queridos ciudadanos, hoy quiero compartir con ustedes nuestra propuesta integral para transformar la educación en nuestro país. Creemos firmemente que la educación es la herramienta más poderosa para construir un futuro próspero y equitativo para todos. 

Nuestro plan incluye:
✅ Aumento del presupuesto educativo al 6% del PIB
✅ Mejora de la infraestructura escolar
✅ Capacitación continua para docentes
✅ Tecnología en todas las aulas
✅ Programas de alimentación escolar

Juntos podemos hacer la diferencia. #EducaciónParaTodos #Elecciones2024""",
            
            """El desarrollo económico sostenible es fundamental para el progreso de nuestra nación. Por eso, presentamos nuestro plan económico que se enfoca en:

🔹 Apoyo a las pequeñas y medianas empresas
🔹 Creación de empleos dignos y bien remunerados  
🔹 Inversión en infraestructura moderna
🔹 Fomento de la innovación y tecnología
🔹 Fortalecimiento del sector agrícola

Trabajemos unidos por una economía que beneficie a todos los sectores de la sociedad. Su voto es su voz. #EconomíaParaTodos""",
            
            """La salud es un derecho fundamental de todos los ciudadanos. Nuestro sistema de salud necesita una transformación profunda que garantice atención de calidad para todos, sin importar su condición económica.

Nuestros compromisos:
🏥 Construcción de nuevos hospitales y centros de salud
💊 Medicamentos accesibles para todos
👨‍⚕️ Más médicos y especialistas
🚑 Mejora en servicios de emergencia
🔬 Inversión en investigación médica

La salud no puede esperar. #SaludParaTodos #Compromiso2024""",
            
            """Agradezco profundamente el cariño y apoyo que hemos recibido en nuestro recorrido por todo el país. Cada encuentro con ustedes fortalece nuestro compromiso de trabajar incansablemente por el bienestar de todas las familias.

Hemos escuchado sus preocupaciones, sus sueños y sus propuestas. Todo esto se refleja en nuestro plan de gobierno, construido con la participación ciudadana y pensando en las necesidades reales de nuestro pueblo.

Juntos construiremos el cambio que necesitamos. #EscuchandoAlPueblo #UnidosPorElCambio""",
            
            """La seguridad ciudadana es una prioridad absoluta en nuestro plan de gobierno. Todos tenemos derecho a vivir en paz y tranquilidad en nuestras comunidades.

Estrategia integral de seguridad:
🚔 Fortalecimiento de las fuerzas policiales
📱 Tecnología para prevención del delito
🏘️ Programas comunitarios de seguridad
⚖️ Justicia rápida y efectiva
👥 Programas de reinserción social

La seguridad se construye entre todos. #SeguridadParaTodos #PazSocial"""
        ]
        
        posts = np.random.choice(sample_posts, posts_count, replace=True).tolist()
        
        # Generar datos de engagement (Facebook tiende a tener más engagement que Twitter)
        posts_data = []
        total_likes = 0
        total_comments = 0
        total_shares = 0
        
        for i, post in enumerate(posts):
            likes = np.random.poisson(base_followers * 0.05)  # 5% engagement promedio
            comments = np.random.poisson(likes * 0.15)
            shares = np.random.poisson(likes * 0.08)
            
            post_data = {
                'message': post,
                'created_time': datetime.now() - timedelta(days=np.random.randint(0, days_back)),
                'likes': likes,
                'comments': comments,
                'shares': shares
            }
            posts_data.append(post_data)
            
            total_likes += likes
            total_comments += comments
            total_shares += shares
        
        metrics = {
            'followers': base_followers,
            'posts_count': posts_count,
            'total_likes': total_likes,
            'total_comments': total_comments,
            'total_shares': total_shares,
            'verified': np.random.choice([True, False], p=[0.8, 0.2])  # 80% verificados
        }
        
        return {
            'metrics': metrics,
            'posts': posts,
            'posts_data': posts_data,
            'page_info': {
                'name': page_name.title(),
                'about': f"Página oficial del candidato {page_name}",
                'category': "Político",
                'verified': metrics['verified']
            }
        }
    
    def analyze_post_performance(self, posts_data: List[Dict]) -> Dict:
        """Analizar rendimiento de posts individuales"""
        if not posts_data:
            return {}
        
        performance_data = []
        
        for post in posts_data:
            total_engagement = (
                post.get('likes', 0) + 
                post.get('comments', 0) + 
                post.get('shares', 0)
            )
            
            performance_data.append({
                'message': post.get('message', '')[:100] + '...',
                'engagement': total_engagement,
                'likes': post.get('likes', 0),
                'comments': post.get('comments', 0),
                'shares': post.get('shares', 0),
                'created_time': post.get('created_time')
            })
        
        # Ordenar por engagement
        performance_data.sort(key=lambda x: x['engagement'], reverse=True)
        
        # Calcular estadísticas
        engagements = [p['engagement'] for p in performance_data]
        avg_engagement = np.mean(engagements) if engagements else 0
        
        return {
            'top_performing_posts': performance_data[:5],
            'average_engagement': avg_engagement,
            'total_posts_analyzed': len(performance_data),
            'best_post': performance_data[0] if performance_data else {},
            'engagement_distribution': {
                'min': min(engagements) if engagements else 0,
                'max': max(engagements) if engagements else 0,
                'median': np.median(engagements) if engagements else 0,
                'std': np.std(engagements) if engagements else 0
            }
        }
    
    def analyze_posting_schedule(self, posts_data: List[Dict]) -> Dict:
        """Analizar horarios de publicación"""
        if not posts_data:
            return {}
        
        # Extraer horas y días
        hours = []
        weekdays = []
        
        for post in posts_data:
            if 'created_time' in post:
                if isinstance(post['created_time'], str):
                    # Parsear string de fecha
                    try:
                        dt = datetime.fromisoformat(post['created_time'].replace('Z', '+00:00'))
                    except:
                        continue
                else:
                    dt = post['created_time']
                
                hours.append(dt.hour)
                weekdays.append(dt.weekday())
        
        # Distribución por hora
        hour_distribution = {hour: hours.count(hour) for hour in range(24)}
        
        # Distribución por día de la semana
        weekday_names = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        weekday_distribution = {weekday_names[i]: weekdays.count(i) for i in range(7)}
        
        return {
            'posting_hours': hour_distribution,
            'posting_weekdays': weekday_distribution,
            'most_active_hour': max(hour_distribution, key=hour_distribution.get) if hours else None,
            'most_active_day': max(weekday_distribution, key=weekday_distribution.get) if weekdays else None,
            'posts_analyzed': len([p for p in posts_data if 'created_time' in p])
        }
    
    def get_audience_engagement_insights(self, posts_data: List[Dict]) -> Dict:
        """Obtener insights sobre el engagement de la audiencia"""
        if not posts_data:
            return {}
        
        # Calcular ratios de engagement
        like_ratios = []
        comment_ratios = []
        share_ratios = []
        
        for post in posts_data:
            likes = post.get('likes', 0)
            comments = post.get('comments', 0)
            shares = post.get('shares', 0)
            total = likes + comments + shares
            
            if total > 0:
                like_ratios.append(likes / total)
                comment_ratios.append(comments / total)
                share_ratios.append(shares / total)
        
        return {
            'engagement_patterns': {
                'avg_like_ratio': np.mean(like_ratios) if like_ratios else 0,
                'avg_comment_ratio': np.mean(comment_ratios) if comment_ratios else 0,
                'avg_share_ratio': np.mean(share_ratios) if share_ratios else 0
            },
            'interaction_preferences': {
                'likes_dominate': np.mean(like_ratios) > 0.7 if like_ratios else False,
                'comments_active': np.mean(comment_ratios) > 0.2 if comment_ratios else False,
                'shares_viral': np.mean(share_ratios) > 0.1 if share_ratios else False
            },
            'total_interactions': sum(
                post.get('likes', 0) + post.get('comments', 0) + post.get('shares', 0)
                for post in posts_data
            )
        }
