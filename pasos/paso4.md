# configuración de seguridad
```python 
# ./app/settings/security.py
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
import hashlib
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session


from app.settings.settings import settings
from app.database.postgres.database import get_db
from app.models.models import UserModel


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_token(user_id: int) -> str:
    return jwt.encode({"user_id": user_id}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("user_id")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    user = db.query(UserModel).filter_by(id=user_id).first()
    if not user:
        return {"message":"usuario no encontrado"}
    return user


def require_roles(*roles):
    def role_checker(user: UserModel = Depends(get_current_user)):
        user_roles_names = user.role
        if not any(r in user_roles_names for r in roles):
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return user
    return role_checker
```