"""
Service Machine Learning
Charge et utilise le modèle d'obésité pour faire des prédictions
"""
import joblib
import numpy as np
from typing import Dict, List, Tuple
from pathlib import Path
import logging

from app.config import settings, OBESITY_CATEGORIES, EXPECTED_FEATURES
from app.schemas.prediction import PredictionInput, PredictionResult, ModelInfo

logger = logging.getLogger(__name__)

class MLService:
    """Service de Machine Learning pour les prédictions d'obésité"""
    
    def __init__(self):
        self.model = None
        self.model_loaded = False
        self.load_model()
    
    def load_model(self):
        """Charge le modèle depuis le fichier pkl"""
        try:
            model_path = Path(settings.model_path)
            
            if not model_path.exists():
                logger.error(f"Modèle non trouvé à l'emplacement: {model_path}")
                raise FileNotFoundError(f"Fichier modèle non trouvé: {model_path}")
            
            # Charge le modèle avec joblib
            self.model = joblib.load(model_path)
            self.model_loaded = True
            
            logger.info(f"Modèle chargé avec succès depuis: {model_path}")
            logger.info(f"Type de modèle: {type(self.model)}")
            
        except Exception as e:
            logger.error(f"Erreur lors du chargement du modèle: {e}")
            self.model_loaded = False
            raise
    
    def predict(self, input_data: PredictionInput) -> PredictionResult:
        """
        Fait une prédiction avec le modèle
        
        Args:
            input_data: Données d'entrée validées
            
        Returns:
            PredictionResult avec la classe prédite et les probabilités
            
        Raises:
            RuntimeError: Si le modèle n'est pas chargé
        """
        if not self.model_loaded or self.model is None:
            raise RuntimeError("Modèle non chargé")
        
        try:
            # Prépare les données pour le modèle
            features = np.array([input_data.to_list()])
            
            # Fait la prédiction
            prediction = self.model.predict(features)[0]
            probabilities = self.model.predict_proba(features)[0]
            
            # Récupère la classe prédite
            predicted_class = OBESITY_CATEGORIES.get(prediction, f"Unknown_Class_{prediction}")
            
            # Récupère la probabilité de la classe prédite
            confidence = float(probabilities[prediction])
            
            # Crée le dictionnaire de toutes les probabilités
            all_probabilities = {
                OBESITY_CATEGORIES.get(i, f"Class_{i}"): float(prob)
                for i, prob in enumerate(probabilities)
            }
            
            logger.info(f"Prédiction réalisée: {predicted_class} ({confidence:.3f})")
            
            return PredictionResult(
                predicted_class=predicted_class,
                confidence=confidence,
                confidence_percentage=round(confidence * 100, 2),
                all_probabilities=all_probabilities,
                input_features=input_data.to_dict()
            )
            
        except Exception as e:
            logger.error(f"Erreur lors de la prédiction: {e}")
            raise RuntimeError(f"Erreur de prédiction: {e}")
    
    def get_model_info(self) -> ModelInfo:
        """
        Retourne les informations sur le modèle pour l'endpoint /metrics
        
        Returns:
            ModelInfo avec les détails du modèle
        """
        if not self.model_loaded:
            raise RuntimeError("Modèle non chargé")
        
        return ModelInfo(
            model_name="Obesity Classification Model",
            model_version="1.0",
            features=EXPECTED_FEATURES,
            classes=list(OBESITY_CATEGORIES.values()),
            last_training_date="2024-09-01",  # Tu peux changer cette date
            accuracy=0.97  # Basé sur tes métriques très bonnes
        )
    
    def validate_features(self, input_data: PredictionInput) -> bool:
        """
        Valide que les features correspondent à ce qu'attend le modèle
        
        Args:
            input_data: Données d'entrée
            
        Returns:
            True si valide, False sinon
        """
        try:
            # Vérifie que toutes les features sont présentes
            input_dict = input_data.to_dict()
            
            for feature in EXPECTED_FEATURES:
                if feature not in input_dict:
                    logger.warning(f"Feature manquante: {feature}")
                    return False
            
            # Vérifie que les valeurs sont des nombres
            for key, value in input_dict.items():
                if not isinstance(value, (int, float)):
                    logger.warning(f"Feature {key} n'est pas un nombre: {value}")
                    return False
                    
                if np.isnan(value) or np.isinf(value):
                    logger.warning(f"Feature {key} contient une valeur invalide: {value}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de la validation: {e}")
            return False

# Instance globale du service ML
ml_service = MLService()