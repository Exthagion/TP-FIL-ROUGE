from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash
from motor.motor_asyncio import AsyncIOMotorDatabase

async def get_user_by_email(db: AsyncIOMotorDatabase, email: str):
    return await db["users"].find_one({"email": email})

async def create_user(db: AsyncIOMotorDatabase, user_in: UserCreate):
    user = {
        "email": user_in.email,
        "hashed_password": get_password_hash(user_in.password),
        "is_active": True,
    }
    result = await db["users"].insert_one(user)
    user["_id"] = result.inserted_id
    return user

async def update_user(db: AsyncIOMotorDatabase, email: str, user_in: UserUpdate):
    update_data = user_in.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    await db["users"].update_one({"email": email}, {"$set": update_data})
    return await get_user_by_email(db, email)

async def delete_user(db: AsyncIOMotorDatabase, email: str):
    await db["users"].delete_one({"email": email})
