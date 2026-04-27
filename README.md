# 🛒 Payment & Order Processing Service

This project is a backend microservice for an Amazon-like e-commerce platform built using **FastAPI** and **PostgreSQL**.

It handles:

* Order creation
* Payment initiation
* Webhook handling
* Order status updates
* Idempotent payment processing

---

# 🚀 Tech Stack

* **Backend**: FastAPI
* **Database**: PostgreSQL
* **ORM**: SQLAlchemy
* **Validation**: Pydantic
* **Server**: Uvicorn
* **Version Control**: Git + GitHub

---

# 📂 Project Structure

```
app/
 ├── routers/        # API routes
 ├── services/       # Business logic
 ├── models/         # Database models
 ├── schemas/        # Pydantic schemas
 ├── database/       # DB connection
 ├── utils/          # Logger & helpers
 └── main.py         # Entry point
```

---

# ⚙️ Setup Instructions

## 1. Clone the repo

```
git clone https://github.com/srimathia1996/app.git
cd app
```

## 2. Create virtual environment

```
python -m venv venv
venv\Scripts\activate   # Windows
```

## 3. Install dependencies

```
pip install -r requirements.txt
```

## 4. Configure environment variables

Create a `.env` file:

```
DATABASE_URL=postgresql://username:password@localhost:5432/payment_db
WEBHOOK_SECRET=mysecret
```

---

## 5. Run the server

```
uvicorn app.main:app --reload
```

---

# 📘 API Endpoints

## 🟢 Create Order

```
POST /orders
```

## 🟢 Get Order

```
GET /orders/{order_id}
```

## 🟢 Initiate Payment

```
POST /payments/initiate
```

## 🟢 Payment Webhook

```
POST /payments/webhook
```

---

# 💳 Payment Flow

1. User creates order → status = `PENDING`
2. Payment initiated → payment record created
3. Webhook received:

   * SUCCESS → order = `PAID`
   * FAILED → order = `FAILED`
4. Stock updated only on success

---

# 🔐 Features Implemented

✅ Idempotency (no duplicate payments)
✅ Webhook handling
✅ Transaction handling
✅ Stock validation
✅ Logging
✅ Error handling

---

# ⚠️ Edge Cases Handled

* Duplicate webhook
* Payment retry
* Invalid order
* Stock issues
* Wrong webhook secret

---

# 🧪 Testing

Use:

* Swagger UI → http://127.0.0.1:8000/docs
* Postman collection (included)

---

# 📌 Future Improvements

* Stripe/Razorpay integration
* Authentication (JWT)
* Order cancellation
* Unit test coverage

