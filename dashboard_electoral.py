"""
Dashboard Interactivo de Análisis Electoral
==========================================

Dashboard web interactivo para visualizar resultados del análisis electoral.

Uso:
    streamlit run dashboard_electoral.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from electoral_analysis.data import DataManager, DemographicSegmentation
from electoral_analysis.social_media import SocialMediaAnalyzer
from electoral_analysis.models import PredictionEngine

# Configuración de la página
st.set_page_config(
    page_title="Análisis Electoral Dashboard",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_electoral_data():
    """Cargar datos electorales con cache"""
    data_manager = DataManager()
    return data_manager.load_electoral_data()

@st.cache_data
def perform_segmentation(data):
    """Realizar segmentación con cache"""
    segmentator = DemographicSegmentation()
    segmented_data = segmentator.perform_segmentation(data, n_segments=5)
    characteristics = segmentator.get_segment_characteristics()
    voting_patterns = segmentator.analyze_segment_voting_patterns(segmented_data)
    return segmented_data, characteristics, voting_patterns

@st.cache_data
def analyze_social_media():
    """Analizar redes sociales con cache"""
    social_analyzer = SocialMediaAnalyzer()
    
    # Candidatos y sus cuentas
    social_accounts = {
        'María González': {'twitter': '@maria_gonzalez', 'facebook': 'maria.gonzalez.oficial'},
        'Carlos Rodríguez': {'twitter': '@carlos_rodriguez', 'facebook': 'carlos.rodriguez.candidato'},
        'Ana Martínez': {'twitter': '@ana_martinez', 'facebook': 'ana.martinez.politica'},
        'Luis Fernández': {'twitter': '@luis_fernandez', 'facebook': 'luis.fernandez.lider'},
        'Carmen López': {'twitter': '@carmen_lopez', 'facebook': 'carmen.lopez.candidata'}
    }
    
    for candidate, accounts in social_accounts.items():
        social_analyzer.add_candidate(candidate, accounts)
    
    results = social_analyzer.analyze_all_candidates(days_back=30)
    comparison = social_analyzer.compare_candidates()
    prediction = social_analyzer.get_winner_prediction_social_media()
    
    return results, comparison, prediction

@st.cache_data
def generate_predictions(data, social_data):
    """Generar predicciones con cache"""
    prediction_engine = PredictionEngine()
    
    # Entrenar modelos
    training_results = prediction_engine.train_models(data, social_data)
    
    # Realizar predicciones
    predictions = prediction_engine.predict_election_results(data, social_data)
    
    # Obtener predicción ensemble
    ensemble_result = prediction_engine.ensemble_prediction(predictions)
    
    # Analizar factores clave
    key_factors = prediction_engine.analyze_key_factors()
    
    return {
        'ensemble_prediction': ensemble_result,
        'individual_predictions': predictions,
        'model_performance': training_results,
        'key_factors': key_factors
    }

def main():
    """Función principal del dashboard"""
    
    # Título principal
    st.title("🗳️ Dashboard de Análisis Electoral")
    st.markdown("---")
    
    # Sidebar para navegación
    st.sidebar.title("Navegación")
    page = st.sidebar.selectbox(
        "Seleccionar análisis:",
        ["Resumen General", "Segmentación Demográfica", "Redes Sociales", "Predicción Electoral", "Comparación de Modelos"]
    )
    
    # Cargar datos
    with st.spinner("Cargando datos electorales..."):
        electoral_data = load_electoral_data()
        segmented_data, segment_characteristics, voting_patterns = perform_segmentation(electoral_data)
        social_results, social_comparison, social_prediction = analyze_social_media()
        prediction_results = generate_predictions(segmented_data, social_results)
    
    # Navegación por páginas
    if page == "Resumen General":
        show_general_overview(electoral_data, prediction_results, social_prediction)
    elif page == "Segmentación Demográfica":
        show_demographic_segmentation(segmented_data, segment_characteristics, voting_patterns)
    elif page == "Redes Sociales":
        show_social_media_analysis(social_results, social_comparison, social_prediction)
    elif page == "Predicción Electoral":
        show_electoral_prediction(prediction_results)
    elif page == "Comparación de Modelos":
        show_model_comparison(prediction_results)

def show_general_overview(data, predictions, social_prediction):
    """Mostrar resumen general"""
    st.header("📊 Resumen General del Análisis Electoral")
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Votantes", f"{len(data):,}")
    
    with col2:
        st.metric("Candidatos", len(data['preferred_candidate'].unique()))
    
    with col3:
        ensemble = predictions['ensemble_prediction']
        winner = ensemble.get('predicted_winner', 'N/A')
        st.metric("Ganador Predicho", winner)
    
    with col4:
        confidence = ensemble.get('confidence_level', 0)
        st.metric("Confianza", f"{confidence:.1%}")
    
    st.markdown("---")
    
    # Gráfico de distribución de candidatos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribución Actual de Preferencias")
        candidate_counts = data['preferred_candidate'].value_counts()
        fig = px.pie(
            values=candidate_counts.values,
            names=candidate_counts.index,
            title="Preferencias de Candidatos en Encuestas"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Predicción Final")
        ranking = ensemble.get('ranking', [])
        if ranking:
            candidates = [item[0] for item in ranking]
            shares = [item[1] for item in ranking]
            
            fig = px.bar(
                x=shares,
                y=candidates,
                orientation='h',
                title="Predicción de Participación de Voto",
                labels={'x': 'Participación Predicha', 'y': 'Candidatos'}
            )
            fig.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
    
    # Comparación de predicciones
    st.markdown("---")
    st.subheader("Comparación de Métodos de Predicción")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Predicción basada en Encuestas:**")
        survey_winner = data['preferred_candidate'].value_counts().index[0]
        survey_share = data['preferred_candidate'].value_counts(normalize=True).iloc[0]
        st.write(f"Ganador: {survey_winner} ({survey_share:.1%})")
    
    with col2:
        st.write("**Predicción basada en Redes Sociales:**")
        social_winner = social_prediction.get('prediccion_ganador', 'N/A')
        st.write(f"Ganador: {social_winner}")

def show_demographic_segmentation(data, characteristics, voting_patterns):
    """Mostrar análisis de segmentación demográfica"""
    st.header("👥 Segmentación Demográfica de Votantes")
    
    # Distribución de segmentos
    segment_counts = data['segment'].value_counts().sort_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribución de Segmentos")
        fig = px.pie(
            values=segment_counts.values,
            names=[f"Segmento {i}" for i in segment_counts.index],
            title="Tamaño de Segmentos Demográficos"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Características por Edad")
        fig = px.box(
            data, 
            x='segment', 
            y='age',
            title="Distribución de Edad por Segmento"
        )
        fig.update_xaxis(title="Segmento")
        fig.update_yaxis(title="Edad")
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabla de características
    st.subheader("Características Detalladas de Segmentos")
    
    # Crear DataFrame para mostrar características
    char_data = []
    for segment_name, char in characteristics.items():
        char_data.append({
            'Segmento': segment_name,
            'Descripción': char['descripcion'],
            'Tamaño': char['tamaño'],
            'Edad Promedio': char['edad_promedio'],
            'Candidato Preferido': char['candidato_preferido'],
            'Intención de Voto': char['intencion_voto_promedio'],
            'Interés Político': char['interes_politico']
        })
    
    char_df = pd.DataFrame(char_data)
    st.dataframe(char_df, use_container_width=True)
    
    # Análisis de preferencias por segmento
    st.subheader("Preferencias de Candidatos por Segmento")
    
    # Crear matriz de preferencias
    preference_matrix = data.groupby(['segment', 'preferred_candidate']).size().unstack(fill_value=0)
    preference_matrix_pct = preference_matrix.div(preference_matrix.sum(axis=1), axis=0) * 100
    
    fig = px.imshow(
        preference_matrix_pct.values,
        x=preference_matrix_pct.columns,
        y=[f"Segmento {i}" for i in preference_matrix_pct.index],
        color_continuous_scale="Blues",
        title="Preferencias de Candidatos por Segmento (%)"
    )
    fig.update_layout(xaxis_title="Candidatos", yaxis_title="Segmentos")
    st.plotly_chart(fig, use_container_width=True)

def show_social_media_analysis(social_results, comparison, social_prediction):
    """Mostrar análisis de redes sociales"""
    st.header("📱 Análisis de Redes Sociales")
    
    # Métricas de redes sociales
    st.subheader("Métricas Principales por Candidato")
    
    # Crear DataFrame de métricas
    metrics_data = []
    for candidate, data in social_results.items():
        engagement = data.get('engagement_metrics', {})
        sentiment = data.get('overall_sentiment', {})
        
        metrics_data.append({
            'Candidato': candidate,
            'Seguidores': engagement.get('total_followers', 0),
            'Posts': engagement.get('total_posts', 0),
            'Engagement Rate': engagement.get('engagement_rate', 0),
            'Score Influencia': data.get('influence_score', 0),
            'Sentimiento Positivo (%)': sentiment.get('positive_percentage', 0),
            'Sentimiento Negativo (%)': sentiment.get('negative_percentage', 0)
        })
    
    metrics_df = pd.DataFrame(metrics_data)
    st.dataframe(metrics_df, use_container_width=True)
    
    # Gráficos de comparación
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Ranking de Influencia")
        influence_ranking = comparison['ranking_influencia']
        candidates = [item[0] for item in influence_ranking]
        scores = [item[1] for item in influence_ranking]
        
        fig = px.bar(
            x=scores,
            y=candidates,
            orientation='h',
            title="Score de Influencia en Redes Sociales",
            labels={'x': 'Score de Influencia', 'y': 'Candidatos'}
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Análisis de Sentimiento")
        sentiment_data = []
        for candidate, data in social_results.items():
            sentiment = data.get('overall_sentiment', {})
            sentiment_data.append({
                'Candidato': candidate,
                'Positivo': sentiment.get('positive_percentage', 0),
                'Negativo': sentiment.get('negative_percentage', 0),
                'Neutral': sentiment.get('neutral_percentage', 0)
            })
        
        sentiment_df = pd.DataFrame(sentiment_data)
        fig = px.bar(
            sentiment_df,
            x='Candidato',
            y=['Positivo', 'Negativo', 'Neutral'],
            title="Distribución de Sentimiento por Candidato",
            labels={'value': 'Porcentaje', 'variable': 'Sentimiento'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Predicción basada en redes sociales
    st.subheader("Predicción basada en Redes Sociales")
    
    col1, col2 = st.columns(2)
    
    with col1:
        winner = social_prediction.get('prediccion_ganador', 'N/A')
        st.metric("Ganador Predicho (Redes Sociales)", winner)
        
        st.write("**Metodología:**")
        methodology = social_prediction.get('metodologia', 'N/A')
        st.write(methodology)
    
    with col2:
        ranking = social_prediction.get('ranking_completo', [])
        if ranking:
            st.write("**Ranking Completo:**")
            for i, (candidate, data) in enumerate(ranking[:5], 1):
                score = data['score_combinado']
                st.write(f"{i}. {candidate}: {score:.1f} puntos")

def show_electoral_prediction(prediction_results):
    """Mostrar predicción electoral"""
    st.header("🎯 Predicción Electoral")
    
    ensemble = prediction_results['ensemble_prediction']
    individual_predictions = prediction_results['individual_predictions']
    key_factors = prediction_results['key_factors']
    
    # Resultado principal
    col1, col2, col3 = st.columns(3)
    
    with col1:
        winner = ensemble.get('predicted_winner', 'N/A')
        st.metric("Ganador Predicho", winner)
    
    with col2:
        confidence = ensemble.get('confidence_level', 0)
        st.metric("Nivel de Confianza", f"{confidence:.1%}")
    
    with col3:
        margin = ensemble.get('margin_of_victory', 0)
        st.metric("Margen de Victoria", f"{margin:.1%}")
    
    # Ranking de candidatos
    st.subheader("Ranking Final de Candidatos")
    
    ranking = ensemble.get('ranking', [])
    if ranking:
        candidates = [item[0] for item in ranking]
        shares = [item[1] * 100 for item in ranking]  # Convertir a porcentaje
        
        fig = px.bar(
            x=candidates,
            y=shares,
            title="Predicción de Participación de Voto (%)",
            labels={'x': 'Candidatos', 'y': 'Participación Predicha (%)'}
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Comparación de modelos
    st.subheader("Predicciones por Modelo Individual")
    
    model_data = []
    for model_name, prediction in individual_predictions.items():
        model_data.append({
            'Modelo': model_name.replace('_', ' ').title(),
            'Ganador Predicho': prediction['predicted_winner'],
            'Probabilidad del Ganador': f"{prediction['winner_probability']:.1%}"
        })
    
    model_df = pd.DataFrame(model_data)
    st.dataframe(model_df, use_container_width=True)
    
    # Factores clave
    st.subheader("Factores Clave de Influencia")
    
    top_factors = key_factors.get('top_factors', [])
    if top_factors:
        factors = [item[0] for item in top_factors[:8]]
        importance = [item[1] for item in top_factors[:8]]
        
        fig = px.bar(
            x=importance,
            y=factors,
            orientation='h',
            title="Importancia de Factores en la Predicción",
            labels={'x': 'Importancia', 'y': 'Factores'}
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

def show_model_comparison(prediction_results):
    """Mostrar comparación de modelos"""
    st.header("🔬 Comparación de Modelos")
    
    model_performance = prediction_results['model_performance']
    individual_predictions = prediction_results['individual_predictions']
    
    # Rendimiento de modelos
    st.subheader("Rendimiento de Modelos")
    
    performance_data = []
    for model_name, performance in model_performance.items():
        performance_data.append({
            'Modelo': model_name.replace('_', ' ').title(),
            'Precisión': f"{performance['accuracy']:.1%}",
            'CV Promedio': f"{performance['cv_mean']:.1%}",
            'CV Desv. Estándar': f"{performance['cv_std']:.3f}"
        })
    
    performance_df = pd.DataFrame(performance_data)
    st.dataframe(performance_df, use_container_width=True)
    
    # Gráfico de precisión
    models = [data['Modelo'] for data in performance_data]
    accuracies = [float(data['Precisión'].strip('%')) for data in performance_data]
    
    fig = px.bar(
        x=models,
        y=accuracies,
        title="Precisión de Modelos (%)",
        labels={'x': 'Modelos', 'y': 'Precisión (%)'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Distribución de votos por modelo
    st.subheader("Distribución de Votos por Modelo")
    
    # Crear gráfico de subplots
    fig = make_subplots(
        rows=1, 
        cols=len(individual_predictions),
        subplot_titles=[name.replace('_', ' ').title() for name in individual_predictions.keys()],
        specs=[[{'type': 'domain'}] * len(individual_predictions)]
    )
    
    for i, (model_name, prediction) in enumerate(individual_predictions.items(), 1):
        vote_share = prediction['vote_share']
        
        fig.add_trace(
            go.Pie(
                labels=list(vote_share.keys()),
                values=list(vote_share.values()),
                name=model_name
            ),
            row=1, col=i
        )
    
    fig.update_layout(title_text="Distribución de Votos Predicha por Cada Modelo")
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
