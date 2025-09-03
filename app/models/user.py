from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.database import Base

class UserRole(str, enum.Enum):
    """Rôles possibles pour un utilisateur"""
    USER = "user"
    ADMIN = "admin"

class User(Base):
    """
    Modèle utilisateur
    
    Attributes:
        id: Identifiant unique
        username: Nom d'utilisateur unique
        email: Email unique
        hashed_password: Mot de passe haché
        is_active: Utilisateur actif ou non
        role: Rôle (user/admin)
        created_at: Date de création
        updated_at: Date de mise à jour
        predictions: Relation vers les prédictions de l'utilisateur
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), default=UserRole.USER)
    
    # Timestamps automatiques
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relation avec les prédictions (sera définie après création du modèle Prediction)
    predictions = relationship("Prediction", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
    
    @property
    def is_admin(self) -> bool:
        """Vérifie si l'utilisateur est admin"""
        return self.role == UserRole.ADMIN