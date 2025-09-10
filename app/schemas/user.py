from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime
from app.models.user import UserRole

class UserBase(BaseModel):
    """Schéma de base d'un utilisateur (sans mot de passe)"""
    id: int
    username: str
    email: str
    is_active: bool
    role: UserRole
    created_at: datetime
    
    class Config:
        from_attributes = True  # Pour SQLAlchemy

# --- Schémas pour la création/mise à jour ---
class UserCreate(BaseModel):
    """Schéma pour créer un utilisateur (register)"""
    username: str
    email: EmailStr
    password: str
    role: Optional[UserRole] = UserRole.USER  # Par défaut USER

    
    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError('Le nom d\'utilisateur doit contenir au moins 3 caractères')
        if len(v) > 50:
            raise ValueError('Le nom d\'utilisateur ne peut pas dépasser 50 caractères')
        return v.lower().strip()
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Le mot de passe doit contenir au moins 6 caractères')
        return v

class UserLogin(BaseModel):
    """Schéma pour la connexion d'un utilisateur"""
    username: str
    password: str


# Schéma pour la connexion d'un utilisateur
class UserLogin(BaseModel):
    username: str
    password: str

# --- Schémas de réponse ---



# class UserResponse(UserBase):
#     """Schéma de réponse complète pour un utilisateur"""
#     updated_at: Optional[datetime] = None

# Schéma pour la réponse de l'API (pour afficher les infos utilisateur)
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    is_active: bool
    created_at: datetime
    # Permet à Pydantic de lire les données d'un objet ORM
    class Config:
        from_attributes = True

class UserList(BaseModel):
    """Schéma pour la liste des utilisateurs (admin)"""
    users: list[UserBase]
    total: int

# --- Schémas pour l'authentification ---

class Token(BaseModel):
    """Schéma pour le token JWT"""
    access_token: str
    token_type: str = "bearer"
    user: UserBase

class TokenData(BaseModel):
    """Données contenues dans le token JWT"""
    username: Optional[str] = None
    user_id: Optional[int] = None



class LoginResponse(BaseModel):
    user: UserResponse
    access_token: str
    token_type: str