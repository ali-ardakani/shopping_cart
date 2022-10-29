from config.settings import get_db
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from user.models import User
from user.views import get_current_active_user

from .schema import ProductCreate, ProductID, ProductName
from .views import (add_product_to_shopping_cart_view, create_product_view,
                    get_current_shopping_cart_view, get_product_view,
                    list_active_products_view, list_products_view,
                    list_shopping_cart_paid_view,
                    remove_product_from_shopping_cart_view,
                    update_product_view, delete_product_view)

router = APIRouter(
    prefix="/product",
    tags=["product"],
    responses={404: {
        "description": "Not found"
    }},
)


@router.post("/create",
             status_code=status.HTTP_201_CREATED,
             summary="Create a new product",
             responses={
                 201: {
                     "description": "Product created successfully",
                     "content": {
                         "application/json": {
                             "example": {
                                 "message":
                                 "Product {name} created successfully"
                             }
                         }
                     }
                 },
                 400: {
                     "description": "Product already exists",
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "Product already exists"
                             }
                         }
                     }
                 },
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
             })
def create_product(product: ProductCreate,
                   current_user: User = Depends(get_current_active_user),
                   db: Session = Depends(get_db)):
    product = create_product_view(product.name, product.price, db)
    return {"message": f"Product {product.name} created successfully"}


@router.post("/info",
             status_code=status.HTTP_200_OK,
             summary="Get product info",
             responses={
                 200: {
                     "description": "Product info",
                     "content": {
                         "application/json": {
                             "example": {
                                 "id": 1,
                                 "name": "Product name",
                                 "price": 100.0,
                                 "is_active": True
                             }
                         }
                     }
                 },
                 404: {
                     "description": "Not found",
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "Product not found"
                             }
                         }
                     }
                 },
             })
def get_product(product: ProductName, db: Session = Depends(get_db)):
    product = get_product_view(product.name, db)
    return product


@router.put(
    "/update",
    status_code=status.HTTP_200_OK,
    summary="Update product info",
    responses={
        200: {
            "description": "Product updated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message":
                        "Product {name} updated successfully; new price: {price}"
                    }
                }
            }
        },
        404: {
            "description": "Not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Product not found"
                    }
                }
            }
        },
    })
def update_product(product: ProductCreate,
                   current_user: User = Depends(get_current_active_user),
                   db: Session = Depends(get_db)):
    product = update_product_view(product.name, product.price, db)
    return {
        "message":
        f"Product {product.name} updated successfully; new price: {product.price}"
    }


@router.delete("/delete",
               status_code=status.HTTP_200_OK,
               summary="Delete a product",
               responses={
                   200: {
                       "description": "Product deleted successfully",
                       "content": {
                           "application/json": {
                               "example": {
                                   "message":
                                   "Product {name} deleted successfully"
                               }
                           }
                       }
                   },
                   404: {
                       "description": "Not found",
                       "content": {
                           "application/json": {
                               "example": {
                                   "detail": "Product not found"
                               }
                           }
                       }
                   },
               })
def delete_product(product: ProductName,
                   current_user: User = Depends(get_current_active_user),
                   db: Session = Depends(get_db)):
    product = delete_product_view(product.name, db)
    return {"message": f"Product {product.name} deleted successfully"}


@router.get("/list",
            status_code=status.HTTP_200_OK,
            summary="List all products",
            responses={
                200: {
                    "description": "List of products",
                    "content": {
                        "application/json": {
                            "example": [{
                                "id": 1,
                                "name": "Product name 1",
                                "price": 100.0,
                                "is_active": True
                            }, {
                                "id": 2,
                                "name": "Product name 2",
                                "price": 100.0,
                                "is_active": False
                            }]
                        }
                    }
                },
            })
def list_products(db: Session = Depends(get_db)):
    products = list_products_view(db)
    return products


@router.get("/list_active",
            status_code=status.HTTP_200_OK,
            summary="List all active products",
            responses={
                200: {
                    "description": "List of active products",
                    "content": {
                        "application/json": {
                            "example": [
                                {
                                    "id": 1,
                                    "name": "Product name",
                                    "price": 100.0,
                                    "is_active": True
                                },
                            ]
                        }
                    }
                },
            })
def list_active_products(db: Session = Depends(get_db)):
    products = list_active_products_view(db)
    return products


@router.post("/add-to-cart",
             status_code=status.HTTP_200_OK,
             summary="Add product to shopping cart",
             responses={
                 200: {
                     "description":
                     "Product added to shopping cart successfully",
                     "content": {
                         "application/json": {
                             "example": {
                                 "message":
                                 "Product added to shopping cart successfully"
                             }
                         }
                     }
                 },
                 404: {
                     "description": "Not found",
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "Product not found"
                             }
                         }
                     }
                 }
             })
def add_product_to_shopping_cart(
    product: ProductID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)):
    add_product_to_shopping_cart_view(current_user.id, product.id, db)
    return {"message": "Product added to shopping cart successfully"}


@router.post(
    "/remove-from-cart",
    status_code=status.HTTP_200_OK,
    summary="Remove product from shopping cart",
    responses={
        200: {
            "description": "Product removed from shopping cart successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message":
                        "Product removed from shopping cart successfully"
                    }
                }
            }
        },
        404: {
            "description": "Not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Product not found"
                    }
                }
            }
        }
    })
def remove_product_from_shopping_cart(
    product: ProductID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)):
    remove_product_from_shopping_cart_view(current_user.id, product.id, db)
    return {"message": "Product removed from shopping cart successfully"}


@router.get("/shopping-cart",
            status_code=status.HTTP_200_OK,
            summary="Open shopping cart information",
            responses={
                200: {
                    "description": "Shopping cart information",
                    "content": {
                        "application/json": {
                            "example": [{
                                "paid": False,
                                "id": 1,
                                "user_id": 1,
                                "shopping_cart_id": 1,
                                "product_id": 1
                            }]
                        }
                    }
                },
            })
def get_current_shopping_cart(
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)):
    shopping_cart = get_current_shopping_cart_view(current_user.id, db)
    return shopping_cart


@router.get(
    "/shopping-cart-paid",
    status_code=status.HTTP_200_OK,
    summary="paid shopping cart information",
    responses={
        200: {
            "description": "Shopping cart information",
            "content": {
                "application/json": { 
                    "example": [{
                        "id": 1,
                        "user_id": 1,
                        "orders": [1, 2, 3],
                        "completed": True
                    }]
                }
            }
        },
    })
def list_shopping_cart_paid(
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)):
    shopping_cart = list_shopping_cart_paid_view(current_user.id, db)
    return shopping_cart
