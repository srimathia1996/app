import uuid
import os
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.models import Payment, Order, Product, OrderItem
from app.utils.logger import logger

SECRET = os.getenv("WEBHOOK_SECRET", "mysecret")


# ✅ INITIATE PAYMENT
def initiate_payment(db: Session, order_id: str, idempotency_key: str):
    try:
        logger.info(f"Initiating payment for order {order_id}")

        # 🔍 Check order
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        # 🔁 Idempotency check
        existing_payment = db.query(Payment).filter(
            Payment.idempotency_key == idempotency_key
        ).first()

        if existing_payment:
            logger.info(f"Returning existing payment for key {idempotency_key}")
            return {
                "payment_id": existing_payment.id,
                "status": existing_payment.payment_status
            }

        # 💳 Create payment
        payment = Payment(
            id=str(uuid.uuid4()),
            order_id=order_id,
            payment_gateway_id="mock_" + str(uuid.uuid4()),
            payment_status="INITIATED",
            amount=order.total_amount,
            currency="INR",
            idempotency_key=idempotency_key
        )

        db.add(payment)
        db.commit()
        db.refresh(payment)

        logger.info(f"Payment created: {payment.id}")

        return {
            "payment_id": payment.id,
            "status": payment.payment_status
        }

    except IntegrityError:
        db.rollback()

        # 🔁 Fetch existing after conflict
        existing_payment = db.query(Payment).filter(
            Payment.idempotency_key == idempotency_key
        ).first()

        return {
            "payment_id": existing_payment.id,
            "status": existing_payment.payment_status
        }

    except Exception as e:
        db.rollback()
        logger.error(f"Payment initiation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ✅ WEBHOOK HANDLER
def webhook_handler(db: Session, payload: dict):
    try:
        logger.info(f"Webhook received: {payload}")

        # 🔐 Validate secret FIRST
        if payload.get("secret") != SECRET:
            logger.error("Invalid webhook secret")
            raise HTTPException(status_code=403, detail="Invalid webhook")

        payment_id = payload.get("payment_id")
        status = payload.get("status")

        payment = db.query(Payment).filter(Payment.id == payment_id).first()
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")

        order = db.query(Order).filter(Order.id == payment.order_id).first()

        # ✅ Update payment
        payment.payment_status = status

        # ✅ Update order
        if status == "SUCCESS":
            if order.status != "PAID":
                logger.info(f"Payment SUCCESS for order {order.id}")

                order.status = "PAID"

                # Reduce stock ONLY once
                order_items = db.query(OrderItem).filter(
                    OrderItem.order_id == order.id
                ).all()

                for item in order_items:
                    product = db.query(Product).filter(
                        Product.id == item.product_id
                    ).first()

                    if product:
                        product.stock_quantity -= item.quantity

        elif status == "FAILED":
            logger.error(f"Payment FAILED for order {order.id}")
            order.status = "FAILED"

        db.commit()

    except Exception as e:
        db.rollback()
        logger.error(f"Webhook error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))