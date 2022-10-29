from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str
    
class AccessToken(BaseModel):
    access_token: str

class TokenData(BaseModel):
    username: str | None = None
    
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "password": "password"
            }
        }
        
class UserRegister(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@email.com",
                "password": "password"
            }
        }