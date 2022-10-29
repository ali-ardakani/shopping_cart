from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    price: float

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Product 1",
                "price": 100.0,
            }
        }
        
class ProductName(BaseModel):
    name: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Product 1",
            }
        }
        
class ProductID(BaseModel):
    id: int
