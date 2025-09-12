"""
Script pour transformer un utilisateur existant en admin
"""
import sys
from pathlib import Path

# Ajoute le répertoire parent au path
sys.path.append(str(Path(__file__).parent))

from app.database import SessionLocal
from app.models.user import User, UserRole

def make_user_admin():
    """Transforme un utilisateur en admin"""
    
    db = SessionLocal()
    
    try:
        # Demande le nom d'utilisateur
        username = input("Entrez le nom d'utilisateur à transformer en admin: ")
        
        # Trouve l'utilisateur
        user = db.query(User).filter(User.username == username).first()
        
        if not user:
            print(f"❌ Utilisateur '{username}' non trouvé")
            return
        
        # Transforme en admin
        user.role = UserRole.ADMIN
        db.commit()
        
        print(f"✅ Utilisateur '{username}' est maintenant administrateur!")
        print(f"   Email: {user.email}")
        print(f"   Rôle: {user.role}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erreur: {e}")
    
    finally:
        db.close()

if __name__ == "__main__":
    make_user_admin()