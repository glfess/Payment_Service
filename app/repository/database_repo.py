from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from uuid import UUID

from app.models.payment import Payment
from app.models.outbox import OutboxEvent

class PaymentRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, payment_id: UUID) -> Payment | None:
        query = select(Payment).where(Payment.id == payment_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_idempotency_key(self, idempotency_key: str) -> Payment | None:
        result = await self.session.execute(select(Payment).where(Payment.idempotency_key == idempotency_key))
        return result.scalar_one_or_none()

    async def update_status(self, payment_id: str, new_status: str):
        query = update(Payment).where(Payment.id == payment_id).values(status=new_status)
        await self.session.execute(query)

    async def save_all(self, *objects):
        self.session.add_all(objects)