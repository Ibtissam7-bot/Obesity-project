"""
Import de tous les schémas pour faciliter les imports
"""
from app.schemas.user import (
    UserCreate, UserLogin, UserBase, UserResponse, 
    UserList, Token, TokenData
)
from app.schemas.prediction import (
    PredictionInput, PredictionResult, PredictionResponse,
    PredictionHistory, ModelInfo
)

__all__ = [
    # User schemas
    "UserCreate", "UserLogin", "UserBase", "UserResponse", 
    "UserList", "Token", "TokenData",
    # Prediction schemas  
    "PredictionInput", "PredictionResult", "PredictionResponse",
    "PredictionHistory", "ModelInfo"
]