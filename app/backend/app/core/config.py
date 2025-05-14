from pydantic import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "petitedouceur"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    MONGODB_URL: str = "http://localhost:27017"
    DATABASE_NAME: str = "mongodb"

    class Config:
        env_file = ".env"

settings = Settings()
