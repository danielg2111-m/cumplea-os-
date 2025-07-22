import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
import pickle

class DataProcessor:
    def __init__(self):
        self.data_storage = "data/surveys/"
        self.ensure_storage_directory()
    
    def ensure_storage_directory(self):
        """Crear directorio de almacenamiento si no existe"""
        os.makedirs(self.data_storage, exist_ok=True)
    
    def process_survey_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Procesar y limpiar datos de encuesta"""
        # Crear copia para no modificar original
        processed_df = df.copy()
        
        # Limpiar nombres de columnas
        processed_df.columns = [self.clean_column_name(col) for col in processed_df.columns]
        
        # Detectar y convertir tipos de datos
        processed_df = self.detect_and_convert_types(processed_df)
        
        # Limpiar datos faltantes
        processed_df = self.handle_missing_data(processed_df)
        
        # Normalizar datos de texto
        text_columns = self.get_text_columns(processed_df)
        for col in text_columns:
            processed_df[col] = processed_df[col].astype(str).str.strip()
        
        return processed_df
    
    def clean_column_name(self, column_name: str) -> str:
        """Limpiar nombres de columnas"""
        # Remover caracteres especiales y espacios
        clean_name = str(column_name).strip()
        clean_name = clean_name.replace(' ', '_').replace('-', '_')
        clean_name = ''.join(c for c in clean_name if c.isalnum() or c == '_')
        return clean_name.lower()
    
    def detect_and_convert_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Detectar y convertir tipos de datos automáticamente"""
        for column in df.columns:
            # Intentar convertir a numérico
            if df[column].dtype == 'object':
                # Verificar si es numérico
                numeric_series = pd.to_numeric(df[column], errors='coerce')
                if not numeric_series.isna().all():
                    non_null_ratio = numeric_series.notna().sum() / len(df)
                    if non_null_ratio > 0.7:  # Si 70% son numéricos
                        df[column] = numeric_series
                        continue
                
                # Verificar si es fecha
                try:
                    date_series = pd.to_datetime(df[column], errors='coerce')
                    if not date_series.isna().all():
                        non_null_ratio = date_series.notna().sum() / len(df)
                        if non_null_ratio > 0.7:
                            df[column] = date_series
                            continue
                except:
                    pass
                
                # Verificar si es categórico
                unique_ratio = df[column].nunique() / len(df)
                if unique_ratio < 0.5:  # Si menos del 50% son únicos
                    df[column] = df[column].astype('category')
        
        return df
    
    def handle_missing_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Manejar datos faltantes"""
        # Para columnas numéricas, usar mediana
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            if df[col].isna().any():
                df[col].fillna(df[col].median(), inplace=True)
        
        # Para columnas categóricas, usar moda
        categorical_columns = df.select_dtypes(include=['category', 'object']).columns
        for col in categorical_columns:
            if df[col].isna().any():
                mode_value = df[col].mode()
                if len(mode_value) > 0:
                    df[col].fillna(mode_value[0], inplace=True)
                else:
                    df[col].fillna('No especificado', inplace=True)
        
        return df
    
    def analyze_data_types(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analizar tipos de datos y estadísticas básicas"""
        analysis = {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "column_types": {},
            "missing_data": {},
            "summary_stats": {}
        }
        
        for column in df.columns:
            dtype = str(df[column].dtype)
            analysis["column_types"][column] = dtype
            
            # Datos faltantes
            missing_count = df[column].isna().sum()
            missing_percentage = (missing_count / len(df)) * 100
            analysis["missing_data"][column] = {
                "count": int(missing_count),
                "percentage": round(missing_percentage, 2)
            }
            
            # Estadísticas según tipo
            if df[column].dtype in ['int64', 'float64']:
                analysis["summary_stats"][column] = {
                    "mean": float(df[column].mean()),
                    "median": float(df[column].median()),
                    "std": float(df[column].std()),
                    "min": float(df[column].min()),
                    "max": float(df[column].max())
                }
            elif df[column].dtype in ['object', 'category']:
                value_counts = df[column].value_counts().head(5)
                analysis["summary_stats"][column] = {
                    "unique_values": int(df[column].nunique()),
                    "most_common": value_counts.to_dict()
                }
        
        return analysis
    
    def get_text_columns(self, df: pd.DataFrame) -> List[str]:
        """Identificar columnas de texto"""
        text_columns = []
        
        for column in df.columns:
            if df[column].dtype == 'object':
                # Verificar si contiene texto largo (más de 10 caracteres promedio)
                avg_length = df[column].astype(str).str.len().mean()
                if avg_length > 10:
                    text_columns.append(column)
        
        return text_columns
    
    def descriptive_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Realizar análisis descriptivo completo"""
        analysis = {
            "basic_info": self.analyze_data_types(df),
            "distributions": {},
            "correlations": {},
            "outliers": {}
        }
        
        # Análisis de distribuciones
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            analysis["distributions"][col] = {
                "histogram_data": df[col].value_counts().sort_index().to_dict(),
                "quartiles": {
                    "Q1": float(df[col].quantile(0.25)),
                    "Q2": float(df[col].quantile(0.5)),
                    "Q3": float(df[col].quantile(0.75))
                }
            }
        
        # Análisis de correlaciones
        if len(numeric_columns) > 1:
            corr_matrix = df[numeric_columns].corr()
            analysis["correlations"] = corr_matrix.to_dict()
        
        # Detección de outliers
        for col in numeric_columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            analysis["outliers"][col] = {
                "count": len(outliers),
                "percentage": (len(outliers) / len(df)) * 100
            }
        
        return analysis
    
    def perform_clustering(self, df: pd.DataFrame, n_clusters: int = 3) -> Dict[str, Any]:
        """Realizar análisis de clustering"""
        # Preparar datos para clustering
        numeric_df = df.select_dtypes(include=[np.number])
        
        if len(numeric_df.columns) < 2:
            return {"error": "Insuficientes columnas numéricas para clustering"}
        
        # Normalizar datos
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(numeric_df.fillna(numeric_df.mean()))
        
        # Aplicar K-means
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(scaled_data)
        
        # Análisis de clusters
        cluster_analysis = {
            "cluster_labels": clusters.tolist(),
            "cluster_centers": kmeans.cluster_centers_.tolist(),
            "cluster_sizes": pd.Series(clusters).value_counts().to_dict(),
            "inertia": float(kmeans.inertia_)
        }
        
        # Estadísticas por cluster
        df_with_clusters = df.copy()
        df_with_clusters['cluster'] = clusters
        
        cluster_stats = {}
        for cluster_id in range(n_clusters):
            cluster_data = df_with_clusters[df_with_clusters['cluster'] == cluster_id]
            cluster_stats[f"cluster_{cluster_id}"] = {
                "size": len(cluster_data),
                "percentage": (len(cluster_data) / len(df)) * 100,
                "numeric_means": cluster_data.select_dtypes(include=[np.number]).mean().to_dict()
            }
        
        cluster_analysis["cluster_statistics"] = cluster_stats
        
        # PCA para visualización
        if len(numeric_df.columns) > 2:
            pca = PCA(n_components=2)
            pca_data = pca.fit_transform(scaled_data)
            cluster_analysis["pca_visualization"] = {
                "coordinates": pca_data.tolist(),
                "explained_variance": pca.explained_variance_ratio_.tolist()
            }
        
        return cluster_analysis
    
    def correlation_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Análisis detallado de correlaciones"""
        numeric_df = df.select_dtypes(include=[np.number])
        
        if len(numeric_df.columns) < 2:
            return {"error": "Insuficientes columnas numéricas para análisis de correlación"}
        
        # Matriz de correlación
        corr_matrix = numeric_df.corr()
        
        # Encontrar correlaciones fuertes
        strong_correlations = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) > 0.5:  # Correlación fuerte
                    strong_correlations.append({
                        "variable1": corr_matrix.columns[i],
                        "variable2": corr_matrix.columns[j],
                        "correlation": float(corr_value),
                        "strength": "fuerte" if abs(corr_value) > 0.7 else "moderada"
                    })
        
        return {
            "correlation_matrix": corr_matrix.to_dict(),
            "strong_correlations": strong_correlations,
            "heatmap_data": corr_matrix.values.tolist(),
            "column_names": corr_matrix.columns.tolist()
        }
    
    def detect_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Detectar patrones en los datos"""
        patterns = {
            "response_patterns": {},
            "temporal_patterns": {},
            "categorical_patterns": {}
        }
        
        # Patrones de respuesta
        for column in df.columns:
            if df[column].dtype in ['object', 'category']:
                value_counts = df[column].value_counts()
                patterns["response_patterns"][column] = {
                    "most_common": value_counts.head(3).to_dict(),
                    "diversity_index": float(value_counts.nunique() / len(df))
                }
        
        # Patrones temporales (si hay columnas de fecha)
        date_columns = df.select_dtypes(include=['datetime64']).columns
        for col in date_columns:
            df[col] = pd.to_datetime(df[col])
            patterns["temporal_patterns"][col] = {
                "date_range": {
                    "start": df[col].min().isoformat(),
                    "end": df[col].max().isoformat()
                },
                "frequency_by_month": df[col].dt.month.value_counts().to_dict()
            }
        
        return patterns
    
    def generate_summary(self, analysis_results: Dict[str, Any]) -> str:
        """Generar resumen del análisis"""
        summary_parts = []
        
        if "descriptive" in analysis_results:
            basic_info = analysis_results["descriptive"]["basic_info"]
            summary_parts.append(
                f"Encuesta con {basic_info['total_rows']} respuestas y {basic_info['total_columns']} preguntas."
            )
        
        if "sentiment" in analysis_results:
            sentiment_info = analysis_results["sentiment"]["overall_sentiment"]
            if sentiment_info:
                dominant = sentiment_info.get("dominant_sentiment", "neutral")
                summary_parts.append(f"Sentimiento general: {dominant}")
        
        if "clustering" in analysis_results:
            clustering_info = analysis_results["clustering"]
            if "cluster_sizes" in clustering_info:
                n_clusters = len(clustering_info["cluster_sizes"])
                summary_parts.append(f"Se identificaron {n_clusters} grupos de respuestas.")
        
        return " ".join(summary_parts) if summary_parts else "Análisis completado."
    
    def save_survey_data(self, survey_id: str, df: pd.DataFrame):
        """Guardar datos de encuesta"""
        filepath = os.path.join(self.data_storage, f"{survey_id}.pkl")
        with open(filepath, 'wb') as f:
            pickle.dump(df, f)
    
    def load_survey_data(self, survey_id: str) -> Optional[pd.DataFrame]:
        """Cargar datos de encuesta"""
        filepath = os.path.join(self.data_storage, f"{survey_id}.pkl")
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                return pickle.load(f)
        return None
    
    def list_surveys(self) -> List[Dict[str, Any]]:
        """Listar todas las encuestas guardadas"""
        surveys = []
        for filename in os.listdir(self.data_storage):
            if filename.endswith('.pkl'):
                survey_id = filename[:-4]
                filepath = os.path.join(self.data_storage, filename)
                stat = os.stat(filepath)
                surveys.append({
                    "survey_id": survey_id,
                    "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    "size": stat.st_size
                })
        return surveys
    
    def delete_survey(self, survey_id: str) -> bool:
        """Eliminar encuesta"""
        filepath = os.path.join(self.data_storage, f"{survey_id}.pkl")
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
