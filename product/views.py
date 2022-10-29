from sqlalchemy.orm import Session

from .models import Product, ShoppingCart


def create_product_view(name: str, price: int, db: Session):
    return Product.create_product(name, price, db)


def get_product_view(name: str, db: Session):
    return Product.get_product(name, db)

def update_product_view(name: str, price: int, db: Session):
    return Product.update_product(name, price, db)

def delete_product_view(name: str, db: Session):
    return Product.delete_product(name, db)


def list_products_view(db: Session):
    return Product.get_all_products(db)


def list_active_products_view(db: Session):
    return Product.get_active_products(db)


def add_product_to_shopping_cart_view(user_id: int, product_id: int,
                                      db: Session):
    return ShoppingCart.add_product_to_shopping_cart(user_id, product_id, db)


def remove_product_from_shopping_cart_view(user_id: int, product_id: int,
                                           db: Session):
    return ShoppingCart.remove_product_from_shopping_cart(
        user_id, product_id, db)


def get_current_shopping_cart_view(user_id: int, db: Session):
    return ShoppingCart.get_current_shopping_cart(user_id, db)


def list_shopping_cart_paid_view(user_id: int, db: Session):
    return ShoppingCart.get_list_shopping_cart_paid(user_id, db)
