"""
Configuration de la base de données PostgreSQL avec SQLAlchemy
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import logging
from sqlalchemy import text
from app.config import settings

# Logger pour le debug
logger = logging.getLogger(__name__)

# Création du moteur de base de données
engine = create_engine(
    settings.database_url_full)

# Session factory
SessionLocal = sessionmaker( autocommit=False,autoflush=False,bind=engine)

# Base pour les modèles SQLAlchemy
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    Générateur de session de base de données pour les endpoints FastAPI
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Erreur de base de données: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def create_tables():
    """Crée toutes les tables dans la base de données"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Tables créées avec succès")
    except Exception as e:
        logger.error(f"Erreur lors de la création des tables: {e}")
        raise

def test_connection():
    """Teste la connexion à la base de données"""
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        logger.info("Connexion à la base de données OK")
        return True
    except Exception as e:
        logger.error(f"Erreur de connexion à la base de données: {e}")
        return False
#tester la connexion
print(test_connection())