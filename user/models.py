from config.settings import Base
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Integer, String
        
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email}, is_active={self.is_active})"
    
    @staticmethod
    def get_user(username: str, db: Session):
        user = db.query(User).filter(User.username.ilike(username)).first()
        return user
    
    @staticmethod
    def create_user(user: "User", db: Session):
        if db.query(User).filter(User.username.ilike(user.username)).first():
            raise HTTPException(status_code=400, detail="User already exists")
        if db.query(User).filter(User.email.ilike(user.email)).first():
            raise HTTPException(status_code=400, detail="Email already exists")
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def delete_user(id: int, db: Session):
        user = db.query(User).filter(User.id == id).first()
        db.delete(user)
        db.commit()
        return user
    
    @staticmethod
    def update_user(id: int, user: BaseModel, db: Session):
        user = db.query(User).filter(User.id == id).first()
        for key, value in user.dict().items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def get_users(db: Session):
        users = db.query(User).all()
        return users

class ExpiredToken(Base):
    __tablename__ = "expired_tokens"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    
    def __repr__(self):
        return f"ExpiredToken(id={self.id}, token={self.token})"
    
    @staticmethod
    def get_expired_token(token: str, db: Session):
        expired_token = db.query(ExpiredToken).filter(ExpiredToken.token == token).first()
        return expired_token
    
    @staticmethod
    def add_token(token: str, db: Session):
        if db.query(ExpiredToken).filter(ExpiredToken.token == token).first():
            raise HTTPException(status_code=400, detail="Token already exists")
        expired_token = ExpiredToken(token=token)
        db.add(expired_token)
        db.commit()
        db.refresh(expired_token)
        return token
    
    @staticmethod
    def get_expired_tokens(db: Session):
        expired_tokens = db.query(ExpiredToken).all()
        return expired_tokens