from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse, Token, UserCreate , UserLogin, LoginResponse
from app.services.auth_service import AuthService, get_current_user
from app.services.auth_service import create_user
from app.config import settings

# Créez votre routeur
router = APIRouter(prefix="/auth",tags=["Authentification"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Crée un nouvel utilisateur.
    """
    # Vérifie si l'utilisateur existe déjà
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Nom d'utilisateur déjà enregistré"
        )
    
    # Utilisez votre service pour créer l'utilisateur
    new_user = create_user(db, user)
    return {"message": "Utilisateur enregistré avec succès"}

@router.post("/login", response_model=LoginResponse)
def login_for_access_token(
    user_data: UserLogin, 
    db: Session = Depends(get_db)
):
    """
    Authentifie l'utilisateur et renvoie un token JWT.
    """
    # Authentifie l'utilisateur
    user = AuthService.authenticate_user(db, user_data.username, user_data.password)
    
    # Gère les échecs d'authentification
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Définit l'expiration du token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    
    # Crée le token
    access_token = AuthService.create_access_token(
        data={"sub": user.username, "user_id": user.id}, 
        expires_delta=access_token_expires
    )
    
    # Renvoie le token et les informations utilisateur
    return {
        "user": user, 
        "access_token": access_token, 
        "token_type": "bearer"
    }



@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Récupère les informations de l'utilisateur connecté.
    """
    return current_user
