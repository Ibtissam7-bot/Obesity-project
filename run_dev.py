"""
Script simple pour lancer l'application en développement
"""
import uvicorn
import os
from pathlib import Path

# Assure-toi que le fichier modèle existe
model_path = Path("ml/obesity_model.pkl")
if not model_path.exists():
    print("❌ ERREUR: Le fichier ml/obesity_model.pkl n'existe pas!")
    print("Place ton modèle dans le dossier ml/ et renomme-le obesity_model.pkl")
    exit(1)

print("✅ Modèle trouvé!")
print("🚀 Démarrage de l'API...")
print("📖 Documentation disponible sur: http://localhost:8000/docs")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Redémarre automatiquement si tu changes le code
        log_level="info"
    )