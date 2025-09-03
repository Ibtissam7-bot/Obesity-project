"""
Service d'authentification avec JWT
Gère la création des tokens, vérification des mots de passe, etc.
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.config import settings
from app.models.user import User
from app.schemas.user import TokenData

# Configuration pour le hashage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuration pour récupérer le token Bearer
security = HTTPBearer()

class AuthService:
    """Service d'authentification"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hashe un mot de passe"""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Vérifie un mot de passe contre son hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Crée un token JWT
        
        Args:
            data: Données à encoder dans le token
            expires_delta: Durée de validité personnalisée
            
        Returns:
            Token JWT signé
        """
        to_encode = data.copy()
        
        # Définit l'expiration
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        
        # Encode et signe le token
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.secret_key, 
            algorithm=settings.algorithm
        )
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> TokenData:
        """
        Vérifie et decode un token JWT
        
        Args:
            token: Token JWT à vérifier
            
        Returns:
            TokenData avec les informations du token
            
        Raises:
            HTTPException: Si le token est invalide
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            # Décode le token
            payload = jwt.decode(
                token, 
                settings.secret_key, 
                algorithms=[settings.algorithm]
            )
            
            # Récupère les données
            username: str = payload.get("sub")
            user_id: int = payload.get("user_id")
            
            if username is None or user_id is None:
                raise credentials_exception
                
            return TokenData(username=username, user_id=user_id)
            
        except JWTError:
            raise credentials_exception
    
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
        """
        Authentifie un utilisateur
        
        Args:
            db: Session de base de données
            username: Nom d'utilisateur
            password: Mot de passe en clair
            
        Returns:
            User si authentification réussie, None sinon
        """
        user = db.query(User).filter(User.username == username).first()
        
        if not user:
            return None
            
        if not AuthService.verify_password(password, user.hashed_password):
            return None
            
        if not user.is_active:
            return None
            
        return user

# --- Dépendances FastAPI ---

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    """
    Dépendance FastAPI pour récupérer l'utilisateur actuel via JWT
    
    Usage dans un endpoint:
    def my_endpoint(current_user: User = Depends(get_current_user)):
        # current_user contient l'utilisateur connecté
    """
    # Import local pour éviter les imports circulaires
    from app.database import get_db
    
    db = next(get_db())
    
    try:
        # Récupère le token depuis l'en-tête Authorization
        token = credentials.credentials
        
        # Vérifie le token
        token_data = AuthService.verify_token(token)
        
        # Récupère l'utilisateur depuis la DB
        user = db.query(User).filter(User.id == token_data.user_id).first()
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Utilisateur non trouvé"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Utilisateur désactivé"
            )
        
        return user
    finally:
        db.close()

def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Dépendance FastAPI pour vérifier que l'utilisateur actuel est admin
    
    Usage:
    def admin_endpoint(admin_user: User = Depends(get_current_admin_user)):
        # admin_user est forcément admin
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès refusé - privilèges administrateur requis"
        )
    return current_user