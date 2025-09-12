# 🏥 Obesity Prediction API
API complète de prédiction d'obésité avec Machine Learning, authentification JWT et interface d'administration.

**Réalisé par : SANNAKY Ibtissam**

**Courriel: bissamsannaky@gmail.com**

# 🚀 Fonctionnalités

🤖 Prédiction ML : Modèle RandomForest pour classifier les types d'obésité

🔐 Authentification JWT : Connexion sécurisée avec tokens

📊 Interface web : Pages HTML pour utiliser l'API facilement

👑 Panel Admin : Gestion des utilisateurs et statistiques

📈 Historique : Sauvegarde des prédictions par utilisateur

🐳 Docker Ready : Déploiement avec Docker Compose

🏗️ Architecture

├── app/                    # Code principal FastAPI

│   ├── models/            # Modèles SQLAlchemy (User, Prediction)

│   ├── schemas/           # Validation Pydantic

│   ├── routers/           # Endpoints API

│   ├── services/          # Logique métier (Auth, ML)

│   └── static/templates/  # Pages HTML

├── ml/                    # Modèle Machine Learning et fichiers associés

└── docker-compose.yml     # Configuration Docker

└── Dockerfile    # Configuration Docker

└── requirements.txt     # Configuration Docker

## 📋 Features d'entrée
Le modèle utilise ces caractéristiques pour prédire l'obésité :

Age : Âge en années

Height : Taille en cm

Weight : Poids en kg

history : Hérédité familiale (0=Non, 1=Oui)

Consumption of vegetables (FCVC)

Number of main meals (NCP)

Daily water consumption (CH2O)

Frequency of physical activity (FAF)

Time spent using electronic devices (TUE)

Alcohol consumption (CALC)

## 🎯 Classes de sortie

Insufficient_Weight

Normal_Weight

Obesity_Type_I

Obesity_Type_II

Obesity_Type_III

Overweight_Level_I

Overweight_Level_II

## 🚀 Démarrage rapide
**Option 1 : Docker Compose (Recommandé)**

Clone le projet

git clone https://github.com/Ibtissam7-bot/Obesity-project.git

cd Obesity-project

**Configuration de la base de données**

Modifie le fichier .env selon tes paramètres

**Crée l'admin par défaut**

python create_admin.py

**Lance l'application localement à travers:** uvicorn app.main:app --reload

## Démarrage avec Docker
#### 1. Télécharger l'image
docker pull bissam7dock/obesity:latest

#### 2.Lancer l'application
docker run -d -p 8000:8000 bissam7dock/obesity:latest

#### 3. Tester sur http://localhost:8000

**Accède à l'application**
 Home: http://localhost:8000/pages/home
 Interface : http://localhost:8000/pages/login  
 API Docs : http://localhost:8000/docs

# Démarre l'application
📱 Utilisation
1. Connexion Admin par défaut

URL : http://localhost:8000/pages/login
Username : admin
Password : admin123

2. Créer un utilisateur

URL : http://localhost:8000/pages/register
Remplis le formulaire d'inscription

3. Faire une prédiction

URL : http://localhost:8000/pages/app
Connecte-toi et remplis le formulaire
Ou clique sur "Test rapide" pour tester

4. Interface Admin

URL : http://localhost:8000/pages/admin
Gestion des utilisateurs et statistiques

🔧 API Endpoints
**Authentification**

POST /auth/register - Inscription
POST /auth/login - Connexion
GET /auth/me - Info utilisateur actuel

**Prédictions**

POST /predict/ - Nouvelle prédiction

GET /predict/history - Historique personnel

GET /predict/metrics - Informations du modèle

**Administration (Admin uniquement)**

GET /admin/users - Liste des utilisateurs

DELETE /admin/users/{id} - Supprimer un utilisateur

GET /admin/stats - Statistiques générales

### 🐳 Docker Hub
Image disponible sur Docker Hub

bashdocker pull bissam7dock/obesity:latest


#### Test avec les pages HTML
**Aller sur http://localhost:8000/pages/app**, puis faire un test rapide.

## 📊 Métriques du modèle utilisé
Le modèle RandomForest obtient d'excellentes performances :

Accuracy : ~97%
Precision/Recall : >90% pour toutes les classes
Features :   10 caractéristiques simples mais efficaces

