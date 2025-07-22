"""
Módulo de Gestión de Datos Electorales
"""

from .data_manager import DataManager
from .electoral_data import ElectoralDataProcessor
from .demographic_segmentation import DemographicSegmentation

__all__ = ['DataManager', 'ElectoralDataProcessor', 'DemographicSegmentation']
