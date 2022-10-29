from config.settings import Base
from fastapi.exceptions import HTTPException
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import Session, relationship


class ShoppingCart(Base):
    __tablename__ = "shopping_cart"

    id = Column(Integer, primary_key=True, index=True)
    orders = relationship("Order", backref="shopping_cart")
    user_id = Column(Integer, ForeignKey("users.id"))
    completed = Column(Boolean, default=False)

    @staticmethod
    def get_shopping_cart(user_id: int, db: Session):
        shopping_cart = db.query(ShoppingCart).filter(
            ShoppingCart.user_id == user_id).first()
        return shopping_cart

    @staticmethod
    def get_current_shopping_cart(user_id: int, db: Session):
        shopping_cart = db.query(ShoppingCart).filter(
            ShoppingCart.user_id == user_id,
            ShoppingCart.completed == False).first()
        if not shopping_cart:
            raise HTTPException(status_code=404, detail="Shopping cart not found")
        return shopping_cart.orders

    @staticmethod
    def get_list_shopping_cart_paid(user_id: int, db: Session):
        shopping_cart = db.query(ShoppingCart).filter(
            ShoppingCart.user_id == user_id,
            ShoppingCart.completed == True).all()
        return shopping_cart

    @staticmethod
    def create_shopping_cart(user_id: int, db: Session):
        shopping_cart = ShoppingCart(user_id=user_id)
        db.add(shopping_cart)
        db.commit()
        db.refresh(shopping_cart)
        return shopping_cart

    @staticmethod
    def add_product_to_shopping_cart(user_id: int, product_id: int,
                                     db: Session):
        shopping_cart = db.query(ShoppingCart).filter(
            ShoppingCart.user_id == user_id,
            ShoppingCart.completed == False).first()
        if not shopping_cart:
            shopping_cart = ShoppingCart.create_shopping_cart(user_id, db)
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=400, detail="Product not found")
        if not product.is_active:
            raise HTTPException(status_code=400,
                                detail="Product is not active")
        order = Order.create_order(product_id, shopping_cart.id, db)
        shopping_cart.orders.append(order)
        db.commit()
        db.refresh(shopping_cart)
        return shopping_cart

    @staticmethod
    def remove_product_from_shopping_cart(user_id: int, product_id: int,
                                          db: Session):
        shopping_cart = db.query(ShoppingCart).filter(
            ShoppingCart.user_id == user_id,
            ShoppingCart.completed == False).first()
        if not shopping_cart:
            return shopping_cart
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=400, detail="Product not found")
        order = Order.get_orders(product_id, shopping_cart.id, db)
        if not order:
            raise HTTPException(status_code=400, detail="Order not found")
        for item in order:
            db.delete(item)
        db.commit()
        db.refresh(shopping_cart)
        return shopping_cart
    
class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    paid = Column(Boolean, default=False)
    shopping_cart_id = Column(Integer, ForeignKey("shopping_cart.id"))
    
    @staticmethod
    def create_order(product_id: int, user_id: int, db: Session):
        order = Order(product_id=product_id, user_id=user_id)
        db.add(order)
        db.commit()
        db.refresh(order)
        return order
    
    @staticmethod
    def get_orders(product_id: int, user_id: int, db: Session):
        order = db.query(Order).filter(Order.product_id == product_id,
                                       Order.user_id == user_id).all()
        return order

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    price = Column(Float)
    is_active = Column(Boolean, default=True)

    @staticmethod
    def get_product(name: str, db: Session):
        product = db.query(Product).filter(Product.name.ilike(name)).first()
        if not product:
            raise HTTPException(status_code=400, detail="Product not found")
        return product

    @staticmethod
    def get_all_products(db: Session):
        return db.query(Product).all()

    @staticmethod
    def get_active_products(db: Session):
        return db.query(Product).filter(Product.is_active == True).all()

    @staticmethod
    def create_product(name: str, price: int, db: Session):
        product = Product(name=name, price=price)
        db.add(product)
        db.commit()
        db.refresh(product)
        return product
    
    @staticmethod
    def update_product(name: str, price: int, db: Session):
        product = Product.get_product(name, db)
        product.price = price
        db.commit()
        db.refresh(product)
        return product
    
    @staticmethod
    def delete_product(name: str, db: Session):
        product = Product.get_product(name, db)
        product.is_active = False
        db.commit()
        db.refresh(product)
        return product
