import hmac
import hashlib

from app.config import WEBHOOK_SECRET


def verify_signature(body: bytes, signature: str):

    generated_signature = hmac.new(
        WEBHOOK_SECRET.encode(), body, hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(generated_signature, signature)
