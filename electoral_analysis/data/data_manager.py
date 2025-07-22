"""
Gestor Principal de Datos Electorales
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from typing import Dict, List, Optional, Tuple
import os
from datetime import datetime, timedelta
import logging

class DataManager:
    """
    Clase principal para la gestión de datos electorales
    """
    
    def __init__(self, database_url: Optional[str] = None):
        self.database_url = database_url or os.getenv('DATABASE_URL')
        self.engine = None
        self.logger = self._setup_logger()
        
        if self.database_url:
            try:
                self.engine = create_engine(self.database_url)
                self.logger.info("Conexión a base de datos establecida")
            except Exception as e:
                self.logger.error(f"Error conectando a la base de datos: {e}")
    
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
    
    def load_electoral_data(self, file_path: str = None) -> pd.DataFrame:
        """
        Cargar datos electorales desde archivo o base de datos
        """
        if file_path:
            return self._load_from_file(file_path)
        elif self.engine:
            return self._load_from_database()
        else:
            return self._generate_sample_data()
    
    def _load_from_file(self, file_path: str) -> pd.DataFrame:
        """Cargar datos desde archivo"""
        try:
            if file_path.endswith('.csv'):
                return pd.read_csv(file_path)
            elif file_path.endswith('.xlsx'):
                return pd.read_excel(file_path)
            else:
                raise ValueError("Formato de archivo no soportado")
        except Exception as e:
            self.logger.error(f"Error cargando archivo: {e}")
            return self._generate_sample_data()
    
    def _load_from_database(self) -> pd.DataFrame:
        """Cargar datos desde base de datos"""
        try:
            query = """
            SELECT * FROM electoral_data 
            WHERE election_date >= CURRENT_DATE - INTERVAL '2 years'
            """
            return pd.read_sql(query, self.engine)
        except Exception as e:
            self.logger.error(f"Error cargando desde base de datos: {e}")
            return self._generate_sample_data()
    
    def _generate_sample_data(self) -> pd.DataFrame:
        """Generar datos de muestra para demostración"""
        np.random.seed(42)
        n_records = 10000
        
        # Candidatos ficticios
        candidates = ['María González', 'Carlos Rodríguez', 'Ana Martínez', 'Luis Fernández', 'Carmen López']
        
        # Regiones
        regions = ['Norte', 'Sur', 'Este', 'Oeste', 'Centro']
        
        # Generar datos
        data = {
            'voter_id': range(1, n_records + 1),
            'age': np.random.normal(45, 15, n_records).astype(int),
            'gender': np.random.choice(['M', 'F'], n_records),
            'education': np.random.choice(['Primaria', 'Secundaria', 'Universidad', 'Posgrado'], n_records),
            'income_level': np.random.choice(['Bajo', 'Medio', 'Alto'], n_records),
            'region': np.random.choice(regions, n_records),
            'preferred_candidate': np.random.choice(candidates, n_records),
            'voting_intention': np.random.uniform(0, 1, n_records),
            'political_interest': np.random.uniform(1, 10, n_records),
            'social_media_activity': np.random.uniform(0, 1, n_records),
            'survey_date': pd.date_range(
                start='2024-01-01', 
                end='2024-12-01', 
                periods=n_records
            )
        }
        
        df = pd.DataFrame(data)
        
        # Ajustar edad para valores válidos
        df['age'] = df['age'].clip(18, 80)
        
        self.logger.info(f"Datos de muestra generados: {len(df)} registros")
        return df
    
    def save_data(self, df: pd.DataFrame, table_name: str = 'electoral_data') -> bool:
        """Guardar datos en base de datos"""
        if not self.engine:
            self.logger.warning("No hay conexión a base de datos disponible")
            return False
        
        try:
            df.to_sql(table_name, self.engine, if_exists='replace', index=False)
            self.logger.info(f"Datos guardados en tabla {table_name}")
            return True
        except Exception as e:
            self.logger.error(f"Error guardando datos: {e}")
            return False
    
    def get_candidate_list(self, df: pd.DataFrame) -> List[str]:
        """Obtener lista de candidatos únicos"""
        return df['preferred_candidate'].unique().tolist()
    
    def get_demographic_summary(self, df: pd.DataFrame) -> Dict:
        """Obtener resumen demográfico"""
        summary = {
            'total_voters': len(df),
            'age_distribution': df['age'].describe().to_dict(),
            'gender_distribution': df['gender'].value_counts(normalize=True).to_dict(),
            'education_distribution': df['education'].value_counts(normalize=True).to_dict(),
            'income_distribution': df['income_level'].value_counts(normalize=True).to_dict(),
            'regional_distribution': df['region'].value_counts(normalize=True).to_dict()
        }
        return summary
    
    def filter_data(self, df: pd.DataFrame, filters: Dict) -> pd.DataFrame:
        """Aplicar filtros a los datos"""
        filtered_df = df.copy()
        
        for column, value in filters.items():
            if column in filtered_df.columns:
                if isinstance(value, list):
                    filtered_df = filtered_df[filtered_df[column].isin(value)]
                else:
                    filtered_df = filtered_df[filtered_df[column] == value]
        
        return filtered_df
    
    def export_data(self, df: pd.DataFrame, file_path: str, format: str = 'csv') -> bool:
        """Exportar datos a archivo"""
        try:
            if format.lower() == 'csv':
                df.to_csv(file_path, index=False)
            elif format.lower() == 'excel':
                df.to_excel(file_path, index=False)
            else:
                raise ValueError("Formato no soportado")
            
            self.logger.info(f"Datos exportados a {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error exportando datos: {e}")
            return False
