"""
Endpoints d'administration
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.prediction import Prediction
from app.schemas.user import UserList, UserResponse
from app.services.auth_service import get_current_admin_user

# Router pour grouper les endpoints
router = APIRouter(prefix="/admin", tags=["Administration"])

@router.get("/users", response_model=UserList)
def list_all_users(
    admin_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
    limit: int = 100
):
    """
    Liste tous les utilisateurs (admin seulement)
    """
    users = db.query(User).limit(limit).all()
    total = db.query(User).count()
    
    return UserList(users=users, total=total)

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id: int,
    admin_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Récupère un utilisateur par son ID (admin seulement)
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    
    return user

@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    admin_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Supprime un utilisateur (admin seulement)
    """
    # Vérifie que ce n'est pas l'admin qui se supprime lui-même
    if user_id == admin_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vous ne pouvez pas supprimer votre propre compte"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    
    # Supprime l'utilisateur (les prédictions seront supprimées automatiquement grâce au cascade)
    db.delete(user)
    db.commit()
    
    return {"message": f"Utilisateur {user.username} supprimé avec succès"}

@router.put("/users/{user_id}/toggle-active")
def toggle_user_active(
    user_id: int,
    admin_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Active/désactive un utilisateur (admin seulement)
    """
    if user_id == admin_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vous ne pouvez pas désactiver votre propre compte"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    
    # Change le statut
    user.is_active = not user.is_active
    db.commit()
    
    status_text = "activé" if user.is_active else "désactivé"
    return {"message": f"Utilisateur {user.username} {status_text} avec succès"}

@router.get("/stats")
def get_admin_stats(
    admin_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Statistiques générales (admin seulement)
    """
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    total_predictions = db.query(Prediction).count()
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "inactive_users": total_users - active_users,
        "total_predictions": total_predictions
    }