# Étape 1 : Build de l'application React
FROM node:20 AS build

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm ci

COPY . .

RUN npm run build

# Étape 2 : Serveur nginx pour servir l'app statique de façon sécurisée
FROM nginx:alpine

# Copie des fichiers statiques compilés dans nginx
COPY --from=build /app/build /usr/share/nginx/html

# Suppression de la page d'accueil nginx par défaut
RUN rm /etc/nginx/conf.d/default.conf

# Ajout d'une config nginx sécurisée (CSP, headers sécurité)
COPY nginx.conf /etc/nginx/conf.d

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
