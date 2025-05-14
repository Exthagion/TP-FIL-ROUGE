from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import User, UserUpdate
from app.api.deps import get_current_user, get_db
from app.crud.user import get_user_by_email, update_user, delete_user
from motor.motor_asyncio import AsyncIOMotorDatabase
from .schemas import UserUpdate, UserOut
from .models import User
from .database import get_db
from .dependencies import get_current_user

router = APIRouter()

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=User)
async def update_user_me(user_in: UserUpdate, db: AsyncIOMotorDatabase = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = await update_user(db, current_user.email, user_in)
    return user

@router.delete("/me")
async def delete_user_me(db: AsyncIOMotorDatabase = Depends(get_db), current_user: User = Depends(get_current_user)):
    await delete_user(db, current_user.email)
    return {"msg": "User deleted"}

@router.put("/users/me", response_model=UserOut)
def update_user(user_update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_data = user_update.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(current_user, key, value)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.delete("/users/me")
def delete_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db.delete(current_user)
    db.commit()
    return {"detail": "Compte supprimé avec succès"}

