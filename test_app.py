from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_order():
    response = client.post("/orders", json={
        "user_id": "1",
        "items": [
            {"product_id": "1", "quantity": 1}
        ]
    })

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "PENDING"
    assert "id" in data


def test_initiate_payment():
    # First create order
    order = client.post("/orders", json={
        "user_id": "1",
        "items": [{"product_id": "1", "quantity": 1}]
    }).json()

    response = client.post("/payments/initiate", json={
        "order_id": order["id"],
        "idempotency_key": "test_key_1"
    })

    assert response.status_code == 200
    data = response.json()
    assert "payment_id" in data


def test_payment_success():
    # Create order
    order = client.post("/orders", json={
        "user_id": "1",
        "items": [{"product_id": "1", "quantity": 1}]
    }).json()

    # Initiate payment
    payment = client.post("/payments/initiate", json={
        "order_id": order["id"],
        "idempotency_key": "test_key_2"
    }).json()

    # Send webhook
    client.post("/payments/webhook", json={
        "payment_id": payment["payment_id"],
        "status": "SUCCESS",
        "secret": "mysecret"
    })

    # Check order status
    updated = client.get(f"/orders/{order['id']}").json()
    assert updated["status"] == "PAID"


def test_payment_failure():
    # Create order
    order = client.post("/orders", json={
        "user_id": "1",
        "items": [{"product_id": "1", "quantity": 1}]
    }).json()

    # Initiate payment
    payment = client.post("/payments/initiate", json={
        "order_id": order["id"],
        "idempotency_key": "test_key_3"
    }).json()

    # Send failed webhook
    client.post("/payments/webhook", json={
        "payment_id": payment["payment_id"],
        "status": "FAILED",
        "secret": "mysecret"
    })

    # Check order status
    updated = client.get(f"/orders/{order['id']}").json()
    assert updated["status"] == "FAILED"