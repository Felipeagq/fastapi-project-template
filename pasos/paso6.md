# Routas de usuairos
```python 
# ./app/routes/user_route.py

from fastapi import APIRouter, Depends, status, HTTPException

from app.database.postgres.database import get_db
from app.models.models import UserModel, BlogModel
from sqlalchemy.orm import Session

from app.schemas.userSchemas import UserCreate, PostCreate

from app.settings.security import *

router = APIRouter(tags=["User Managment"])

@router.post("/register")
def register(user: UserCreate,db: Session = Depends(get_db)):
    if db.query(UserModel).filter_by(username=user.username).first():
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    data = user.model_dump()
    data["password"] = hash_password(data["password"])
    new_user = UserModel(**data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
 
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter_by(username=form_data.username).first()
    if not user or user.password != hash_password(form_data.password):
        return {"message":"Credenciales invalidas"}
    token = create_token(user.id)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/users/{user_id}")
def me(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        return {"message":"usuario no encontrado"}
    return user

@router.delete("/users/{user_id}")
def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        return {"message":"usuario no encontrado"}
    db.delete(user)
    db.commit()
    return {"message": f"Usuario con ID {user_id} eliminado",
            "user":user}

@router.get("/list")
def users_lists( db: Session = Depends(get_db),current_user: UserModel = Depends(require_roles("admin"))):
    user = db.query(UserModel).all()
    return user


@router.get("/adminroute")
def admin_route( db: Session = Depends(get_db),current_user: UserModel = Depends(require_roles("admin"))):
    return "eres admin"

@router.get("/userroute")
def user_route( db: Session = Depends(get_db),current_user: UserModel = Depends(require_roles("user"))):
    return "eres user"

@router.get("/useradminroute")
def user_admin_route( db: Session = Depends(get_db),current_user: UserModel = Depends(require_roles("user","admin"))):
    return "eres user o admin"



@router.post("/posts/")
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(require_roles("admin","user"))):
    new_post = BlogModel(
        title=post.title, # titulo al post
        content=post.content,  # contenido al post
        user_id=current_user.id # al usuario loggeado
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

    
@router.get("/posts/")
def get_my_posts(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return db.query(BlogModel).filter_by(user_id=current_user.id).all()


@router.get("/protected/admin-area")
def admin_area(current_user: UserModel = Depends(require_roles("admin"))):
    return {
        "msg": "Welcome to the admin area",
        "data":current_user
    }

@router.get("/protected/admin-user-area")
def admin_user_area(current_user: UserModel = Depends(require_roles("admin","user"))):
    return {
        "msg": "Welcome to the admin user area",
        "data":current_user
        }

@router.get("/protected/user-area")
def user_area(current_user: UserModel = Depends(require_roles("user"))):
    return {
        "msg": "Welcome to the user area",
        "data":current_user
        }

```