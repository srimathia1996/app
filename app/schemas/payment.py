from pydantic import BaseModel

class PaymentRequest(BaseModel):
    order_id: str
    idempotency_key: str



class PaymentWebhook(BaseModel):
    payment_id: str
    status: str
    secret:str