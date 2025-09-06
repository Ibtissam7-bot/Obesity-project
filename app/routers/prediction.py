# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from typing import List

# from app.database import get_db
# from app.models.user import User
# from app.models.prediction import Prediction
# from app.schemas.prediction import PredictionInput, PredictionResult, PredictionHistory, ModelInfo
# from app.services.auth_service import get_current_user
# from app.services.ml_service import ml_service

# # Router pour grouper les endpoints
# router = APIRouter(prefix="/predict", tags=["Predictions"])

# @router.post("/", response_model=PredictionResult)
# def make_prediction(
#     input_data: PredictionInput,
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     """
#     Fait une prédiction d'obésité et la sauvegarde
#     """
#     try:
#         # Valide les données
#         if not ml_service.validate_features(input_data):
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Données d'entrée invalides"
#             )
        
#         # Fait la prédiction
#         result = ml_service.predict(input_data)
        
#         # Sauvegarde la prédiction en base
#         new_prediction = Prediction(
#             user_id=current_user.id,
#             predicted_class=result.predicted_class,
#             confidence=result.confidence,
#             input_features=result.input_features,
#             all_probabilities=result.all_probabilities
#         )
        
#         db.add(new_prediction)
#         db.commit()
        
#         return result
        
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Erreur lors de la prédiction: {str(e)}"
#         )

# @router.get("/history", response_model=PredictionHistory)
# def get_prediction_history(
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db),
#     limit: int = 50
# ):
#     """
#     Récupère l'historique des prédictions de l'utilisateur connecté
#     """
#     # Récupère les prédictions de l'utilisateur (les plus récentes d'abord)
#     predictions = db.query(Prediction)\
#         .filter(Prediction.user_id == current_user.id)\
#         .order_by(Prediction.created_at.desc())\
#         .limit(limit)\
#         .all()
    
#     total = db.query(Prediction)\
#         .filter(Prediction.user_id == current_user.id)\
#         .count()
    
#     return PredictionHistory(
#         predictions=predictions,
#         total=total
#     )

# @router.get("/metrics", response_model=ModelInfo)
# def get_model_metrics():
#     """
#     Récupère les informations du modèle ML (nom, features, classes, etc.)
#     """
#     try:
#         return ml_service.get_model_info()
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Erreur lors de la récupération des métriques: {str(e)}"
#         )




# """
# Endpoints pour les prédictions ML
# Code simple et lisible
# """
# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from typing import List

# from app.database import get_db
# from app.models.user import User
# from app.models.prediction import Prediction
# from app.schemas.prediction import PredictionInput, PredictionResult, PredictionHistory, ModelInfo
# from app.services.auth_service import get_current_user
# from app.services.ml_service import ml_service

# # Router pour grouper les endpoints
# router = APIRouter(prefix="/predict", tags=["Predictions"])

# @router.post("/", response_model=PredictionResult)
# def make_prediction(
#     input_data: PredictionInput,
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     """
#     Fait une prédiction d'obésité et la sauvegarde
#     """
#     import logging
#     logger = logging.getLogger(__name__)
    
#     try:
#         logger.info(f"Utilisateur: {current_user.username}")
#         logger.info(f"Données reçues: {input_data}")
        
#         # Valide les données
#         if not ml_service.validate_features(input_data):
#             logger.error("Validation des features échouée")
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Données d'entrée invalides"
#             )
        
#         logger.info("Validation OK, appel du modèle...")
        
#         # Fait la prédiction
#         result = ml_service.predict(input_data)
        
#         logger.info(f"Prédiction OK: {result.predicted_class}")
        
#         # Sauvegarde la prédiction en base
#         new_prediction = Prediction(
#             user_id=current_user.id,
#             predicted_class=result.predicted_class,
#             confidence=result.confidence,
#             input_features=result.input_features,
#             all_probabilities=result.all_probabilities
#         )
        
#         db.add(new_prediction)
#         db.commit()
#         logger.info("Prédiction sauvegardée en base")
        
#         return result
        
#     except HTTPException:
#         raise
#     except Exception as e:
#         logger.error(f"Erreur complète: {e}")
#         import traceback
#         logger.error(f"Traceback: {traceback.format_exc()}")
#         db.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Erreur lors de la prédiction: {str(e)}"
#         )

# @router.get("/history", response_model=PredictionHistory)
# def get_prediction_history(
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db),
#     limit: int = 50
# ):
#     """
#     Récupère l'historique des prédictions de l'utilisateur connecté
#     """
#     # Récupère les prédictions de l'utilisateur (les plus récentes d'abord)
#     predictions = db.query(Prediction)\
#         .filter(Prediction.user_id == current_user.id)\
#         .order_by(Prediction.created_at.desc())\
#         .limit(limit)\
#         .all()
    
#     total = db.query(Prediction)\
#         .filter(Prediction.user_id == current_user.id)\
#         .count()
    
#     return PredictionHistory(
#         predictions=predictions,
#         total=total
#     )

# @router.get("/metrics", response_model=ModelInfo)
# def get_model_metrics():
#     """
#     Récupère les informations du modèle ML (nom, features, classes, etc.)
#     """
#     try:
#         return ml_service.get_model_info()
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Erreur lors de la récupération des métriques: {str(e)}"
#         )

"""
Endpoints pour les prédictions ML
Code simple et lisible
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.prediction import Prediction
from app.schemas.prediction import PredictionInput, PredictionResult, PredictionHistory, ModelInfo
from app.services.auth_service import get_current_user
from app.services.ml_service_fixed import ml_service_fixed as ml_service

# Router pour grouper les endpoints
router = APIRouter(prefix="/predict", tags=["Predictions"])

@router.post("/", response_model=PredictionResult)
def make_prediction(
    input_data: PredictionInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Fait une prédiction d'obésité et la sauvegarde
    """
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"Utilisateur: {current_user.username}")
        logger.info(f"Données reçues: {input_data}")
        
        # Valide les données
        if not ml_service.validate_features(input_data):
            logger.error("Validation des features échouée")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Données d'entrée invalides"
            )
        
        logger.info("Validation OK, appel du modèle...")
        
        # Fait la prédiction
        result = ml_service.predict(input_data)
        
        logger.info(f"Prédiction OK: {result.predicted_class}")
        
        # Sauvegarde la prédiction en base
        new_prediction = Prediction(
            user_id=current_user.id,
            predicted_class=result.predicted_class,
            confidence=result.confidence,
            input_features=result.input_features,
            all_probabilities=result.all_probabilities
        )
        
        db.add(new_prediction)
        db.commit()
        logger.info("Prédiction sauvegardée en base")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur complète: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la prédiction: {str(e)}"
        )

@router.get("/history", response_model=PredictionHistory)
def get_prediction_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 50
):
    """
    Récupère l'historique des prédictions de l'utilisateur connecté
    """
    # Récupère les prédictions de l'utilisateur (les plus récentes d'abord)
    predictions = db.query(Prediction)\
        .filter(Prediction.user_id == current_user.id)\
        .order_by(Prediction.created_at.desc())\
        .limit(limit)\
        .all()
    
    total = db.query(Prediction)\
        .filter(Prediction.user_id == current_user.id)\
        .count()
    
    return PredictionHistory(
        predictions=predictions,
        total=total
    )

@router.get("/metrics", response_model=ModelInfo)
def get_model_metrics():
    """
    Récupère les informations du modèle ML (nom, features, classes, etc.)
    """
    try:
        return ml_service.get_model_info()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des métriques: {str(e)}"
        )