# Utilisation d'une image officielle Python avec des librairies système minimales
FROM python:3.11-slim

# Variables d'environnement sécurisées
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Installation des dépendances système essentielles
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Créer et utiliser un user non-root
RUN useradd -ms /bin/bash appuser
WORKDIR /home/appuser/app
USER appuser

# Copier les fichiers
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser . .

# Exposer le port d'écoute
EXPOSE 8000

# Commande pour démarrer l'API avec Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
