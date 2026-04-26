from fastapi import FastAPI
from app.database.connection import engine
from app.database.base import Base

# 👇 VERY IMPORTANT
from app.models import models
from app.routers import order_router, payment_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

# 👇 INCLUDE ROUTERS
app.include_router(order_router.router)
app.include_router(payment_router.router)


@app.get("/")
def home():
    return {"message": "API Running"}