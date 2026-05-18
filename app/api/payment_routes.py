from fastapi import APIRouter
from fastapi import Request
from fastapi import Header
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import get_db

from app.controllers.payment_controller import (
    process_payment_webhook,
    fetch_payment_events,
)

router = APIRouter()


@router.post("/webhook/payments")
async def payment_webhook(
    request: Request,
    x_razorpay_signature: str = Header(None),
    db: Session = Depends(get_db),
):

    return await process_payment_webhook(request, x_razorpay_signature, db)


@router.get("/payments/{payment_id}/events")
def get_payment_events(payment_id: str, db: Session = Depends(get_db)):

    return fetch_payment_events(payment_id, db)
