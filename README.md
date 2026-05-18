# Payment Webhook System

A minimal webhook listener system built using FastAPI and MySQL for handling mocked payment status updates from providers like Razorpay or PayPal.

---

# Features

- Receive payment webhook events
- Validate webhook signature using HMAC SHA256
- Store events in MySQL
- Prevent duplicate event processing
- Fetch payment event history
- Alembic database migrations
- Swagger API documentation

---

# Tech Stack

- FastAPI
- MySQL
- SQLAlchemy
- Alembic
- PyMySQL

---

# Project Structure

```bash
payment_webhook_system/
│
├── alembic/
│   └── versions/
│
├── app/
│   ├── api/
│   │   └── payment_routes.py
│   │
│   ├── controllers/
│   │   └── payment_controller.py
│   │
│   ├── services/
│   │   └── signature_service.py
│   │
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   └── main.py
│
├── mock_payloads/
│   ├── payment_authorized.json
│   ├── payment_captured.json
│   └── payment_failed.json
│
├── requirements.txt
├── alembic.ini
├── README.md
└── DOCS.md
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone YOUR_GITHUB_REPO_URL
```

```bash
cd payment_webhook_system
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# MySQL Database Setup

Login to MySQL:

```bash
mysql -u root -p
```

Create database:

```sql
CREATE DATABASE payment_webhook;
```

---

# Environment Variables

Create `.env` file in root directory:

```env
DATABASE_URL=mysql+pymysql://root:root%401234@localhost:3306/payment_webhook

WEBHOOK_SECRET=test_secret
```

---

# Database Migration

## Create Migration

```bash
alembic revision --autogenerate -m "create payment events table"
```

## Run Migration

```bash
alembic upgrade head
```

---

# Run Application

```bash
uvicorn app.main:app --reload
```

Server will start at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# API Endpoints

## 1. Receive Payment Webhook

### Endpoint

```http
POST /webhook/payments
```

### Headers

```text
X-Razorpay-Signature
```

### Request Example

```bash
curl -X POST http://127.0.0.1:8000/webhook/payments \
-H "Content-Type: application/json" \
-H "X-Razorpay-Signature: YOUR_SIGNATURE" \
-d @mock_payloads/payment_authorized.json
```

### Success Response

```json
{
  "message": "Webhook processed successfully"
}
```

---

## 2. Fetch Payment Events

### Endpoint

```http
GET /payments/{payment_id}/events
```

### Example

```bash
curl http://127.0.0.1:8000/payments/pay_014/events
```

### Response

```json
[
  {
    "event_type": "payment.authorized",
    "received_at": "2026-05-18T10:00:00"
  }
]
```

---

# Duplicate Event Handling

The system prevents duplicate webhook processing using a unique constraint on:

```text
event_id
```

---

# Signature Validation

Webhook signatures are validated using:

```python
HMAC SHA256
```

Shared secret used:

```text
test_secret
```

---

# Mock Payloads

Sample payloads are available inside:

```text
mock_payloads/
```

Files:
- payment_authorized.json
- payment_captured.json
- payment_failed.json

---

# Future Improvements

- Docker support
- Async database operations
- Unit testing
- Structured logging
- Redis queue
- Rate limiting

---