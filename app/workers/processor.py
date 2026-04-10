import asyncio
import random
import httpx

from faststream import FastStream
from faststream.rabbit import RabbitBroker, RabbitQueue, RabbitExchange

from app.models.database import SessionLocal
from app.repository.database_repo import PaymentRepo
from app.core.broker import broker, payment_queue

app = FastStream(broker)

async def send_webhook_with_retries(url:str, data:dict, retries:int=3):
    async with httpx.AsyncClient() as client:
        for i in range(retries):
            try:
                response = await client.post(url, json=data, timeout=5.0)
                if response.status_code == 200:
                    return True
            except Exception:
                await asyncio.sleep(2 ** i)
        return False

@broker.subscriber(payment_queue)
async def process_payment(payload: dict):
    print(f"DEBUG: Received message: {payload}")
    payment_id = payload["payment_id"]
    webhook_url = payload["webhook_url"]

    await asyncio.sleep(random.uniform(2, 5))

    is_success = random.random() < 0.9
    new_status = "succeeded" if is_success else "failed"

    async with SessionLocal() as session:
        repo = PaymentRepo(session)
        await repo.update_status(payment_id, new_status)
        await session.commit()

    webhook_data = {"payment_id": payment_id, "status": new_status}
    await send_webhook_with_retries(webhook_url, webhook_data)

async def main():
    await app.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
