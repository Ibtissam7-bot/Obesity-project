from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base

class Prediction(Base):
    """
    Modèle de prédiction d'obésité
    
    Attributes:
        id: Identifiant unique
        user_id: ID de l'utilisateur (clé étrangère)
        predicted_class: Classe prédite (ex: "Obesity_Type_I")
        confidence: Probabilité de la classe prédite (0-1)
        input_features: Données d'entrée utilisées (JSON)
        all_probabilities: Toutes les probabilités des classes (JSON)
        created_at: Date de la prédiction
        user: Relation vers l'utilisateur
    """
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Résultats de la prédiction
    predicted_class = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False)  # Probabilité de la classe prédite
    
    # Données utilisées pour la prédiction (stockées en JSON)
    input_features = Column(JSON, nullable=False)
    all_probabilities = Column(JSON, nullable=False)  # {classe: probabilité}
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relation avec l'utilisateur
    user = relationship("User", back_populates="predictions")
    
    def __repr__(self):
        return f"<Prediction(id={self.id}, user_id={self.user_id}, class='{self.predicted_class}', confidence={self.confidence:.3f})>"
    
    @property
    def confidence_percentage(self) -> float:
        """Retourne la confidence en pourcentage"""
        return round(self.confidence * 100, 2)