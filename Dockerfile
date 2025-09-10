# # Image de base Python 3.11 slim
# FROM python:3.11-slim

# # Variables d'environnement
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# # Définit le répertoire de travail
# WORKDIR /app

# # Installe les dépendances système
# RUN apt-get update && apt-get install -y \
#     gcc \
#     && rm -rf /var/lib/apt/lists/*

# # Copie et installe les dépendances Python
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copie le code source
# COPY . . 
# COPY docker_init.py .

# # Crée un utilisateur non-root
# RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
# USER appuser

# # Expose le port
# EXPOSE 8000

# # Script de démarrage
# COPY --chown=appuser:appuser start.sh /app/start.sh
# RUN chmod +x /app/start.sh

# # Commande par défaut
# CMD ["/app/start.sh"]
# ObesiTrack/Dockerfile

FROM python:3.11-slim

# Définir le répertoire de travail dans le conteneur.
# C'est ici que l'application Python sera exécutée.
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Installer les dépendances système (si nécessaire)
RUN apt-get update && apt-get install -y build-essential libpq-dev gfortran libopenblas-dev liblapack-dev

RUN python -m pip install --upgrade pip
# RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Copier le fichier de dépendances depuis l'hôte (maintenant ObesiTrack/requirements.txt)
# vers /app/requirements.txt dans le conteneur.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code de l'application (le dossier 'app' de l'hôte)
# vers le répertoire /app/app dans le conteneur.
# Vous devez copier le contenu du répertoire 'app' de l'hôte
# vers un sous-répertoire 'app' dans le WORKDIR du conteneur.
COPY app/ ./app/
 # <--- Copie le dossier ObesiTrack/app/ vers /app/app/ du conteneur

# Copier le script start.sh si vous l'utilisez
# Il se trouve à la racine du contexte (ObesiTrack/start.sh)
COPY start.sh .
 # Copie start.sh dans /app/
RUN chmod +x /app/start.sh


# Si vous voulez créer un utilisateur non-root
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Exposer le port de l'application
EXPOSE 8000

# Commande pour démarrer l'application.
# Utilise le script start.sh que nous avons copié.
CMD ["./start.sh"]