Projet Fil Rouge
Réalisé avec Python (utilisé beaucoup depuis le début de l'année, je suis plutôt à l'aise avec contrairement à d'autres languages), React, JavaScript
Listes des ressources primaires utilisées :
React
axios
fastapi
pydantic
datetime
AsyncIOMotorDatabase
sqlalchemy.orm

J'ai utilisé Docker pour ma BDD (sur MongoDB)

Pour ce qui est de la sécurisation de ma plateforme, j'ai choisi d'ajouter :
rate_limiter.py : un rate limiter (bloquer les essais de connexion trop nombreux)
validators.py : un validateur (pour bloquer les requêtes non conformes et empêcher les injections SQL """basique""")
deps.py : un système de token avec JWT qui utilise un secret et un algorithme

Ce qu'il me manque et que j'aimerais beaucoup faire :
Arriver à faire fonctionner mon backend
un MakeFile (pour tester mon infra)
Test Top10 OWASP via cron ou une autre solution
Une seedfile

Problèmes rencontrés :
Difficultés sur Docker, utilisation et lacunes personnelles
Impossible de lancer mon infra dans sa totalité, il me manque encore de nombreuses compétences à acquérir (surtout en docker et en front)
