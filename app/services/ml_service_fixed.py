"""
Service Machine Learning - VERSION CORRIGÉE
Remplace temporairement ml_service.py
"""
import joblib
import numpy as np
from typing import Dict, List, Tuple
from pathlib import Path
import logging

from app.config import settings, OBESITY_CATEGORIES, EXPECTED_FEATURES, CLASS_TO_INDEX
from app.schemas.prediction import PredictionInput, PredictionResult, ModelInfo

logger = logging.getLogger(__name__)

class MLServiceFixed:
    """Service ML corrigé"""
    
    def __init__(self):
        self.model = None
        self.model_loaded = False
        self.load_model()
    
    def load_model(self):
        """Charge le modèle"""
        try:
            model_path = Path(settings.model_path)
            
            if not model_path.exists():
                logger.error(f"Modèle non trouvé: {model_path}")
                raise FileNotFoundError(f"Modèle non trouvé: {model_path}")
            
            # Charge le modèle
            import pickle
            try:
                self.model = joblib.load(model_path)
                logger.info("Modèle chargé avec joblib")
            except:
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                logger.info("Modèle chargé avec pickle")
            
            self.model_loaded = True
            logger.info(f"✅ Modèle chargé: {type(self.model)}")
            
        except Exception as e:
            logger.error(f"❌ Erreur chargement: {e}")
            self.model_loaded = False
            raise
    
    def predict(self, input_data: PredictionInput) -> PredictionResult:
        """Fait une prédiction - VERSION SIMPLE QUI MARCHE"""
        if not self.model_loaded:
            raise RuntimeError("Modèle non chargé")
        
        try:
            # Données
            features = input_data.to_list()
            features_array = np.array([features])
            
            # Prédiction
            prediction = self.model.predict(features_array)[0]
            probabilities = self.model.predict_proba(features_array)[0]
            
            logger.info(f"🎯 Prédiction: {prediction}")
            logger.info(f"📊 Probas: {probabilities}")
            
            # Ton modèle retourne 'Normal_Weight' (string)
            predicted_class = str(prediction)
            
            # On trouve l'index: 'Normal_Weight' -> index 1
            prediction_index = CLASS_TO_INDEX.get(predicted_class, 0)
            
            # On prend la probabilité à cet index: probabilities[1] = 0.77
            confidence = float(probabilities[prediction_index])
            
            logger.info(f"✅ '{predicted_class}' -> index {prediction_index} -> {confidence:.3f}")
            
            # Toutes les probas
            all_probabilities = {}
            for i, prob in enumerate(probabilities):
                class_name = OBESITY_CATEGORIES.get(i, f"Class_{i}")
                all_probabilities[class_name] = float(prob)
            
            # Résultat
            result = PredictionResult(
                predicted_class=predicted_class,
                confidence=confidence,
                confidence_percentage=round(confidence * 100, 2),
                all_probabilities=all_probabilities,
                input_features=input_data.to_dict()
            )
            
            logger.info(f"🎉 SUCCÈS: {predicted_class} ({confidence:.1%})")
            return result
            
        except Exception as e:
            logger.error(f"💥 Erreur: {e}")
            import traceback
            logger.error(traceback.format_exc())
            raise RuntimeError(f"Erreur: {e}")
    
    def validate_features(self, input_data: PredictionInput) -> bool:
        """Valide les features"""
        return True  # Simplifié pour l'instant
    
    def get_model_info(self) -> ModelInfo:
        """Info modèle"""
        return ModelInfo(
            features=EXPECTED_FEATURES,
            classes=list(OBESITY_CATEGORIES.values())
        )

# Instance globale
ml_service_fixed = MLServiceFixed()