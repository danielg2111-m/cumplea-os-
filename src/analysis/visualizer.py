import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Dict, List, Any
import json
from wordcloud import WordCloud
import base64
import io
import matplotlib.pyplot as plt

class Visualizer:
    def __init__(self):
        self.chart_types = [
            "bar", "pie", "histogram", "scatter", "line", 
            "box", "heatmap", "wordcloud", "cluster"
        ]
    
    def create_visualizations(self, df: pd.DataFrame, requested_charts: List[str] = None) -> Dict[str, Any]:
        """Crear visualizaciones automáticas de los datos"""
        if requested_charts is None or "all" in requested_charts:
            requested_charts = self.chart_types
        
        visualizations = {}
        
        # Análisis automático de columnas
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
        text_columns = [col for col in categorical_columns if df[col].astype(str).str.len().mean() > 20]
        
        # Gráficos de barras para variables categóricas
        if "bar" in requested_charts and categorical_columns:
            visualizations["bar_charts"] = self.create_bar_charts(df, categorical_columns)
        
        # Gráficos de pastel
        if "pie" in requested_charts and categorical_columns:
            visualizations["pie_charts"] = self.create_pie_charts(df, categorical_columns)
        
        # Histogramas para variables numéricas
        if "histogram" in requested_charts and numeric_columns:
            visualizations["histograms"] = self.create_histograms(df, numeric_columns)
        
        # Gráficos de dispersión
        if "scatter" in requested_charts and len(numeric_columns) >= 2:
            visualizations["scatter_plots"] = self.create_scatter_plots(df, numeric_columns)
        
        # Box plots
        if "box" in requested_charts and numeric_columns:
            visualizations["box_plots"] = self.create_box_plots(df, numeric_columns)
        
        # Mapa de calor de correlaciones
        if "heatmap" in requested_charts and len(numeric_columns) >= 2:
            visualizations["correlation_heatmap"] = self.create_correlation_heatmap(df, numeric_columns)
        
        # Nube de palabras
        if "wordcloud" in requested_charts and text_columns:
            visualizations["wordclouds"] = self.create_wordclouds(df, text_columns)
        
        return visualizations
    
    def create_bar_charts(self, df: pd.DataFrame, categorical_columns: List[str]) -> List[Dict[str, Any]]:
        """Crear gráficos de barras para variables categóricas"""
        bar_charts = []
        
        for column in categorical_columns[:5]:  # Limitar a 5 gráficos
            value_counts = df[column].value_counts().head(10)
            
            fig = go.Figure(data=[
                go.Bar(
                    x=value_counts.index.tolist(),
                    y=value_counts.values.tolist(),
                    marker_color='lightblue'
                )
            ])
            
            fig.update_layout(
                title=f'Distribución de {column}',
                xaxis_title=column,
                yaxis_title='Frecuencia',
                template='plotly_white'
            )
            
            bar_charts.append({
                "title": f"Distribución de {column}",
                "chart_data": fig.to_json(),
                "type": "bar",
                "column": column
            })
        
        return bar_charts
    
    def create_pie_charts(self, df: pd.DataFrame, categorical_columns: List[str]) -> List[Dict[str, Any]]:
        """Crear gráficos de pastel"""
        pie_charts = []
        
        for column in categorical_columns[:3]:  # Limitar a 3 gráficos
            value_counts = df[column].value_counts().head(8)
            
            fig = go.Figure(data=[
                go.Pie(
                    labels=value_counts.index.tolist(),
                    values=value_counts.values.tolist(),
                    hole=0.3
                )
            ])
            
            fig.update_layout(
                title=f'Proporción de {column}',
                template='plotly_white'
            )
            
            pie_charts.append({
                "title": f"Proporción de {column}",
                "chart_data": fig.to_json(),
                "type": "pie",
                "column": column
            })
        
        return pie_charts
    
    def create_histograms(self, df: pd.DataFrame, numeric_columns: List[str]) -> List[Dict[str, Any]]:
        """Crear histogramas para variables numéricas"""
        histograms = []
        
        for column in numeric_columns:
            fig = go.Figure(data=[
                go.Histogram(
                    x=df[column].dropna(),
                    nbinsx=20,
                    marker_color='lightgreen'
                )
            ])
            
            fig.update_layout(
                title=f'Distribución de {column}',
                xaxis_title=column,
                yaxis_title='Frecuencia',
                template='plotly_white'
            )
            
            histograms.append({
                "title": f"Distribución de {column}",
                "chart_data": fig.to_json(),
                "type": "histogram",
                "column": column
            })
        
        return histograms
    
    def create_scatter_plots(self, df: pd.DataFrame, numeric_columns: List[str]) -> List[Dict[str, Any]]:
        """Crear gráficos de dispersión"""
        scatter_plots = []
        
        # Crear combinaciones de pares de variables
        for i in range(len(numeric_columns)):
            for j in range(i+1, min(i+3, len(numeric_columns))):  # Limitar combinaciones
                col1, col2 = numeric_columns[i], numeric_columns[j]
                
                fig = go.Figure(data=[
                    go.Scatter(
                        x=df[col1],
                        y=df[col2],
                        mode='markers',
                        marker=dict(
                            size=8,
                            color='lightcoral',
                            opacity=0.6
                        )
                    )
                ])
                
                fig.update_layout(
                    title=f'{col1} vs {col2}',
                    xaxis_title=col1,
                    yaxis_title=col2,
                    template='plotly_white'
                )
                
                scatter_plots.append({
                    "title": f"{col1} vs {col2}",
                    "chart_data": fig.to_json(),
                    "type": "scatter",
                    "columns": [col1, col2]
                })
        
        return scatter_plots
    
    def create_box_plots(self, df: pd.DataFrame, numeric_columns: List[str]) -> List[Dict[str, Any]]:
        """Crear box plots"""
        box_plots = []
        
        for column in numeric_columns:
            fig = go.Figure(data=[
                go.Box(
                    y=df[column].dropna(),
                    name=column,
                    marker_color='lightblue'
                )
            ])
            
            fig.update_layout(
                title=f'Box Plot de {column}',
                yaxis_title=column,
                template='plotly_white'
            )
            
            box_plots.append({
                "title": f"Box Plot de {column}",
                "chart_data": fig.to_json(),
                "type": "box",
                "column": column
            })
        
        return box_plots
    
    def create_correlation_heatmap(self, df: pd.DataFrame, numeric_columns: List[str]) -> Dict[str, Any]:
        """Crear mapa de calor de correlaciones"""
        corr_matrix = df[numeric_columns].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns.tolist(),
            y=corr_matrix.columns.tolist(),
            colorscale='RdBu',
            zmid=0,
            text=np.round(corr_matrix.values, 2),
            texttemplate="%{text}",
            textfont={"size": 10}
        ))
        
        fig.update_layout(
            title='Mapa de Correlaciones',
            template='plotly_white',
            width=600,
            height=500
        )
        
        return {
            "title": "Mapa de Correlaciones",
            "chart_data": fig.to_json(),
            "type": "heatmap",
            "columns": numeric_columns
        }
    
    def create_wordclouds(self, df: pd.DataFrame, text_columns: List[str]) -> List[Dict[str, Any]]:
        """Crear nubes de palabras"""
        wordclouds = []
        
        for column in text_columns[:2]:  # Limitar a 2 columnas
            # Combinar todo el texto
            text_data = ' '.join(df[column].dropna().astype(str))
            
            if len(text_data.strip()) > 0:
                try:
                    # Crear wordcloud
                    wordcloud = WordCloud(
                        width=800, 
                        height=400, 
                        background_color='white',
                        max_words=50,
                        colormap='viridis'
                    ).generate(text_data)
                    
                    # Convertir a imagen base64
                    img = io.BytesIO()
                    plt.figure(figsize=(10, 5))
                    plt.imshow(wordcloud, interpolation='bilinear')
                    plt.axis('off')
                    plt.title(f'Nube de Palabras - {column}')
                    plt.tight_layout()
                    plt.savefig(img, format='png', bbox_inches='tight', dpi=150)
                    plt.close()
                    
                    img.seek(0)
                    img_base64 = base64.b64encode(img.getvalue()).decode()
                    
                    wordclouds.append({
                        "title": f"Nube de Palabras - {column}",
                        "image_base64": img_base64,
                        "type": "wordcloud",
                        "column": column
                    })
                    
                except Exception as e:
                    print(f"Error creando wordcloud para {column}: {e}")
        
        return wordclouds
    
    def create_sentiment_visualization(self, sentiment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crear visualización específica para análisis de sentimientos"""
        if "overall_sentiment" not in sentiment_data:
            return {}
        
        overall = sentiment_data["overall_sentiment"]
        distribution = overall.get("distribution", {})
        
        # Gráfico de barras de sentimientos
        fig = go.Figure(data=[
            go.Bar(
                x=list(distribution.keys()),
                y=list(distribution.values()),
                marker=dict(
                    color=['green' if x == 'positive' else 'red' if x == 'negative' else 'gray' 
                           for x in distribution.keys()]
                )
            )
        ])
        
        fig.update_layout(
            title='Distribución de Sentimientos',
            xaxis_title='Sentimiento',
            yaxis_title='Cantidad',
            template='plotly_white'
        )
        
        return {
            "title": "Distribución de Sentimientos",
            "chart_data": fig.to_json(),
            "type": "sentiment_bar"
        }
    
    def create_cluster_visualization(self, cluster_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crear visualización de clusters"""
        if "pca_visualization" not in cluster_data:
            return {}
        
        pca_coords = cluster_data["pca_visualization"]["coordinates"]
        cluster_labels = cluster_data["cluster_labels"]
        
        # Convertir a arrays numpy
        coords = np.array(pca_coords)
        
        fig = go.Figure(data=[
            go.Scatter(
                x=coords[:, 0],
                y=coords[:, 1],
                mode='markers',
                marker=dict(
                    color=cluster_labels,
                    colorscale='viridis',
                    size=8,
                    opacity=0.7
                ),
                text=[f'Cluster {label}' for label in cluster_labels]
            )
        ])
        
        fig.update_layout(
            title='Visualización de Clusters (PCA)',
            xaxis_title='Componente Principal 1',
            yaxis_title='Componente Principal 2',
            template='plotly_white'
        )
        
        return {
            "title": "Visualización de Clusters",
            "chart_data": fig.to_json(),
            "type": "cluster_scatter"
        }
    
    def get_available_chart_types(self) -> List[str]:
        """Obtener tipos de gráficos disponibles"""
        return self.chart_types
    
    def create_dashboard_summary(self, df: pd.DataFrame, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Crear resumen visual para dashboard"""
        summary = {
            "total_responses": len(df),
            "total_questions": len(df.columns),
            "completion_rate": (df.notna().sum().sum() / (len(df) * len(df.columns))) * 100,
            "data_quality_score": self.calculate_data_quality_score(df)
        }
        
        # Agregar métricas específicas del análisis
        if "sentiment" in analysis_results:
            sentiment_info = analysis_results["sentiment"].get("overall_sentiment", {})
            summary["dominant_sentiment"] = sentiment_info.get("dominant_sentiment", "neutral")
            summary["average_polarity"] = sentiment_info.get("average_polarity", 0)
        
        if "clustering" in analysis_results:
            cluster_info = analysis_results["clustering"]
            summary["identified_clusters"] = len(cluster_info.get("cluster_sizes", {}))
        
        return summary
    
    def calculate_data_quality_score(self, df: pd.DataFrame) -> float:
        """Calcular puntuación de calidad de datos"""
        # Factores: completitud, consistencia, validez
        completeness = (df.notna().sum().sum() / (len(df) * len(df.columns))) * 100
        
        # Penalizar por duplicados
        duplicate_penalty = (df.duplicated().sum() / len(df)) * 10
        
        # Bonificar por variedad en respuestas
        variety_bonus = min(df.nunique().mean() / len(df) * 20, 10)
        
        quality_score = max(0, min(100, completeness - duplicate_penalty + variety_bonus))
        return round(quality_score, 1)
