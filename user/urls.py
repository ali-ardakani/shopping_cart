import re
from datetime import timedelta

from config.settings import ACCESS_TOKEN_EXPIRE_MINUTES, get_db
from fastapi import APIRouter, Depends, Request, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .models import ExpiredToken, User
from .schema import Token, UserRegister
from .views import Authenticate, get_current_active_user

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {
        "description": "Not found"
    }},
)


@router.post(
    "/register",
    status_code=201,
    summary="Register a new user",
    responses={
        201: {
            "description": "User registered successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "User {username} registered successfully"
                    }
                }
            }
        },
        400: {
            "description": "User already exists",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User/Email already exists Or invalid email"
                    }
                }
            }
        },
      
    }
    )
def register(user: UserRegister, db: Session = Depends(get_db)):
    # Check email is valid
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.fullmatch(regex, user.email):
        raise HTTPException(status_code=400, detail="Invalid email")
    user = User(
        username=user.username,
        email=user.email,
        hashed_password=Authenticate.get_password_hash(user.password),
        is_active=True,
    )
    user = User.create_user(user, db)
    return {"message": f"User {user.username} registered successfully"}


@router.delete(
    "/delete",
    status_code=status.HTTP_200_OK,
    summary="Delete a user",
    description="Delete logged in user",
    responses={
        401: {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Not authenticated"
                    }
                }
            }
        },
        404: {
            "description": "Not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User not found"
                    }
                }
            }
        },
        200: {
            "description": "Deleted logged in user",
            "content": {
                "application/json": {
                    "example": {
                        "message": "User {username} deleted successfully"
                    }
                }
            }
        },
    },
    )
def delete(current_user: User = Depends(get_current_active_user),
           db: Session = Depends(get_db)):
    User.delete_user(current_user.id, db)
    return {"message": f"User {current_user.username} deleted successfully"}


@router.post(
    "/token",
    response_model=Token,
    summary="Get access token",
    responses={
        401: {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Incorrect username or password"
                    }
                }
            }
        },
        200: {
            "description": "Access token",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "access_token",
                        "token_type": "bearer"
                    }
                }
            }
        },
    },
    )
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)):
    auth = Authenticate(form_data.username, form_data.password, db)
    user = auth.authenticate()
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = Authenticate.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="Logout user",
    responses={
        401: {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Not authenticated"
                    }
                }
            }
        },
        200: {
            "description": "Logged out user",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Logged out successfully"
                    }
                }
            }
        },
    },               
    )
def logout(current_user: User = Depends(get_current_active_user),
           db: Session = Depends(get_db),
           request: Request = None):
    token = request.headers["Authorization"].split(" ")[1]
    ExpiredToken.add_token(token, db)
    return {"message": "Logged out successfully"}
