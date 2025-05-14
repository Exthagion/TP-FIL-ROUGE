from app.db.base import db

async def init_db():
    await db["users"].create_index("email", unique=True)