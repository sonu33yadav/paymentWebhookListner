from fastapi import FastAPI

from app.database import Base
from app.database import engine

from app.api.payment_routes import router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router)


@app.get("/")
def home():

    return {"message": "Payment Webhook API Running"}
