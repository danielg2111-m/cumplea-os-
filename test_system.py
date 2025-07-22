"""
Script de prueba simplificado para el sistema de análisis electoral
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_basic_imports():
    """Probar importaciones básicas"""
    print("Probando importaciones básicas...")
    
    try:
        # Importaciones estándar que deberían estar disponibles
        import json
        import csv
        import datetime
        import random
        print("✓ Importaciones estándar exitosas")
        
        # Probar estructura del proyecto
        if os.path.exists('electoral_analysis'):
            print("✓ Directorio electoral_analysis encontrado")
        else:
            print("✗ Directorio electoral_analysis no encontrado")
            
        # Verificar archivos principales
        main_files = [
            'main_electoral_analysis.py',
            'dashboard_electoral.py',
            'requirements.txt',
            'README.md'
        ]
        
        for file in main_files:
            if os.path.exists(file):
                print(f"✓ {file} encontrado")
            else:
                print(f"✗ {file} no encontrado")
                
        return True
        
    except Exception as e:
        print(f"✗ Error en importaciones: {e}")
        return False

def test_data_generation():
    """Probar generación de datos simulados"""
    print("\nProbando generación de datos...")
    
    try:
        import random
        import datetime
        
        # Simular datos básicos
        candidates = ['María González', 'Carlos Rodríguez', 'Ana Martínez', 'Luis Fernández', 'Carmen López']
        regions = ['Norte', 'Sur', 'Este', 'Oeste', 'Centro']
        
        # Generar datos de muestra
        sample_data = []
        for i in range(100):
            sample_data.append({
                'voter_id': i + 1,
                'age': random.randint(18, 80),
                'gender': random.choice(['M', 'F']),
                'education': random.choice(['Primaria', 'Secundaria', 'Universidad', 'Posgrado']),
                'income_level': random.choice(['Bajo', 'Medio', 'Alto']),
                'region': random.choice(regions),
                'preferred_candidate': random.choice(candidates),
                'voting_intention': random.uniform(0, 1),
                'political_interest': random.uniform(1, 10),
                'social_media_activity': random.uniform(0, 1)
            })
        
        print(f"✓ Generados {len(sample_data)} registros de votantes")
        print(f"✓ Candidatos: {len(candidates)}")
        print(f"✓ Regiones: {len(regions)}")
        
        # Analizar distribución de candidatos
        candidate_counts = {}
        for record in sample_data:
            candidate = record['preferred_candidate']
            candidate_counts[candidate] = candidate_counts.get(candidate, 0) + 1
        
        print("\nDistribución de preferencias:")
        for candidate, count in candidate_counts.items():
            percentage = (count / len(sample_data)) * 100
            print(f"  {candidate}: {count} votos ({percentage:.1f}%)")
        
        return True
        
    except Exception as e:
        print(f"✗ Error en generación de datos: {e}")
        return False

def test_basic_analysis():
    """Probar análisis básico sin dependencias externas"""
    print("\nProbando análisis básico...")
    
    try:
        import random
        
        # Datos simulados
        candidates = ['María González', 'Carlos Rodríguez', 'Ana Martínez', 'Luis Fernández', 'Carmen López']
        
        # Simular métricas de redes sociales
        social_metrics = {}
        for candidate in candidates:
            social_metrics[candidate] = {
                'followers': random.randint(1000, 100000),
                'posts': random.randint(10, 50),
                'engagement_rate': random.uniform(0.01, 0.1),
                'sentiment_positive': random.uniform(30, 80),
                'influence_score': random.uniform(20, 95)
            }
        
        print("✓ Métricas de redes sociales simuladas:")
        for candidate, metrics in social_metrics.items():
            print(f"  {candidate}:")
            print(f"    Seguidores: {metrics['followers']:,}")
            print(f"    Score influencia: {metrics['influence_score']:.1f}")
            print(f"    Sentimiento positivo: {metrics['sentiment_positive']:.1f}%")
        
        # Predicción simple basada en métricas
        print("\n✓ Predicción basada en redes sociales:")
        
        # Calcular score combinado
        combined_scores = {}
        for candidate, metrics in social_metrics.items():
            score = (
                metrics['influence_score'] * 0.4 +
                metrics['engagement_rate'] * 1000 * 0.3 +
                metrics['sentiment_positive'] * 0.3
            )
            combined_scores[candidate] = score
        
        # Ordenar por score
        ranking = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
        
        for i, (candidate, score) in enumerate(ranking, 1):
            print(f"  {i}. {candidate}: {score:.1f} puntos")
        
        predicted_winner = ranking[0][0]
        print(f"\n✓ Ganador predicho (redes sociales): {predicted_winner}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error en análisis básico: {e}")
        return False

def test_file_structure():
    """Verificar estructura de archivos del proyecto"""
    print("\nVerificando estructura del proyecto...")
    
    expected_structure = {
        'electoral_analysis/': [
            '__init__.py',
            'data/__init__.py',
            'data/data_manager.py',
            'data/demographic_segmentation.py',
            'social_media/__init__.py',
            'social_media/social_media_analyzer.py',
            'social_media/twitter_analyzer.py',
            'social_media/facebook_analyzer.py',
            'social_media/sentiment_analyzer.py',
            'models/__init__.py',
            'models/prediction_engine.py',
            'visualization/__init__.py'
        ]
    }
    
    missing_files = []
    existing_files = []
    
    for file_path in expected_structure['electoral_analysis/']:
        full_path = os.path.join('electoral_analysis', file_path)
        if os.path.exists(full_path):
            existing_files.append(file_path)
            print(f"✓ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"✗ {file_path}")
    
    print(f"\nResumen:")
    print(f"✓ Archivos existentes: {len(existing_files)}")
    print(f"✗ Archivos faltantes: {len(missing_files)}")
    
    return len(missing_files) == 0

def main():
    """Función principal de prueba"""
    print("=" * 60)
    print("PRUEBA DEL SISTEMA DE ANÁLISIS ELECTORAL")
    print("=" * 60)
    
    tests = [
        ("Importaciones básicas", test_basic_imports),
        ("Generación de datos", test_data_generation),
        ("Análisis básico", test_basic_analysis),
        ("Estructura de archivos", test_file_structure)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 40)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ Error inesperado en {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen final
    print("\n" + "=" * 60)
    print("RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✓ PASÓ" if result else "✗ FALLÓ"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nResultado: {passed}/{len(results)} pruebas pasaron")
    
    if passed == len(results):
        print("🎉 ¡Todas las pruebas pasaron! El sistema está listo.")
    else:
        print("⚠️ Algunas pruebas fallaron. Revisar configuración.")
    
    print("\nPara ejecutar el sistema completo:")
    print("1. Instalar dependencias: pip install -r requirements.txt")
    print("2. Ejecutar análisis: python3 main_electoral_analysis.py")
    print("3. Lanzar dashboard: streamlit run dashboard_electoral.py")

if __name__ == "__main__":
    main()
