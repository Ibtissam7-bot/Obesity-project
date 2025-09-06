"""
Application principale FastAPI
Point d'entrée de l'API
"""
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.config import settings
from app.database import create_tables, test_connection
from app.services.ml_service import ml_service
from app.routers import auth, prediction, admin, pages

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Création de l'app FastAPI
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API de prédiction d'obésité avec authentification JWT",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Middleware CORS (pour les appels depuis un frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifie les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montage des fichiers statiques (CSS, JS, images)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Inclusion des routers
app.include_router(auth.router)
app.include_router(prediction.router)
app.include_router(admin.router)
app.include_router(pages.router)
@app.on_event("startup")
async def startup_event():
    """Actions à effectuer au démarrage de l'application"""
    logger.info("Démarrage de l'application...")
    
    # Test de connexion à la base de données
    if not test_connection():
        raise RuntimeError("Impossible de se connecter à la base de données")
    
    # Création des tables
    create_tables()
    
    # Vérification du modèle ML
    if not ml_service.model_loaded:
        logger.error("Modèle ML non chargé - l'API ne fonctionnera pas correctement")
    else:
        logger.info("Modèle ML chargé avec succès")
    
    logger.info("Application démarrée avec succès!")

@app.get("/")
def read_root():
    """Endpoint de base - Page d'accueil"""
    return {
        "message": "Bienvenue sur l'API de prédiction d'obésité!",
        "version": settings.app_version,
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    """Endpoint de vérification de santé"""
    return {
        "status": "healthy",
        "database": test_connection(),
        "ml_model": ml_service.model_loaded
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )