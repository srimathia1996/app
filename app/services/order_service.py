import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.models import Order, OrderItem, Product
from app.utils.logger import logger


def create_order(db: Session, user_id: str, items: list):
    try:
        logger.info(f"Creating order for user {user_id}")

        total_amount = 0
        tax_amount = 5000
        shipping_amount = 50

        order_items_data = []

        # 🔒 Lock products (prevent overselling)
        for item in items:
            product = db.query(Product)\
                .filter(Product.id == item.product_id)\
                .with_for_update()\
                .first()

            if not product:
                logger.error(f"Product not found: {item.product_id}")
                raise HTTPException(status_code=404, detail="Product not found")

            if product.stock_quantity < item.quantity:
                logger.error(f"Insufficient stock for product {product.id}")
                raise HTTPException(status_code=400, detail="Insufficient stock")

            item_total = product.price * item.quantity
            total_amount += item_total

            order_items_data.append({
                "product": product,
                "quantity": item.quantity,
                "price": product.price
            })

        # 🧾 Create Order
        order = Order(
            id=str(uuid.uuid4()),
            user_id=user_id,
            total_amount=total_amount + tax_amount + shipping_amount,
            tax_amount=tax_amount,
            shipping_amount=shipping_amount,
            status="PENDING"
        )

        db.add(order)
        db.flush()  # get order.id

        # 🧾 Create Order Items
        for item in order_items_data:
            order_item = OrderItem(
                id=str(uuid.uuid4()),
                order_id=order.id,
                product_id=item["product"].id,
                quantity=item["quantity"],
                price=item["price"]
            )
            db.add(order_item)

        db.commit()
        db.refresh(order)

        logger.info(f"Order created successfully: {order.id}")

        return order

    except Exception as e:
        db.rollback()
        logger.error(f"Order creation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


def get_order(db: Session, order_id: str):
    try:
        order = db.query(Order).filter(Order.id == order_id).first()

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        return order

    except Exception as e:
        logger.error(f"Fetch order failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))