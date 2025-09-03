from pydantic import BaseModel, validator
from typing import Dict, List
from datetime import datetime

# --- Schémas d'entrée ---

class PredictionInput(BaseModel):
    """
    Schéma pour les données d'entrée du modèle ML
    Basé sur tes features: Age, Height, Weight, history
    """
    Age: float
    Height: float  # en cm 
    Weight: float  # en kg 
    history: float  
    
    @validator('Age')
    def validate_age(cls, v):
        if v < 0 or v > 150:
            raise ValueError('L\'âge doit être entre 0 et 150 ans')
        return v
    
    @validator('Height')
    def validate_height(cls, v):
        if v < 50 or v > 300:
            raise ValueError('La taille doit être entre 50 et 300 cm')
        return v
    
    @validator('Weight')
    def validate_weight(cls, v):
        if v < 10 or v > 500:
            raise ValueError('Le poids doit être entre 10 et 500 kg')
        return v
    
    @validator('history')
    def validate_history(cls, v):
        if v < 0:
            raise ValueError('La valeur history doit être soit 0 si on pas d\'antécédent d\'obesite dans la famille, soit 1 si oui ')
        return v
    
    def to_list(self) -> List[float]:
        """Convertit en liste pour le modèle ML"""
        return [self.Age, self.Height, self.Weight, self.history]
    
    def to_dict(self) -> Dict[str, float]:
        """Convertit en dictionnaire"""
        return {
            "Age": self.Age,
            "Height": self.Height, 
            "Weight": self.Weight,
            "history": float(self.history)
        }

# --- Schémas de sortie ---

class PredictionResult(BaseModel):
    """Résultat d'une prédiction"""
    predicted_class: str
    confidence: float
    confidence_percentage: float
    all_probabilities: Dict[str, float]
    input_features: Dict[str, float]
    
    class Config:
        json_encoders = {
            float: lambda v: round(v, 4)
        }

class PredictionResponse(BaseModel):
    """Réponse complète d'une prédiction stockée en DB"""
    id: int
    predicted_class: str
    confidence: float
    confidence_percentage: float
    all_probabilities: Dict[str, float]
    input_features: Dict[str, float]
    created_at: datetime
    
    class Config:
        from_attributes = True

class PredictionHistory(BaseModel):
    """Historique des prédictions pour un utilisateur"""
    predictions: List[PredictionResponse]
    total: int
    
class ModelInfo(BaseModel):
    """Informations sur le modèle ML pour l'endpoint /metrics"""
    model_name: str = "Obesity Classification Model"
    model_version: str = "1.0"
    features: List[str]
    classes: List[str]
    last_training_date: str = "2025-09-01"  # Tu peux changer cette date
    accuracy: float = 0.97  # Basé sur tes résultats qui semblent très bons