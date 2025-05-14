from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Dict
from .schemas import Token, LoginInput
from .security import authenticate_user, create_access_token
from app.schemas.user import UserCreate, User
from app.crud.user import get_user_by_email, create_user
from app.core.security import verify_password, create_access_token
from app.api.deps import get_db
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter()

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/login", response_model=Token)
async def login(user_in: UserCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    user = await get_user_by_email(db, user_in.email)
    if not user or not verify_password(user_in.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=User)
async def register(user_in: UserCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    existing_user = await get_user_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = await create_user(db, user_in)
    return user

router = APIRouter()

# Dictionnaire pour suivre les tentatives de connexion
login_attempts: Dict[str, Dict[str, any]] = {}

MAX_ATTEMPTS = 5
LOCKOUT_TIME = timedelta(minutes=15)

@router.post("/login", response_model=Token)
def login(form_data: LoginInput):
    email = form_data.email
    now = datetime.utcnow()

    # Vérifier si l'utilisateur est verrouillé
    if email in login_attempts:
        attempts = login_attempts[email]
        if attempts["count"] >= MAX_ATTEMPTS:
            if now - attempts["last_attempt"] < LOCKOUT_TIME:
                raise HTTPException(status_code=403, detail="Trop de tentatives. Réessayez plus tard.")
            else:
                # Réinitialiser les tentatives après le verrouillage
                login_attempts[email] = {"count": 0, "last_attempt": now}

    user = authenticate_user(email, form_data.password)
    if not user:
        # Incrémenter le compteur de tentatives
        if email not in login_attempts:
            login_attempts[email] = {"count": 1, "last_attempt": now}
        else:
            login_attempts[email]["count"] += 1
            login_attempts[email]["last_attempt"] = now
        raise HTTPException(status_code=400, detail="Identifiants invalides")

    # Réinitialiser les tentatives après une connexion réussie
    if email in login_attempts:
        del login_attempts[email]

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
