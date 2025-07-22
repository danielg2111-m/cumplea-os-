"""
Segmentación Demográfica de Votantes
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from typing import Dict, List, Tuple, Optional
import matplotlib.pyplot as plt
import seaborn as sns

class DemographicSegmentation:
    """
    Clase para realizar segmentación demográfica de votantes
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.kmeans_model = None
        self.segment_profiles = {}
    
    def prepare_data_for_clustering(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Preparar datos para clustering
        """
        # Seleccionar columnas relevantes para segmentación
        clustering_columns = [
            'age', 'gender', 'education', 'income_level', 
            'political_interest', 'social_media_activity'
        ]
        
        # Filtrar columnas que existen en el DataFrame
        available_columns = [col for col in clustering_columns if col in df.columns]
        clustering_data = df[available_columns].copy()
        
        # Codificar variables categóricas
        categorical_columns = ['gender', 'education', 'income_level']
        for col in categorical_columns:
            if col in clustering_data.columns:
                le = LabelEncoder()
                clustering_data[col + '_encoded'] = le.fit_transform(clustering_data[col])
                self.label_encoders[col] = le
                clustering_data.drop(col, axis=1, inplace=True)
        
        # Normalizar datos numéricos
        numerical_data = self.scaler.fit_transform(clustering_data)
        
        return pd.DataFrame(numerical_data, columns=clustering_data.columns, index=clustering_data.index)
    
    def perform_segmentation(self, df: pd.DataFrame, n_segments: int = 5) -> pd.DataFrame:
        """
        Realizar segmentación de votantes usando K-means
        """
        # Preparar datos
        clustering_data = self.prepare_data_for_clustering(df)
        
        # Aplicar K-means
        self.kmeans_model = KMeans(n_clusters=n_segments, random_state=42)
        segments = self.kmeans_model.fit_predict(clustering_data)
        
        # Agregar segmentos al DataFrame original
        df_segmented = df.copy()
        df_segmented['segment'] = segments
        
        # Crear perfiles de segmentos
        self.segment_profiles = self._create_segment_profiles(df_segmented)
        
        return df_segmented
    
    def _create_segment_profiles(self, df: pd.DataFrame) -> Dict:
        """
        Crear perfiles detallados de cada segmento
        """
        profiles = {}
        
        for segment in df['segment'].unique():
            segment_data = df[df['segment'] == segment]
            
            profile = {
                'size': len(segment_data),
                'percentage': len(segment_data) / len(df) * 100,
                'demographics': {
                    'avg_age': segment_data['age'].mean(),
                    'gender_distribution': segment_data['gender'].value_counts(normalize=True).to_dict(),
                    'education_distribution': segment_data['education'].value_counts(normalize=True).to_dict(),
                    'income_distribution': segment_data['income_level'].value_counts(normalize=True).to_dict(),
                    'avg_political_interest': segment_data['political_interest'].mean(),
                    'avg_social_media_activity': segment_data['social_media_activity'].mean()
                },
                'voting_behavior': {
                    'candidate_preferences': segment_data['preferred_candidate'].value_counts(normalize=True).to_dict(),
                    'avg_voting_intention': segment_data['voting_intention'].mean()
                }
            }
            
            profiles[f'Segmento_{segment}'] = profile
        
        return profiles
    
    def get_segment_characteristics(self) -> Dict:
        """
        Obtener características principales de cada segmento
        """
        if not self.segment_profiles:
            return {}
        
        characteristics = {}
        
        for segment_name, profile in self.segment_profiles.items():
            # Determinar características principales
            dominant_gender = max(profile['demographics']['gender_distribution'], 
                                key=profile['demographics']['gender_distribution'].get)
            dominant_education = max(profile['demographics']['education_distribution'],
                                   key=profile['demographics']['education_distribution'].get)
            dominant_income = max(profile['demographics']['income_distribution'],
                                key=profile['demographics']['income_distribution'].get)
            preferred_candidate = max(profile['voting_behavior']['candidate_preferences'],
                                    key=profile['voting_behavior']['candidate_preferences'].get)
            
            characteristics[segment_name] = {
                'descripcion': self._generate_segment_description(profile),
                'tamaño': f"{profile['size']} votantes ({profile['percentage']:.1f}%)",
                'edad_promedio': f"{profile['demographics']['avg_age']:.1f} años",
                'genero_dominante': dominant_gender,
                'educacion_dominante': dominant_education,
                'nivel_ingresos_dominante': dominant_income,
                'candidato_preferido': preferred_candidate,
                'intencion_voto_promedio': f"{profile['voting_behavior']['avg_voting_intention']:.2f}",
                'interes_politico': f"{profile['demographics']['avg_political_interest']:.1f}/10",
                'actividad_redes_sociales': f"{profile['demographics']['avg_social_media_activity']:.2f}"
            }
        
        return characteristics
    
    def _generate_segment_description(self, profile: Dict) -> str:
        """
        Generar descripción textual del segmento
        """
        avg_age = profile['demographics']['avg_age']
        political_interest = profile['demographics']['avg_political_interest']
        social_media = profile['demographics']['avg_social_media_activity']
        
        # Clasificar por edad
        if avg_age < 30:
            age_group = "jóvenes"
        elif avg_age < 50:
            age_group = "adultos de mediana edad"
        else:
            age_group = "adultos mayores"
        
        # Clasificar por interés político
        if political_interest < 4:
            political_level = "bajo interés político"
        elif political_interest < 7:
            political_level = "interés político moderado"
        else:
            political_level = "alto interés político"
        
        # Clasificar por actividad en redes sociales
        if social_media < 0.3:
            social_level = "baja actividad en redes sociales"
        elif social_media < 0.7:
            social_level = "actividad moderada en redes sociales"
        else:
            social_level = "alta actividad en redes sociales"
        
        return f"Segmento de {age_group} con {political_level} y {social_level}"
    
    def analyze_segment_voting_patterns(self, df: pd.DataFrame) -> Dict:
        """
        Analizar patrones de voto por segmento
        """
        if 'segment' not in df.columns:
            return {}
        
        patterns = {}
        
        for segment in df['segment'].unique():
            segment_data = df[df['segment'] == segment]
            
            # Análisis de preferencias por candidato
            candidate_prefs = segment_data['preferred_candidate'].value_counts(normalize=True)
            
            # Análisis de intención de voto
            avg_intention = segment_data['voting_intention'].mean()
            
            # Análisis por región
            regional_distribution = segment_data['region'].value_counts(normalize=True)
            
            patterns[f'Segmento_{segment}'] = {
                'preferencias_candidatos': candidate_prefs.to_dict(),
                'intencion_voto_promedio': avg_intention,
                'distribucion_regional': regional_distribution.to_dict(),
                'volatilidad': segment_data['voting_intention'].std()
            }
        
        return patterns
    
    def predict_segment_turnout(self, df: pd.DataFrame) -> Dict:
        """
        Predecir participación electoral por segmento
        """
        if 'segment' not in df.columns:
            return {}
        
        turnout_predictions = {}
        
        for segment in df['segment'].unique():
            segment_data = df[df['segment'] == segment]
            
            # Factores que influyen en la participación
            political_interest = segment_data['political_interest'].mean()
            social_media_activity = segment_data['social_media_activity'].mean()
            voting_intention = segment_data['voting_intention'].mean()
            
            # Modelo simple de predicción de participación
            # Basado en interés político, actividad en redes sociales e intención de voto
            predicted_turnout = (
                political_interest * 0.4 + 
                social_media_activity * 10 * 0.3 + 
                voting_intention * 10 * 0.3
            ) / 10
            
            # Normalizar entre 0 y 1
            predicted_turnout = min(max(predicted_turnout, 0), 1)
            
            turnout_predictions[f'Segmento_{segment}'] = {
                'participacion_estimada': predicted_turnout,
                'factores': {
                    'interes_politico': political_interest,
                    'actividad_redes_sociales': social_media_activity,
                    'intencion_voto': voting_intention
                }
            }
        
        return turnout_predictions
    
    def export_segmentation_report(self, df: pd.DataFrame, file_path: str = 'segmentation_report.txt'):
        """
        Exportar reporte completo de segmentación
        """
        if 'segment' not in df.columns:
            print("Error: No se ha realizado segmentación")
            return
        
        characteristics = self.get_segment_characteristics()
        voting_patterns = self.analyze_segment_voting_patterns(df)
        turnout_predictions = self.predict_segment_turnout(df)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("REPORTE DE SEGMENTACIÓN DEMOGRÁFICA\n")
            f.write("=" * 50 + "\n\n")
            
            for segment_name in characteristics.keys():
                f.write(f"{segment_name.upper()}\n")
                f.write("-" * 30 + "\n")
                
                char = characteristics[segment_name]
                f.write(f"Descripción: {char['descripcion']}\n")
                f.write(f"Tamaño: {char['tamaño']}\n")
                f.write(f"Edad promedio: {char['edad_promedio']}\n")
                f.write(f"Candidato preferido: {char['candidato_preferido']}\n")
                f.write(f"Intención de voto: {char['intencion_voto_promedio']}\n")
                f.write(f"Interés político: {char['interes_politico']}\n")
                
                if segment_name in turnout_predictions:
                    turnout = turnout_predictions[segment_name]['participacion_estimada']
                    f.write(f"Participación estimada: {turnout:.1%}\n")
                
                f.write("\n")
        
        print(f"Reporte exportado a: {file_path}")
