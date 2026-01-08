from sqlalchemy import Column, String, Integer, ForeignKey
from app.database.postgres.database import Base

from sqlalchemy.orm import relationship

class BlogModel(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("UserModel", back_populates="blogs")



class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(String, nullable=False)
    blogs = relationship("BlogModel", back_populates="creator")