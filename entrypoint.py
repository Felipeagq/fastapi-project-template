from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from app.settings.settings import settings

app = FastAPI(
    title= settings.PROJECT_NAME,
    version= settings.PROJECT_VERSION,
    use_colors=True
)
from app.models.models import *
from app.database.postgres.database import engine
Base.metadata.create_all(bind=engine)

from app.routes import user_route
from app.routes import book_route

@app.get("/")
def hello_check():
    return {
        "PROJECT_NAME": settings.PROJECT_NAME,
        "PROJECT_VERSION": settings.PROJECT_VERSION
    }

app.include_router(user_route.router,prefix="/user")
app.include_router(book_route.router,prefix="/book")

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