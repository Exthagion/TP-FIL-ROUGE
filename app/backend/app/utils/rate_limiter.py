from fastapi import Request, HTTPException
from collections import defaultdict
from time import time

login_attempts = defaultdict(list)
MAX_ATTEMPTS = 5
BLOCK_TIME = 300  # 5 minutes

def rate_limit(request: Request):
    ip = request.client.host
    current_time = time()
    attempts = login_attempts[ip]

    # Supprimer les essais
    login_attempts[ip] = [t for t in attempts if current_time - t < BLOCK_TIME]

    if len(login_attempts[ip]) >= MAX_ATTEMPTS:
        raise HTTPException(status_code=429, detail="Trop de tentatives de connexion, veuillez réessayer plus tard.")

    login_attempts[ip].append(current_time)
