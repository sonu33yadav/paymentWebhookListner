from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import JSON

from datetime import datetime

from app.database import Base


class PaymentEvent(Base):

    __tablename__ = "payment_events"

    id = Column(Integer, primary_key=True, index=True)

    event_id = Column(String(255), unique=True, nullable=False)

    payment_id = Column(String(255), index=True)

    event_type = Column(String(255))

    payload = Column(JSON)

    received_at = Column(DateTime, default=datetime.utcnow)
