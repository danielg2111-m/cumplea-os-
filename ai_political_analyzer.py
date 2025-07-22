#!/usr/bin/env python3
"""
Módulo de Inteligencia Artificial para Análisis Político Electoral
Analiza comportamiento electoral, encuestas y redes sociales
"""
import os
import json
import requests
from datetime import datetime, timedelta
import time
from flask import Flask, request, jsonify, render_template_string
from dotenv import load_dotenv
import logging
import sqlite3
from typing import Dict, List, Optional
import re
from collections import Counter
import statistics

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PoliticalAIAnalyzer:
    """Sistema de IA para análisis político electoral"""
    
    def __init__(self):
        self.db_path = "political_analysis.db"
        self.init_database()
        
        # Flask app
        self.app = Flask(__name__)
        self.setup_routes()
        
        # Configuración de redes sociales (APIs)
        self.twitter_bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        self.facebook_access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        self.instagram_access_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
        
        # Palabras clave políticas para análisis de sentimiento
        self.political_keywords = {
            'positivo': ['excelente', 'bueno', 'apoyo', 'voto', 'confianza', 'progreso', 'cambio positivo', 'líder', 'futuro'],
            'negativo': ['malo', 'rechazo', 'corrupción', 'mentira', 'fracaso', 'crisis', 'problema', 'incompetente'],
            'neutral': ['candidato', 'elección', 'propuesta', 'debate', 'política', 'gobierno', 'partido']
        }
        
        logger.info("🤖 Sistema de IA Política inicializado")
    
    def init_database(self):
        """Inicializar base de datos SQLite"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de candidatos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                party TEXT,
                position TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de encuestas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS polls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                candidate_id INTEGER,
                poll_date DATE,
                percentage REAL,
                sample_size INTEGER,
                margin_error REAL,
                poll_company TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (candidate_id) REFERENCES candidates (id)
            )
        ''')
        
        # Tabla de análisis de redes sociales
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS social_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                candidate_id INTEGER,
                platform TEXT,
                mentions INTEGER,
                positive_sentiment REAL,
                negative_sentiment REAL,
                neutral_sentiment REAL,
                engagement_rate REAL,
                analysis_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (candidate_id) REFERENCES candidates (id)
            )
        ''')
        
        # Tabla de predicciones electorales
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                candidate_id INTEGER,
                predicted_percentage REAL,
                confidence_level REAL,
                prediction_date DATE,
                model_version TEXT,
                factors_considered TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (candidate_id) REFERENCES candidates (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("📊 Base de datos inicializada")
    
    def setup_routes(self):
        """Configurar rutas de Flask"""
        
        @self.app.route('/', methods=['GET'])
        def dashboard():
            """Dashboard principal de análisis político"""
            dashboard_html = '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>🏛️ Análisis Político IA</title>
                <meta charset="utf-8">
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
                    .container { max-width: 1200px; margin: 0 auto; }
                    .card { background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                    .header { text-align: center; color: #2c3e50; }
                    .stats { display: flex; justify-content: space-around; flex-wrap: wrap; }
                    .stat-item { text-align: center; padding: 15px; }
                    .stat-number { font-size: 2em; font-weight: bold; color: #3498db; }
                    .stat-label { color: #7f8c8d; }
                    .btn { background: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; margin: 5px; }
                    .btn:hover { background: #2980b9; }
                    .form-group { margin: 15px 0; }
                    .form-group label { display: block; margin-bottom: 5px; font-weight: bold; }
                    .form-group input, .form-group select, .form-group textarea { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="card header">
                        <h1>🏛️ Sistema de Análisis Político con IA</h1>
                        <p>Análisis de comportamiento electoral, encuestas y redes sociales</p>
                    </div>
                    
                    <div class="card">
                        <h2>📊 Estadísticas Generales</h2>
                        <div class="stats">
                            <div class="stat-item">
                                <div class="stat-number" id="total-candidates">0</div>
                                <div class="stat-label">Candidatos</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-number" id="total-polls">0</div>
                                <div class="stat-label">Encuestas</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-number" id="social-mentions">0</div>
                                <div class="stat-label">Menciones Sociales</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-number" id="predictions">0</div>
                                <div class="stat-label">Predicciones</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="card">
                        <h2>➕ Agregar Candidato</h2>
                        <form id="candidate-form">
                            <div class="form-group">
                                <label>Nombre del Candidato:</label>
                                <input type="text" id="candidate-name" required>
                            </div>
                            <div class="form-group">
                                <label>Partido Político:</label>
                                <input type="text" id="candidate-party">
                            </div>
                            <div class="form-group">
                                <label>Posición/Cargo:</label>
                                <input type="text" id="candidate-position">
                            </div>
                            <button type="submit" class="btn">Agregar Candidato</button>
                        </form>
                    </div>
                    
                    <div class="card">
                        <h2>📈 Subir Encuesta</h2>
                        <form id="poll-form">
                            <div class="form-group">
                                <label>Candidato:</label>
                                <select id="poll-candidate" required>
                                    <option value="">Seleccionar candidato...</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Porcentaje de Intención de Voto:</label>
                                <input type="number" id="poll-percentage" step="0.1" min="0" max="100" required>
                            </div>
                            <div class="form-group">
                                <label>Tamaño de Muestra:</label>
                                <input type="number" id="poll-sample" required>
                            </div>
                            <div class="form-group">
                                <label>Margen de Error (%):</label>
                                <input type="number" id="poll-margin" step="0.1" required>
                            </div>
                            <div class="form-group">
                                <label>Empresa Encuestadora:</label>
                                <input type="text" id="poll-company" required>
                            </div>
                            <button type="submit" class="btn">Subir Encuesta</button>
                        </form>
                    </div>
                    
                    <div class="card">
                        <h2>🔍 Análisis de Redes Sociales</h2>
                        <button onclick="analyzeSocialMedia()" class="btn">Analizar Redes Sociales</button>
                        <button onclick="generatePredictions()" class="btn">Generar Predicciones IA</button>
                        <button onclick="getElectoralTrends()" class="btn">Ver Tendencias Electorales</button>
                    </div>
                    
                    <div class="card">
                        <h2>📋 Resultados de Análisis</h2>
                        <div id="analysis-results">
                            <p>Los resultados del análisis aparecerán aquí...</p>
                        </div>
                    </div>
                </div>
                
                <script>
                    // Cargar estadísticas al inicio
                    loadStats();
                    loadCandidates();
                    
                    function loadStats() {
                        fetch('/api/stats')
                            .then(response => response.json())
                            .then(data => {
                                document.getElementById('total-candidates').textContent = data.candidates || 0;
                                document.getElementById('total-polls').textContent = data.polls || 0;
                                document.getElementById('social-mentions').textContent = data.social_mentions || 0;
                                document.getElementById('predictions').textContent = data.predictions || 0;
                            });
                    }
                    
                    function loadCandidates() {
                        fetch('/api/candidates')
                            .then(response => response.json())
                            .then(data => {
                                const select = document.getElementById('poll-candidate');
                                select.innerHTML = '<option value="">Seleccionar candidato...</option>';
                                data.forEach(candidate => {
                                    const option = document.createElement('option');
                                    option.value = candidate.id;
                                    option.textContent = candidate.name + ' (' + candidate.party + ')';
                                    select.appendChild(option);
                                });
                            });
                    }
                    
                    // Formulario de candidato
                    document.getElementById('candidate-form').addEventListener('submit', function(e) {
                        e.preventDefault();
                        const data = {
                            name: document.getElementById('candidate-name').value,
                            party: document.getElementById('candidate-party').value,
                            position: document.getElementById('candidate-position').value
                        };
                        
                        fetch('/api/candidates', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify(data)
                        })
                        .then(response => response.json())
                        .then(result => {
                            alert('Candidato agregado exitosamente');
                            this.reset();
                            loadStats();
                            loadCandidates();
                        });
                    });
                    
                    // Formulario de encuesta
                    document.getElementById('poll-form').addEventListener('submit', function(e) {
                        e.preventDefault();
                        const data = {
                            candidate_id: document.getElementById('poll-candidate').value,
                            percentage: parseFloat(document.getElementById('poll-percentage').value),
                            sample_size: parseInt(document.getElementById('poll-sample').value),
                            margin_error: parseFloat(document.getElementById('poll-margin').value),
                            poll_company: document.getElementById('poll-company').value
                        };
                        
                        fetch('/api/polls', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify(data)
                        })
                        .then(response => response.json())
                        .then(result => {
                            alert('Encuesta subida exitosamente');
                            this.reset();
                            loadStats();
                        });
                    });
                    
                    function analyzeSocialMedia() {
                        document.getElementById('analysis-results').innerHTML = '<p>🔄 Analizando redes sociales...</p>';
                        fetch('/api/analyze-social-media', {method: 'POST'})
                            .then(response => response.json())
                            .then(data => {
                                document.getElementById('analysis-results').innerHTML = 
                                    '<h3>📱 Análisis de Redes Sociales</h3><pre>' + JSON.stringify(data, null, 2) + '</pre>';
                            });
                    }
                    
                    function generatePredictions() {
                        document.getElementById('analysis-results').innerHTML = '<p>🤖 Generando predicciones con IA...</p>';
                        fetch('/api/generate-predictions', {method: 'POST'})
                            .then(response => response.json())
                            .then(data => {
                                document.getElementById('analysis-results').innerHTML = 
                                    '<h3>🔮 Predicciones Electorales IA</h3><pre>' + JSON.stringify(data, null, 2) + '</pre>';
                            });
                    }
                    
                    function getElectoralTrends() {
                        document.getElementById('analysis-results').innerHTML = '<p>📈 Analizando tendencias...</p>';
                        fetch('/api/electoral-trends')
                            .then(response => response.json())
                            .then(data => {
                                document.getElementById('analysis-results').innerHTML = 
                                    '<h3>📊 Tendencias Electorales</h3><pre>' + JSON.stringify(data, null, 2) + '</pre>';
                            });
                    }
                </script>
            </body>
            </html>
            '''
            return dashboard_html
        
        @self.app.route('/api/stats', methods=['GET'])
        def get_stats():
            """Obtener estadísticas generales"""
            return jsonify(self.get_general_stats())
        
        @self.app.route('/api/candidates', methods=['GET', 'POST'])
        def handle_candidates():
            """Manejar candidatos"""
            if request.method == 'POST':
                return jsonify(self.add_candidate(request.json))
            else:
                return jsonify(self.get_candidates())
        
        @self.app.route('/api/polls', methods=['POST'])
        def add_poll():
            """Agregar encuesta"""
            return jsonify(self.add_poll_data(request.json))
        
        @self.app.route('/api/analyze-social-media', methods=['POST'])
        def analyze_social():
            """Analizar redes sociales"""
            return jsonify(self.analyze_social_media())
        
        @self.app.route('/api/generate-predictions', methods=['POST'])
        def generate_predictions():
            """Generar predicciones con IA"""
            return jsonify(self.generate_ai_predictions())
        
        @self.app.route('/api/electoral-trends', methods=['GET'])
        def electoral_trends():
            """Obtener tendencias electorales"""
            return jsonify(self.get_electoral_trends())
    
    def get_general_stats(self):
        """Obtener estadísticas generales"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Contar candidatos
        cursor.execute("SELECT COUNT(*) FROM candidates")
        candidates_count = cursor.fetchone()[0]
        
        # Contar encuestas
        cursor.execute("SELECT COUNT(*) FROM polls")
        polls_count = cursor.fetchone()[0]
        
        # Contar menciones sociales
        cursor.execute("SELECT SUM(mentions) FROM social_analysis")
        social_mentions = cursor.fetchone()[0] or 0
        
        # Contar predicciones
        cursor.execute("SELECT COUNT(*) FROM predictions")
        predictions_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'candidates': candidates_count,
            'polls': polls_count,
            'social_mentions': social_mentions,
            'predictions': predictions_count
        }
    
    def get_candidates(self):
        """Obtener lista de candidatos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name, party, position FROM candidates ORDER BY name")
        candidates = []
        for row in cursor.fetchall():
            candidates.append({
                'id': row[0],
                'name': row[1],
                'party': row[2],
                'position': row[3]
            })
        
        conn.close()
        return candidates
    
    def add_candidate(self, data):
        """Agregar nuevo candidato"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO candidates (name, party, position) VALUES (?, ?, ?)",
                (data['name'], data.get('party', ''), data.get('position', ''))
            )
            
            candidate_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            logger.info(f"✅ Candidato agregado: {data['name']}")
            return {'success': True, 'candidate_id': candidate_id, 'message': 'Candidato agregado exitosamente'}
        
        except Exception as e:
            logger.error(f"❌ Error agregando candidato: {e}")
            return {'success': False, 'error': str(e)}
    
    def add_poll_data(self, data):
        """Agregar datos de encuesta"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO polls (candidate_id, poll_date, percentage, sample_size, margin_error, poll_company)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                data['candidate_id'],
                datetime.now().date(),
                data['percentage'],
                data['sample_size'],
                data['margin_error'],
                data['poll_company']
            ))
            
            poll_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            logger.info(f"📊 Encuesta agregada para candidato ID: {data['candidate_id']}")
            return {'success': True, 'poll_id': poll_id, 'message': 'Encuesta agregada exitosamente'}
        
        except Exception as e:
            logger.error(f"❌ Error agregando encuesta: {e}")
            return {'success': False, 'error': str(e)}
    
    def analyze_social_media(self):
        """Analizar comportamiento en redes sociales"""
        try:
            # Simular análisis de redes sociales (en producción usarías APIs reales)
            candidates = self.get_candidates()
            analysis_results = []
            
            for candidate in candidates:
                # Simulación de datos de redes sociales
                social_data = self.simulate_social_media_data(candidate['name'])
                
                # Guardar en base de datos
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                for platform, data in social_data.items():
                    cursor.execute('''
                        INSERT INTO social_analysis 
                        (candidate_id, platform, mentions, positive_sentiment, negative_sentiment, 
                         neutral_sentiment, engagement_rate, analysis_date)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        candidate['id'], platform, data['mentions'],
                        data['positive_sentiment'], data['negative_sentiment'],
                        data['neutral_sentiment'], data['engagement_rate'],
                        datetime.now().date()
                    ))
                
                conn.commit()
                conn.close()
                
                analysis_results.append({
                    'candidate': candidate['name'],
                    'social_data': social_data,
                    'overall_sentiment': self.calculate_overall_sentiment(social_data)
                })
            
            logger.info("📱 Análisis de redes sociales completado")
            return {
                'success': True,
                'analysis_date': datetime.now().isoformat(),
                'results': analysis_results
            }
        
        except Exception as e:
            logger.error(f"❌ Error en análisis social: {e}")
            return {'success': False, 'error': str(e)}
    
    def simulate_social_media_data(self, candidate_name):
        """Simular datos de redes sociales (reemplazar con APIs reales)"""
        import random
        
        platforms = ['Twitter', 'Facebook', 'Instagram', 'TikTok']
        social_data = {}
        
        for platform in platforms:
            mentions = random.randint(100, 5000)
            positive = random.uniform(0.2, 0.6)
            negative = random.uniform(0.1, 0.4)
            neutral = 1.0 - positive - negative
            
            social_data[platform] = {
                'mentions': mentions,
                'positive_sentiment': round(positive, 3),
                'negative_sentiment': round(negative, 3),
                'neutral_sentiment': round(neutral, 3),
                'engagement_rate': round(random.uniform(0.02, 0.15), 3),
                'trending_topics': [
                    f"{candidate_name} propuestas",
                    f"debate {candidate_name}",
                    f"campaña {candidate_name}"
                ]
            }
        
        return social_data
    
    def calculate_overall_sentiment(self, social_data):
        """Calcular sentimiento general"""
        total_mentions = sum(data['mentions'] for data in social_data.values())
        if total_mentions == 0:
            return {'positive': 0, 'negative': 0, 'neutral': 0}
        
        weighted_positive = sum(data['mentions'] * data['positive_sentiment'] for data in social_data.values())
        weighted_negative = sum(data['mentions'] * data['negative_sentiment'] for data in social_data.values())
        weighted_neutral = sum(data['mentions'] * data['neutral_sentiment'] for data in social_data.values())
        
        return {
            'positive': round(weighted_positive / total_mentions, 3),
            'negative': round(weighted_negative / total_mentions, 3),
            'neutral': round(weighted_neutral / total_mentions, 3),
            'sentiment_score': round((weighted_positive - weighted_negative) / total_mentions, 3)
        }
    
    def generate_ai_predictions(self):
        """Generar predicciones electorales usando IA"""
        try:
            candidates = self.get_candidates()
            predictions = []
            
            for candidate in candidates:
                # Obtener datos históricos de encuestas
                poll_data = self.get_candidate_poll_history(candidate['id'])
                
                # Obtener datos de redes sociales
                social_data = self.get_candidate_social_data(candidate['id'])
                
                # Algoritmo de predicción (simplificado)
                prediction = self.calculate_electoral_prediction(candidate, poll_data, social_data)
                
                # Guardar predicción
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO predictions 
                    (candidate_id, predicted_percentage, confidence_level, prediction_date, 
                     model_version, factors_considered)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    candidate['id'], prediction['percentage'], prediction['confidence'],
                    datetime.now().date(), 'v1.0', json.dumps(prediction['factors'])
                ))
                
                conn.commit()
                conn.close()
                
                predictions.append({
                    'candidate': candidate['name'],
                    'party': candidate['party'],
                    'predicted_percentage': prediction['percentage'],
                    'confidence_level': prediction['confidence'],
                    'factors': prediction['factors'],
                    'trend': prediction['trend']
                })
            
            # Ordenar por predicción
            predictions.sort(key=lambda x: x['predicted_percentage'], reverse=True)
            
            logger.info("🤖 Predicciones IA generadas")
            return {
                'success': True,
                'prediction_date': datetime.now().isoformat(),
                'model_version': 'v1.0',
                'predictions': predictions,
                'total_coverage': sum(p['predicted_percentage'] for p in predictions)
            }
        
        except Exception as e:
            logger.error(f"❌ Error generando predicciones: {e}")
            return {'success': False, 'error': str(e)}
    
    def calculate_electoral_prediction(self, candidate, poll_data, social_data):
        """Calcular predicción electoral usando múltiples factores"""
        import random
        
        # Factores base
        base_percentage = random.uniform(10, 35)  # Simulación
        
        # Ajuste por encuestas recientes
        poll_adjustment = 0
        if poll_data:
            recent_polls = [p['percentage'] for p in poll_data[-3:]]  # Últimas 3 encuestas
            if recent_polls:
                poll_trend = statistics.mean(recent_polls)
                poll_adjustment = (poll_trend - base_percentage) * 0.4
        
        # Ajuste por redes sociales
        social_adjustment = 0
        if social_data:
            sentiment_score = social_data.get('sentiment_score', 0)
            social_adjustment = sentiment_score * 5  # Convertir a porcentaje
        
        # Predicción final
        final_percentage = max(0, min(100, base_percentage + poll_adjustment + social_adjustment))
        
        # Calcular confianza
        confidence = random.uniform(0.6, 0.9)
        
        # Determinar tendencia
        trend = 'estable'
        if poll_adjustment > 2:
            trend = 'ascendente'
        elif poll_adjustment < -2:
            trend = 'descendente'
        
        return {
            'percentage': round(final_percentage, 2),
            'confidence': round(confidence, 3),
            'trend': trend,
            'factors': {
                'base_support': round(base_percentage, 2),
                'poll_influence': round(poll_adjustment, 2),
                'social_influence': round(social_adjustment, 2),
                'poll_count': len(poll_data) if poll_data else 0,
                'social_mentions': social_data.get('total_mentions', 0) if social_data else 0
            }
        }
    
    def get_candidate_poll_history(self, candidate_id):
        """Obtener historial de encuestas de un candidato"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT percentage, poll_date, sample_size, margin_error, poll_company
            FROM polls 
            WHERE candidate_id = ?
            ORDER BY poll_date DESC
        ''', (candidate_id,))
        
        polls = []
        for row in cursor.fetchall():
            polls.append({
                'percentage': row[0],
                'date': row[1],
                'sample_size': row[2],
                'margin_error': row[3],
                'company': row[4]
            })
        
        conn.close()
        return polls
    
    def get_candidate_social_data(self, candidate_id):
        """Obtener datos de redes sociales de un candidato"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT platform, mentions, positive_sentiment, negative_sentiment, 
                   neutral_sentiment, engagement_rate
            FROM social_analysis 
            WHERE candidate_id = ? AND analysis_date >= date('now', '-7 days')
        ''', (candidate_id,))
        
        social_data = {
            'total_mentions': 0,
            'sentiment_score': 0,
            'platforms': {}
        }
        
        total_weighted_sentiment = 0
        total_mentions = 0
        
        for row in cursor.fetchall():
            platform, mentions, pos, neg, neu, engagement = row
            social_data['platforms'][platform] = {
                'mentions': mentions,
                'positive': pos,
                'negative': neg,
                'neutral': neu,
                'engagement': engagement
            }
            
            total_mentions += mentions
            total_weighted_sentiment += mentions * (pos - neg)
        
        social_data['total_mentions'] = total_mentions
        if total_mentions > 0:
            social_data['sentiment_score'] = total_weighted_sentiment / total_mentions
        
        conn.close()
        return social_data
    
    def get_electoral_trends(self):
        """Obtener tendencias electorales"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Tendencias de encuestas por candidato
            cursor.execute('''
                SELECT c.name, c.party, p.percentage, p.poll_date
                FROM candidates c
                JOIN polls p ON c.id = p.candidate_id
                ORDER BY c.name, p.poll_date DESC
            ''')
            
            trends = {}
            for row in cursor.fetchall():
                name, party, percentage, date = row
                if name not in trends:
                    trends[name] = {
                        'party': party,
                        'polls': [],
                        'average': 0,
                        'trend': 'estable'
                    }
                trends[name]['polls'].append({
                    'percentage': percentage,
                    'date': date
                })
            
            # Calcular promedios y tendencias
            for candidate, data in trends.items():
                if data['polls']:
                    data['average'] = round(statistics.mean([p['percentage'] for p in data['polls']]), 2)
                    
                    # Calcular tendencia
                    if len(data['polls']) >= 2:
                        recent = statistics.mean([p['percentage'] for p in data['polls'][:2]])
                        older = statistics.mean([p['percentage'] for p in data['polls'][-2:]])
                        
                        if recent > older + 1:
                            data['trend'] = 'ascendente'
                        elif recent < older - 1:
                            data['trend'] = 'descendente'
            
            conn.close()
            
            return {
                'success': True,
                'analysis_date': datetime.now().isoformat(),
                'trends': trends,
                'summary': {
                    'total_candidates': len(trends),
                    'leading_candidate': max(trends.items(), key=lambda x: x[1]['average'])[0] if trends else None
                }
            }
        
        except Exception as e:
            logger.error(f"❌ Error obteniendo tendencias: {e}")
            return {'success': False, 'error': str(e)}
    
    def start_server(self, host='0.0.0.0', port=5001, debug=False):
        """Iniciar servidor Flask"""
        logger.info(f"🚀 Iniciando Sistema de Análisis Político IA en {host}:{port}")
        logger.info("🏛️ Dashboard disponible en: http://localhost:5001")
        
        self.app.run(host=host, port=port, debug=debug)

def main():
    """Función principal"""
    print("🏛️ Sistema de Análisis Político con IA")
    print("=" * 60)
    print("📊 Funcionalidades:")
    print("   • Análisis de comportamiento electoral")
    print("   • Gestión de encuestas políticas")
    print("   • Análisis de redes sociales")
    print("   • Predicciones electorales con IA")
    print("   • Tendencias y estadísticas")
    print("=" * 60)
    
    # Crear e iniciar el sistema
    analyzer = PoliticalAIAnalyzer()
    
    try:
        analyzer.start_server()
    except KeyboardInterrupt:
        print("\n👋 Sistema detenido por el usuario")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
