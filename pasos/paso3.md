# Creación de modelos para base de datos 
```python
# ./app/models/models.py

from sqlalchemy import Column, String, Integer, ForeignKey
from app.database.postgres.database import Base

from sqlalchemy.orm import relationship

class BlogModel(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer,ForeignKey("users.id"))
    date = Column(String)
    creator = relationship("UserModel", back_populates="blogs")



class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(String, nullable=False)
    blogs = relationship("BlogModel", back_populates="creator")
```



# se modifica el entrypoint creando la base de datos 
```python
from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from app.settings.settings import settings

app = FastAPI(
    title= settings.PROJECT_NAME,
    version= settings.PROJECT_VERSION,
    use_colors=True
)

# ADD
from app.models.models import *
from app.database.postgres.database import engine
Base.metadata.create_all(bind=engine)

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