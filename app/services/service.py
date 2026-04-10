from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime
from uuid import UUID

from app.schemas.schemas import PaymentCreateRequest
from app.utils.enums import PaymentStatus
from app.models.payment import Payment
from app.models.outbox import OutboxEvent
from app.repository.database_repo import PaymentRepo

class PaymentService:
    @staticmethod
    async def create_payment(db: AsyncSession, payload: PaymentCreateRequest, idempotency_key: str):
        repo = PaymentRepo(db)

        existing = await repo.get_by_idempotency_key(idempotency_key)
        if existing:
            return existing

        payment = Payment(
            amount=payload.amount,
            currency=payload.currency,
            description=payload.description,
            meta_data=payload.meta_data,
            webhook_url=str(payload.webhook_url),
            idempotency_key=idempotency_key,
            status=PaymentStatus.pending,
        )

        db.add(payment)
        await db.flush()

        outbox_event = OutboxEvent(
            event_type="payment.new",
            payload={
                "payment_id": str(payment.id),
                "amount": str(payment.amount),
                "currency": payment.currency.value,
                "webhook_url": str(payment.webhook_url),
            },
            processed=False
        )
        db.add(outbox_event)

        await db.commit()
        await db.refresh(payment)

        return payment

    @staticmethod
    async def get_payment(db: AsyncSession, payment_id: UUID) -> Payment:
        repo = PaymentRepo(db)
        payment = await repo.get_by_id(payment_id)

        if not payment:
            raise ValueError(f"Payment with id {payment_id} does not exist")

        return payment