"""
Router pour servir les pages HTML
Code simple pour servir les templates
"""
from fastapi import APIRouter
from fastapi.responses import FileResponse
from pathlib import Path

# Router pour les pages HTML
router = APIRouter(prefix="/pages", tags=["Pages HTML"])

# # Chemin vers les templates
# TEMPLATES_DIR = Path(__file__).parent.parent / "static" / "templates"
TEMPLATES_DIR = Path("app/static/templates")

@router.get("/home")
def app_obesity_page():
    """Page d'acceuil d'application """
    return FileResponse(TEMPLATES_DIR / "home.html")

@router.get("/login")
def login_page():
    """Page de connexion"""
    return FileResponse(TEMPLATES_DIR / "login.html")

@router.get("/register")
def register_page():
    """Page d'inscription"""
    return FileResponse(TEMPLATES_DIR / "register.html")

@router.get("/app")
def app_obesity_page():
    """Page principale d'application (prédiction d'obésité)"""
    return FileResponse(TEMPLATES_DIR / "app_obesity.html")

@router.get("/admin")
def admin_page():
    """Page d'administration"""
    return FileResponse(TEMPLATES_DIR / "admin.html")