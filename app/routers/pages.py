# app/api/routes/pages.py

from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from auth import get_current_user
from ..schemas.user import TokenData

# Assurez-vous d'avoir un dossier 'templates' à la racine de votre projet
templates = Jinja2Templates(directory="templates")

router = APIRouter(tags=["Frontend"])

@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.get("/app", response_class=HTMLResponse)
async def app_obesity_page(request: Request, user: TokenData = Depends(get_current_user)):
    # La dépendance get_current_user gère l'authentification.
    # Si le token est invalide, une 401 sera levée automatiquement.
    return templates.TemplateResponse("app_obesity.html", {"request": request})

@router.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request, user: TokenData = Depends(get_current_user)):
    # Vérification du rôle pour l'accès à la page
    # Le rôle est maintenant dans le TokenData, pas directement dans le UserDB
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Accès refusé.")
    return templates.TemplateResponse("admin.html", {"request": request})