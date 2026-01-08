from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI SQLALCHEMY CRUD"
    PROJECT_VERSION: str = "v0.0.1"
    API_V1_STR: str = "/api/v1"

    SQLALCHEMY_DATABASE_URL: str = os.getenv("SQLALCHEMY_DATABASE_URL") or "postgresql://postgres:postgres@localhost:5433"
    MONGO_DATABASE_URL: str = os.getenv("MONGO_DATABASE_URL") or "mongodb://root:example@localhost:27018/"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*3
    ALGORITHM: str = "HS256"
    # SECRET_KEY: str = os.urandom(12).hex()
    SECRET_KEY: str =  os.getenv("SECRET_KEY") or "13cd6d096247d567f4723da4"

settings = Settings()


