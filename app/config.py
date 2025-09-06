# """
# Configuration de l'application
# Centralise toutes les variables d'environnement et constantes
# """
# import os
# from typing import Optional
# from pydantic_settings import BaseSettings
# from dotenv import load_dotenv

# # Charge le fichier .env s'il existe
# load_dotenv()

# class Settings(BaseSettings):
#     """Configuration de l'application avec variables d'environnement"""
    
#     # Configuration de base
#     app_name: str = "Obesity Prediction API"
#     app_version: str = "1.0.0"
#     debug: bool = False
    
#     # Base de données PostgreSQL
#     database_url: Optional[str] = None
#     postgres_user: str = "postgres"
#     postgres_password: str = "azerty"
#     postgres_db: str = "obesity"
#     postgres_host: str = "localhost"
#     postgres_port: int = 5432
    
#     # JWT Configuration
#     secret_key: str = "your-super-secret-jwt-key-change-this-in-production"
#     algorithm: str = "HS256"
#     access_token_expire_minutes: int = 30
    
#     # Machine Learning
#     model_path: str = "ml/obesity_model.pkl"
    
#     # Pagination
#     max_predictions_per_user: int = 100
    
#     class Config:
#         env_file = ".env"
    
#     @property
#     def database_url_full(self) -> str:
#         """Construit l'URL complète de la base de données"""
#         if self.database_url:
#             return self.database_url
        
#         return (
#             f"postgresql://{self.postgres_user}:{self.postgres_password}"
#             f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
#         )

# # Instance globale des paramètres
# settings = Settings()

# # Variables pour les catégories d'obésité (à adapter selon ton modèle)
# OBESITY_CATEGORIES = {
#     0: "Insufficient_Weight",
#     1: "Normal_Weight", 
#     2: "Overweight_Level_I",
#     3: "Overweight_Level_II",
#     4: "Obesity_Type_I",
#     5: "Obesity_Type_II",
#     6: "Obesity_Type_III"
# }

# # Features attendues par le modèle 
# EXPECTED_FEATURES = ["Age", "Height", "Weight", "history"]

"""
Configuration de l'application
Centralise toutes les variables d'environnement et constantes
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Charge le fichier .env s'il existe
load_dotenv()

class Settings(BaseSettings):
    """Configuration de l'application avec variables d'environnement"""
    
    # Configuration de base
    app_name: str = "Obesity Prediction API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Base de données PostgreSQL
    database_url: Optional[str] = None
    postgres_user: str = "obesity_user"
    postgres_password: str = "obesity_password"
    postgres_db: str = "obesity_db"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    
    # JWT Configuration
    secret_key: str = "your-super-secret-jwt-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Machine Learning
    model_path: str = "ml/obesity_model.pkl"
    
    # Pagination
    max_predictions_per_user: int = 100
    
    class Config:
        env_file = ".env"
    
    @property
    def database_url_full(self) -> str:
        """Construit l'URL complète de la base de données"""
        if self.database_url:
            return self.database_url
        
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

# Instance globale des paramètres
settings = Settings()

# Variables pour les catégories d'obésité (selon ton modèle et les métriques)
# Basé sur tes résultats : Insufficient_Weight, Normal_Weight, Obesity_Type_I, etc.
OBESITY_CATEGORIES = {
    0: "Insufficient_Weight",
    1: "Normal_Weight", 
    2: "Obesity_Type_I",
    3: "Obesity_Type_II",
    4: "Obesity_Type_III",
    5: "Overweight_Level_I",
    6: "Overweight_Level_II"
}

# Mapping alternatif si ton modèle utilise d'autres indices
# Tu peux changer ceci selon l'ordre réel de ton modèle
CLASS_TO_INDEX = {
    0: "Insufficient_Weight",
    1: "Normal_Weight", 
    2: "Overweight_Level_I",
    3: "Overweight_Level_II", 
    4: "Obesity_Type_I",
    5: "Obesity_Type_II",
    6: "Obesity_Type_III"
}

# Features attendues par ton modèle
EXPECTED_FEATURES = ["Age", "Height", "Weight", "history"]