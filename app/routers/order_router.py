from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.order import OrderCreate
from app.services.order_service import create_order
from app.models.models import Order

router = APIRouter()


# ✅ CREATE ORDER
@router.post("/orders")
def create_new_order(request: OrderCreate, db: Session = Depends(get_db)):
    return create_order(db, request.user_id, request.items)


# ✅ GET ORDER BY ID
@router.get("/orders/{order_id}")
def get_order(order_id: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return {
        "id": order.id,
        "user_id": order.user_id,
        "total_amount": order.total_amount,
        "tax_amount": order.tax_amount,
        "shipping_amount": order.shipping_amount,
        "status": order.status
    }


# ✅ CANCEL ORDER
@router.post("/orders/{order_id}/cancel")
def cancel_order(order_id: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status != "PENDING":
        raise HTTPException(
            status_code=400,
            detail="Only pending orders can be cancelled"
        )

    order.status = "CANCELLED"
    db.commit()

    return {"message": "Order cancelled successfully"}