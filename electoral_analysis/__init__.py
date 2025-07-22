"""
Sistema de Análisis Electoral
============================

Un sistema completo para el análisis del comportamiento electoral, 
segmentación de votantes, análisis de redes sociales y predicción de resultados.

Módulos:
- data: Gestión y procesamiento de datos electorales
- models: Modelos de predicción y análisis
- social_media: Análisis de redes sociales de candidatos
- visualization: Visualización de datos y resultados
- utils: Utilidades y funciones auxiliares
"""

__version__ = "1.0.0"
__author__ = "Electoral Analysis Team"

from .data import DataManager
from .models import PredictionEngine
from .social_media import SocialMediaAnalyzer
from .visualization import ElectoralVisualizer

__all__ = [
    'DataManager',
    'PredictionEngine', 
    'SocialMediaAnalyzer',
    'ElectoralVisualizer'
]
