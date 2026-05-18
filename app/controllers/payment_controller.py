from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models import PaymentEvent

from app.services.signature_service import verify_signature


async def process_payment_webhook(request, signature, db: Session):

    if not signature:

        raise HTTPException(status_code=403, detail="Missing signature")

    raw_body = await request.body()

    valid_signature = verify_signature(raw_body, signature)

    if not valid_signature:

        raise HTTPException(status_code=403, detail="Invalid signature")

    try:
        payload = await request.json()

    except Exception:

        raise HTTPException(status_code=400, detail="Invalid JSON")

    try:

        event_id = payload["id"]

        event_type = payload["event"]

        payment_id = payload["payload"]["payment"]["entity"]["id"]

    except KeyError:

        raise HTTPException(status_code=422, detail="Invalid payload structure")

    existing_event = (
        db.query(PaymentEvent).filter(PaymentEvent.event_id == event_id).first()
    )

    if existing_event:

        return {"message": "Duplicate event ignored"}

    new_event = PaymentEvent(
        event_id=event_id, payment_id=payment_id, event_type=event_type, payload=payload
    )

    db.add(new_event)

    db.commit()

    return {"message": "Webhook processed successfully"}


def fetch_payment_events(payment_id, db: Session):

    events = (
        db.query(PaymentEvent)
        .filter(PaymentEvent.payment_id == payment_id)
        .order_by(PaymentEvent.received_at.asc())
        .all()
    )

    response = []

    for event in events:

        response.append(
            {"event_type": event.event_type, "received_at": event.received_at}
        )

    return response
