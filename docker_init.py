"""
Script d'initialisation pour Docker
Crée l'admin et teste la connexion
"""
import time
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

def wait_for_db():
    """Attend que la base de données soit prête"""
    from app.database import test_connection
    
    max_retries = 30
    retries = 0
    
    while retries < max_retries:
        if test_connection():
            print("✅ Connexion à la base de données OK")
            return True
        
        print(f"⏳ Attente de la base de données... ({retries + 1}/{max_retries})")
        time.sleep(2)
        retries += 1
    
    print("❌ Impossible de se connecter à la base de données")
    return False

def initialize_app():
    """Initialise l'application"""
    from app.database import create_tables
    from app.models.user import User, UserRole
    from app.services.auth_service import AuthService
    from app.database import SessionLocal
    
    # Attend la DB
    if not wait_for_db():
        sys.exit(1)
    
    # Crée les tables
    create_tables()
    print("✅ Tables créées")
    
    # Crée l'admin si il n'existe pas
    db = SessionLocal()
    try:
        admin_exists = db.query(User).filter(User.role == UserRole.ADMIN).first()
        
        if not admin_exists:
            admin_user = User(
                username="admin",
                email="admin@obesity.com",
                hashed_password=AuthService.hash_password("admin123"),
                role=UserRole.ADMIN,
                is_active=True
            )
            
            db.add(admin_user)
            db.commit()
            print("✅ Administrateur créé: admin/admin123")
        else:
            print("✅ Administrateur existe déjà")
    
    except Exception as e:
        db.rollback()
        print(f"❌ Erreur: {e}")
    
    finally:
        db.close()
    
    print("🚀 Application initialisée avec succès!")

if __name__ == "__main__":
    initialize_app()