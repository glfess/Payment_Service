from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers.payment import router as payment_router
from app.core.broker import broker

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("connecting to broker")
    await broker.connect()
    yield
    print("disconnecting from broker")
    await broker.disconnect()

app = FastAPI(title="Payment API", lifespan=lifespan)

app.include_router(payment_router, prefix="")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)