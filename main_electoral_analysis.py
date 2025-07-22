"""
Sistema Principal de Análisis Electoral
======================================

Este es el archivo principal que ejecuta el análisis electoral completo:
1. Análisis del comportamiento electoral y segmentación
2. Análisis de redes sociales de todos los candidatos
3. Predicción del posible ganador

Uso:
    python main_electoral_analysis.py
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os
import sys

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from electoral_analysis.data import DataManager, DemographicSegmentation
from electoral_analysis.social_media import SocialMediaAnalyzer
from electoral_analysis.models import PredictionEngine

def main():
    """Función principal del análisis electoral"""
    
    print("=" * 60)
    print("SISTEMA DE ANÁLISIS ELECTORAL COMPLETO")
    print("=" * 60)
    print()
    
    # ============================================================================
    # 1. CARGA Y PREPARACIÓN DE DATOS
    # ============================================================================
    print("1. CARGANDO Y PREPARANDO DATOS ELECTORALES...")
    print("-" * 50)
    
    # Inicializar gestor de datos
    data_manager = DataManager()
    
    # Cargar datos electorales (usa datos simulados si no hay archivo)
    electoral_data = data_manager.load_electoral_data()
    print(f"✓ Datos cargados: {len(electoral_data)} registros de votantes")
    
    # Obtener resumen demográfico
    demographic_summary = data_manager.get_demographic_summary(electoral_data)
    print(f"✓ Candidatos en el análisis: {len(data_manager.get_candidate_list(electoral_data))}")
    print(f"✓ Regiones analizadas: {len(demographic_summary['regional_distribution'])}")
    print()
    
    # ============================================================================
    # 2. ANÁLISIS DEL COMPORTAMIENTO ELECTORAL Y SEGMENTACIÓN
    # ============================================================================
    print("2. ANÁLISIS DEL COMPORTAMIENTO ELECTORAL Y SEGMENTACIÓN...")
    print("-" * 60)
    
    # Inicializar segmentador demográfico
    segmentator = DemographicSegmentation()
    
    # Realizar segmentación
    segmented_data = segmentator.perform_segmentation(electoral_data, n_segments=5)
    print(f"✓ Segmentación completada: {len(segmented_data['segment'].unique())} segmentos identificados")
    
    # Obtener características de segmentos
    segment_characteristics = segmentator.get_segment_characteristics()
    print("✓ Segmentos demográficos identificados:")
    for segment_name, char in segment_characteristics.items():
        print(f"   - {segment_name}: {char['descripcion']}")
        print(f"     Tamaño: {char['tamaño']}, Candidato preferido: {char['candidato_preferido']}")
    
    # Analizar patrones de voto por segmento
    voting_patterns = segmentator.analyze_segment_voting_patterns(segmented_data)
    print(f"✓ Patrones de voto analizados para {len(voting_patterns)} segmentos")
    
    # Predecir participación por segmento
    turnout_predictions = segmentator.predict_segment_turnout(segmented_data)
    print("✓ Predicciones de participación:")
    for segment, prediction in turnout_predictions.items():
        participation = prediction['participacion_estimada']
        print(f"   - {segment}: {participation:.1%} participación estimada")
    
    # Exportar reporte de segmentación
    segmentator.export_segmentation_report(segmented_data, 'reporte_segmentacion.txt')
    print("✓ Reporte de segmentación exportado: reporte_segmentacion.txt")
    print()
    
    # ============================================================================
    # 3. ANÁLISIS DE REDES SOCIALES DE CANDIDATOS
    # ============================================================================
    print("3. ANÁLISIS DE REDES SOCIALES DE TODOS LOS CANDIDATOS...")
    print("-" * 60)
    
    # Inicializar analizador de redes sociales
    social_analyzer = SocialMediaAnalyzer()
    
    # Obtener lista de candidatos
    candidates = data_manager.get_candidate_list(electoral_data)
    
    # Agregar candidatos con sus cuentas de redes sociales (simuladas)
    social_accounts = {
        'María González': {'twitter': '@maria_gonzalez', 'facebook': 'maria.gonzalez.oficial'},
        'Carlos Rodríguez': {'twitter': '@carlos_rodriguez', 'facebook': 'carlos.rodriguez.candidato'},
        'Ana Martínez': {'twitter': '@ana_martinez', 'facebook': 'ana.martinez.politica'},
        'Luis Fernández': {'twitter': '@luis_fernandez', 'facebook': 'luis.fernandez.lider'},
        'Carmen López': {'twitter': '@carmen_lopez', 'facebook': 'carmen.lopez.candidata'}
    }
    
    # Agregar candidatos al analizador
    for candidate in candidates:
        if candidate in social_accounts:
            social_analyzer.add_candidate(candidate, social_accounts[candidate])
            print(f"✓ Candidato agregado: {candidate}")
    
    # Realizar análisis completo de redes sociales
    print("\nAnalizando redes sociales de todos los candidatos...")
    social_media_results = social_analyzer.analyze_all_candidates(days_back=30)
    
    # Mostrar resultados principales
    print("✓ Análisis de redes sociales completado:")
    for candidate, results in social_media_results.items():
        engagement = results.get('engagement_metrics', {})
        sentiment = results.get('overall_sentiment', {})
        influence = results.get('influence_score', 0)
        
        print(f"   - {candidate}:")
        print(f"     Seguidores: {engagement.get('total_followers', 0):,}")
        print(f"     Score de influencia: {influence:.1f}/100")
        print(f"     Sentimiento positivo: {sentiment.get('positive_percentage', 0):.1f}%")
    
    # Comparar candidatos
    comparison = social_analyzer.compare_candidates()
    print("\n✓ Rankings de redes sociales:")
    print("   Ranking de influencia:")
    for i, (candidate, score) in enumerate(comparison['ranking_influencia'][:3], 1):
        print(f"     {i}. {candidate}: {score:.1f} puntos")
    
    print("   Ranking de sentimiento positivo:")
    for i, (candidate, sentiment) in enumerate(comparison['ranking_sentimiento'][:3], 1):
        print(f"     {i}. {candidate}: {sentiment:.1f}%")
    
    # Predicción basada en redes sociales
    social_prediction = social_analyzer.get_winner_prediction_social_media()
    print(f"\n✓ Predicción basada en redes sociales: {social_prediction.get('prediccion_ganador', 'N/A')}")
    
    # Exportar reporte de redes sociales
    social_analyzer.generate_social_media_report('reporte_redes_sociales.txt')
    print("✓ Reporte de redes sociales exportado: reporte_redes_sociales.txt")
    print()
    
    # ============================================================================
    # 4. PREDICCIÓN DEL POSIBLE GANADOR
    # ============================================================================
    print("4. PREDICCIÓN DEL POSIBLE GANADOR...")
    print("-" * 40)
    
    # Inicializar motor de predicción
    prediction_engine = PredictionEngine()
    
    # Generar predicción completa
    print("Entrenando modelos de predicción...")
    prediction_results = prediction_engine.generate_prediction_report(
        segmented_data, 
        social_media_results,
        'reporte_prediccion_completo.txt'
    )
    
    # Mostrar resultados principales
    ensemble_prediction = prediction_results['ensemble_prediction']
    print("✓ Predicción electoral completada:")
    print(f"   Ganador predicho: {ensemble_prediction.get('predicted_winner', 'N/A')}")
    print(f"   Nivel de confianza: {ensemble_prediction.get('confidence_level', 0):.1%}")
    print(f"   Margen de victoria: {ensemble_prediction.get('margin_of_victory', 0):.1%}")
    
    print("\n   Ranking final de candidatos:")
    for i, (candidate, share) in enumerate(ensemble_prediction.get('ranking', []), 1):
        print(f"     {i}. {candidate}: {share:.1%} de apoyo predicho")
    
    # Mostrar factores clave
    key_factors = prediction_results['key_factors']
    print(f"\n✓ Factor más influyente: {key_factors.get('most_important_factor', 'N/A')}")
    
    print("✓ Reporte de predicción completo exportado: reporte_prediccion_completo.txt")
    print()
    
    # ============================================================================
    # 5. RESUMEN EJECUTIVO
    # ============================================================================
    print("5. RESUMEN EJECUTIVO")
    print("-" * 25)
    
    # Generar resumen ejecutivo
    generate_executive_summary(
        segmented_data, 
        social_media_results, 
        prediction_results,
        'resumen_ejecutivo.txt'
    )
    
    print("✓ Resumen ejecutivo generado: resumen_ejecutivo.txt")
    print()
    print("=" * 60)
    print("ANÁLISIS ELECTORAL COMPLETADO EXITOSAMENTE")
    print("=" * 60)
    print()
    print("Archivos generados:")
    print("- reporte_segmentacion.txt: Análisis demográfico detallado")
    print("- reporte_redes_sociales.txt: Análisis de redes sociales")
    print("- reporte_prediccion_completo.txt: Predicción electoral detallada")
    print("- resumen_ejecutivo.txt: Resumen ejecutivo con conclusiones")

def generate_executive_summary(segmented_data, social_media_results, prediction_results, file_path):
    """Generar resumen ejecutivo del análisis"""
    
    ensemble_prediction = prediction_results['ensemble_prediction']
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("RESUMEN EJECUTIVO - ANÁLISIS ELECTORAL\n")
        f.write("=" * 50 + "\n\n")
        
        f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Datos analizados: {len(segmented_data)} registros de votantes\n\n")
        
        # Predicción principal
        f.write("PREDICCIÓN PRINCIPAL\n")
        f.write("-" * 20 + "\n")
        f.write(f"Ganador predicho: {ensemble_prediction.get('predicted_winner', 'N/A')}\n")
        f.write(f"Nivel de confianza: {ensemble_prediction.get('confidence_level', 0):.1%}\n")
        f.write(f"Margen de victoria: {ensemble_prediction.get('margin_of_victoria', 0):.1%}\n\n")
        
        # Ranking de candidatos
        f.write("RANKING DE CANDIDATOS\n")
        f.write("-" * 25 + "\n")
        for i, (candidate, share) in enumerate(ensemble_prediction.get('ranking', []), 1):
            f.write(f"{i}. {candidate}: {share:.1%}\n")
        f.write("\n")
        
        # Análisis de segmentos
        f.write("SEGMENTOS DEMOGRÁFICOS CLAVE\n")
        f.write("-" * 35 + "\n")
        segments = segmented_data['segment'].unique()
        f.write(f"Se identificaron {len(segments)} segmentos demográficos distintos\n")
        f.write("Cada segmento muestra patrones de voto diferenciados\n\n")
        
        # Redes sociales
        f.write("ANÁLISIS DE REDES SOCIALES\n")
        f.write("-" * 30 + "\n")
        if social_media_results:
            # Encontrar líder en redes sociales
            max_influence = 0
            social_leader = None
            for candidate, data in social_media_results.items():
                influence = data.get('influence_score', 0)
                if influence > max_influence:
                    max_influence = influence
                    social_leader = candidate
            
            f.write(f"Líder en redes sociales: {social_leader} ({max_influence:.1f} puntos)\n")
            f.write("Análisis incluye Twitter, Facebook y análisis de sentimiento\n\n")
        
        # Metodología
        f.write("METODOLOGÍA\n")
        f.write("-" * 15 + "\n")
        f.write("1. Segmentación demográfica usando clustering K-means\n")
        f.write("2. Análisis de redes sociales (Twitter, Facebook)\n")
        f.write("3. Análisis de sentimiento en contenido\n")
        f.write("4. Modelos de machine learning (Random Forest, Gradient Boosting, Regresión Logística)\n")
        f.write("5. Predicción ensemble combinando múltiples modelos\n\n")
        
        # Limitaciones
        f.write("LIMITACIONES\n")
        f.write("-" * 15 + "\n")
        f.write("- Basado en datos simulados para demostración\n")
        f.write("- Predicción sujeta a cambios en el tiempo\n")
        f.write("- Factores externos no considerados\n")
        f.write("- Margen de error inherente a modelos predictivos\n")

if __name__ == "__main__":
    main()
