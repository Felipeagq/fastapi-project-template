# crear entorno virtual
```
python3 -m venv venv
```
# instalar dependencias
```
# requirements.txt
fastapi
uvicorn
starlette
pydantic_settings
python-dotenv
sqlalchemy
motor
psycopg2-binary
```

```
pip install -r requirements.txt
```
# crear ./entrypoint y ./app/settings/settings.py

```python
# ./entrypoint
from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from app.settings.settings import settings

app = FastAPI(
    title= settings.PROJECT_NAME,
    version= settings.PROJECT_VERSION,
    use_colors=True
)

@app.get("/")
def hello_check():
    return {
        "PROJECT_NAME": settings.PROJECT_NAME,
        "PROJECT_VERSION": settings.PROJECT_VERSION
    }

app.add_middleware(
    CORSMiddleware,
    allow_methods = ["*"],
    allow_headers = ["*"],
    allow_origins = ["*"],
    allow_credentials = True
)

if __name__ == "__main__":
    uvicorn.run(
        "entrypoint:app",
        host="localhost",
        port=8000,
        reload=True,
        log_level="info",
        use_colors=True
    )
```

```python
# ./app/settings/settings.py
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

```