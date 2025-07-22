"""
Motor de Predicción Electoral Principal
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from typing import Dict, List, Tuple, Optional
import logging
from datetime import datetime

class PredictionEngine:
    """
    Motor principal de predicción electoral que combina múltiples fuentes de datos
    """
    
    def __init__(self):
        self.models = {
            'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'gradient_boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
            'logistic_regression': LogisticRegression(random_state=42)
        }
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.feature_importance = {}
        self.trained_models = {}
        self.logger = self._setup_logger()
        
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
    
    def prepare_electoral_features(self, df: pd.DataFrame, social_media_data: Dict = None) -> pd.DataFrame:
        """
        Preparar características para el modelo de predicción
        """
        features_df = df.copy()
        
        # Características demográficas
        features_df['age_group'] = pd.cut(
            features_df['age'], 
            bins=[0, 25, 35, 50, 65, 100], 
            labels=['18-25', '26-35', '36-50', '51-65', '65+']
        )
        
        # Codificar variables categóricas
        categorical_columns = ['gender', 'education', 'income_level', 'region', 'age_group']
        for col in categorical_columns:
            if col in features_df.columns:
                features_df[f'{col}_encoded'] = LabelEncoder().fit_transform(features_df[col].astype(str))
        
        # Características de comportamiento político
        features_df['political_engagement'] = (
            features_df['political_interest'] * features_df['social_media_activity']
        )
        
        features_df['voting_likelihood'] = (
            features_df['voting_intention'] * features_df['political_interest'] / 10
        )
        
        # Agregar datos de redes sociales si están disponibles
        if social_media_data:
            features_df = self._add_social_media_features(features_df, social_media_data)
        
        # Características temporales
        if 'survey_date' in features_df.columns:
            features_df['days_to_election'] = (
                pd.to_datetime('2024-12-31') - pd.to_datetime(features_df['survey_date'])
            ).dt.days
            
            features_df['survey_month'] = pd.to_datetime(features_df['survey_date']).dt.month
            features_df['survey_weekday'] = pd.to_datetime(features_df['survey_date']).dt.weekday
        
        return features_df
    
    def _add_social_media_features(self, df: pd.DataFrame, social_media_data: Dict) -> pd.DataFrame:
        """Agregar características basadas en datos de redes sociales"""
        # Crear características agregadas de redes sociales por candidato
        candidate_social_scores = {}
        
        for candidate, data in social_media_data.items():
            # Score combinado de redes sociales
            influence_score = data.get('influence_score', 0)
            engagement = data.get('engagement_metrics', {})
            sentiment = data.get('overall_sentiment', {})
            
            social_score = (
                influence_score * 0.4 +
                engagement.get('engagement_rate', 0) * 1000 * 0.3 +
                sentiment.get('positive_percentage', 0) * 0.3
            )
            
            candidate_social_scores[candidate] = social_score
        
        # Agregar score de redes sociales del candidato preferido
        df['candidate_social_score'] = df['preferred_candidate'].map(candidate_social_scores).fillna(0)
        
        # Normalizar score
        if df['candidate_social_score'].max() > 0:
            df['candidate_social_score'] = df['candidate_social_score'] / df['candidate_social_score'].max()
        
        return df
    
    def train_models(self, df: pd.DataFrame, social_media_data: Dict = None) -> Dict:
        """
        Entrenar modelos de predicción
        """
        # Preparar características
        features_df = self.prepare_electoral_features(df, social_media_data)
        
        # Seleccionar características para el modelo
        feature_columns = [
            'age', 'gender_encoded', 'education_encoded', 'income_level_encoded',
            'region_encoded', 'political_interest', 'social_media_activity',
            'voting_intention', 'political_engagement', 'voting_likelihood'
        ]
        
        # Agregar características adicionales si están disponibles
        if 'candidate_social_score' in features_df.columns:
            feature_columns.append('candidate_social_score')
        
        if 'days_to_election' in features_df.columns:
            feature_columns.extend(['days_to_election', 'survey_month', 'survey_weekday'])
        
        # Filtrar columnas que existen
        available_features = [col for col in feature_columns if col in features_df.columns]
        
        X = features_df[available_features]
        y = features_df['preferred_candidate']
        
        # Codificar variable objetivo
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Dividir datos
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
        )
        
        # Normalizar características
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Entrenar modelos
        results = {}
        
        for model_name, model in self.models.items():
            self.logger.info(f"Entrenando modelo: {model_name}")
            
            # Entrenar modelo
            model.fit(X_train_scaled, y_train)
            
            # Predecir
            y_pred = model.predict(X_test_scaled)
            
            # Evaluar
            accuracy = accuracy_score(y_test, y_pred)
            cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5)
            
            # Guardar modelo entrenado
            self.trained_models[model_name] = model
            
            # Obtener importancia de características (si está disponible)
            if hasattr(model, 'feature_importances_'):
                self.feature_importance[model_name] = dict(
                    zip(available_features, model.feature_importances_)
                )
            
            results[model_name] = {
                'accuracy': accuracy,
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std(),
                'predictions': self.label_encoder.inverse_transform(y_pred),
                'actual': self.label_encoder.inverse_transform(y_test)
            }
            
            self.logger.info(f"{model_name} - Precisión: {accuracy:.3f}, CV: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")
        
        return results
    
    def predict_election_results(self, df: pd.DataFrame, social_media_data: Dict = None) -> Dict:
        """
        Predecir resultados electorales
        """
        if not self.trained_models:
            self.logger.error("Los modelos no han sido entrenados")
            return {}
        
        # Preparar características
        features_df = self.prepare_electoral_features(df, social_media_data)
        
        # Seleccionar las mismas características usadas en entrenamiento
        feature_columns = list(self.feature_importance.get('random_forest', {}).keys())
        if not feature_columns:
            # Usar características por defecto si no hay importancia guardada
            feature_columns = [
                'age', 'gender_encoded', 'education_encoded', 'income_level_encoded',
                'region_encoded', 'political_interest', 'social_media_activity',
                'voting_intention', 'political_engagement', 'voting_likelihood'
            ]
        
        available_features = [col for col in feature_columns if col in features_df.columns]
        X = features_df[available_features]
        X_scaled = self.scaler.transform(X)
        
        # Realizar predicciones con todos los modelos
        predictions = {}
        
        for model_name, model in self.trained_models.items():
            y_pred = model.predict(X_scaled)
            y_pred_proba = model.predict_proba(X_scaled) if hasattr(model, 'predict_proba') else None
            
            # Convertir predicciones a nombres de candidatos
            candidate_predictions = self.label_encoder.inverse_transform(y_pred)
            
            # Calcular distribución de votos
            vote_distribution = pd.Series(candidate_predictions).value_counts(normalize=True)
            
            predictions[model_name] = {
                'vote_share': vote_distribution.to_dict(),
                'predicted_winner': vote_distribution.index[0],
                'winner_probability': vote_distribution.iloc[0],
                'predictions': candidate_predictions.tolist()
            }
            
            if y_pred_proba is not None:
                # Calcular probabilidades promedio por candidato
                avg_probabilities = {}
                candidates = self.label_encoder.classes_
                
                for i, candidate in enumerate(candidates):
                    avg_probabilities[candidate] = y_pred_proba[:, i].mean()
                
                predictions[model_name]['average_probabilities'] = avg_probabilities
        
        return predictions
    
    def ensemble_prediction(self, predictions: Dict) -> Dict:
        """
        Combinar predicciones de múltiples modelos para obtener resultado final
        """
        if not predictions:
            return {}
        
        # Obtener todos los candidatos
        all_candidates = set()
        for model_pred in predictions.values():
            all_candidates.update(model_pred['vote_share'].keys())
        
        # Calcular promedio ponderado de participación de voto
        ensemble_vote_share = {}
        model_weights = {
            'random_forest': 0.4,
            'gradient_boosting': 0.4,
            'logistic_regression': 0.2
        }
        
        for candidate in all_candidates:
            weighted_share = 0
            total_weight = 0
            
            for model_name, model_pred in predictions.items():
                if model_name in model_weights:
                    weight = model_weights[model_name]
                    share = model_pred['vote_share'].get(candidate, 0)
                    weighted_share += share * weight
                    total_weight += weight
            
            if total_weight > 0:
                ensemble_vote_share[candidate] = weighted_share / total_weight
        
        # Ordenar candidatos por participación de voto
        sorted_candidates = sorted(
            ensemble_vote_share.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return {
            'predicted_winner': sorted_candidates[0][0] if sorted_candidates else None,
            'vote_share': ensemble_vote_share,
            'ranking': sorted_candidates,
            'margin_of_victory': (
                sorted_candidates[0][1] - sorted_candidates[1][1] 
                if len(sorted_candidates) >= 2 else 0
            ),
            'confidence_level': self._calculate_confidence(predictions, sorted_candidates[0][0])
        }
    
    def _calculate_confidence(self, predictions: Dict, predicted_winner: str) -> float:
        """Calcular nivel de confianza de la predicción"""
        # Contar cuántos modelos predicen al mismo ganador
        winner_count = 0
        total_models = len(predictions)
        
        for model_pred in predictions.values():
            if model_pred['predicted_winner'] == predicted_winner:
                winner_count += 1
        
        # Calcular confianza basada en consenso de modelos
        consensus_confidence = winner_count / total_models
        
        # Ajustar por margen de victoria promedio
        margin_sum = 0
        for model_pred in predictions.values():
            vote_shares = list(model_pred['vote_share'].values())
            vote_shares.sort(reverse=True)
            if len(vote_shares) >= 2:
                margin_sum += vote_shares[0] - vote_shares[1]
        
        avg_margin = margin_sum / total_models if total_models > 0 else 0
        
        # Combinar confianza de consenso y margen
        final_confidence = (consensus_confidence * 0.7 + avg_margin * 0.3)
        
        return min(final_confidence, 1.0)
    
    def analyze_key_factors(self) -> Dict:
        """Analizar factores clave que influyen en las predicciones"""
        if not self.feature_importance:
            return {}
        
        # Combinar importancia de características de todos los modelos
        combined_importance = {}
        
        for model_name, importance in self.feature_importance.items():
            for feature, value in importance.items():
                if feature not in combined_importance:
                    combined_importance[feature] = []
                combined_importance[feature].append(value)
        
        # Calcular importancia promedio
        avg_importance = {}
        for feature, values in combined_importance.items():
            avg_importance[feature] = np.mean(values)
        
        # Ordenar por importancia
        sorted_features = sorted(
            avg_importance.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return {
            'top_factors': sorted_features[:10],
            'feature_importance_by_model': self.feature_importance,
            'most_important_factor': sorted_features[0][0] if sorted_features else None
        }
    
    def generate_prediction_report(self, 
                                 electoral_data: pd.DataFrame,
                                 social_media_data: Dict = None,
                                 file_path: str = 'prediction_report.txt') -> Dict:
        """Generar reporte completo de predicción electoral"""
        
        # Entrenar modelos
        training_results = self.train_models(electoral_data, social_media_data)
        
        # Realizar predicciones
        predictions = self.predict_election_results(electoral_data, social_media_data)
        
        # Obtener predicción ensemble
        ensemble_result = self.ensemble_prediction(predictions)
        
        # Analizar factores clave
        key_factors = self.analyze_key_factors()
        
        # Generar reporte
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("REPORTE DE PREDICCIÓN ELECTORAL\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"Fecha de análisis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Datos analizados: {len(electoral_data)} registros\n\n")
            
            # Predicción final
            f.write("PREDICCIÓN FINAL (ENSEMBLE)\n")
            f.write("-" * 30 + "\n")
            f.write(f"Ganador predicho: {ensemble_result.get('predicted_winner', 'N/A')}\n")
            f.write(f"Nivel de confianza: {ensemble_result.get('confidence_level', 0):.1%}\n")
            f.write(f"Margen de victoria: {ensemble_result.get('margin_of_victory', 0):.1%}\n\n")
            
            # Ranking de candidatos
            f.write("RANKING DE CANDIDATOS\n")
            f.write("-" * 25 + "\n")
            for i, (candidate, share) in enumerate(ensemble_result.get('ranking', []), 1):
                f.write(f"{i}. {candidate}: {share:.1%}\n")
            f.write("\n")
            
            # Resultados por modelo
            f.write("RESULTADOS POR MODELO\n")
            f.write("-" * 25 + "\n")
            for model_name, result in predictions.items():
                f.write(f"{model_name.upper()}:\n")
                f.write(f"  Ganador: {result['predicted_winner']}\n")
                f.write(f"  Probabilidad: {result['winner_probability']:.1%}\n")
                f.write(f"  Distribución de votos:\n")
                for candidate, share in result['vote_share'].items():
                    f.write(f"    {candidate}: {share:.1%}\n")
                f.write("\n")
            
            # Factores clave
            f.write("FACTORES CLAVE DE INFLUENCIA\n")
            f.write("-" * 35 + "\n")
            for i, (factor, importance) in enumerate(key_factors.get('top_factors', [])[:5], 1):
                f.write(f"{i}. {factor}: {importance:.3f}\n")
            f.write("\n")
            
            # Precisión de modelos
            f.write("PRECISIÓN DE MODELOS\n")
            f.write("-" * 25 + "\n")
            for model_name, result in training_results.items():
                f.write(f"{model_name}: {result['accuracy']:.1%} (CV: {result['cv_mean']:.1%})\n")
        
        self.logger.info(f"Reporte de predicción exportado a: {file_path}")
        
        return {
            'ensemble_prediction': ensemble_result,
            'individual_predictions': predictions,
            'model_performance': training_results,
            'key_factors': key_factors
        }
