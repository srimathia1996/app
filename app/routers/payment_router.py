from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.payment import PaymentRequest, PaymentWebhook
from app.services.payment_service import initiate_payment, webhook_handler

router = APIRouter()

# ✅ Initiate Payment
@router.post("/payments/initiate")
def initiate(request: PaymentRequest, db: Session = Depends(get_db)):
    return initiate_payment(db, request.order_id, request.idempotency_key)


# ✅ Webhook
@router.post("/payments/webhook")
def webhook(payload: PaymentWebhook, db: Session = Depends(get_db)):
    webhook_handler(db, payload.dict())
    return {"message": "Webhook processed"}