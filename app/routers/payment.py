from fastapi import APIRouter, Depends, HTTPException, Header, status, BackgroundTasks

from sqlalchemy.ext.asyncio import AsyncSession

from faststream.rabbit import RabbitBroker

from uuid import UUID

from app.models.database import get_db
from app.schemas.schemas import PaymentResponse, PaymentCreateRequest
from app.deps.auth import get_api_key
from app.core.broker import get_broker
from app.services.service import PaymentService
from app.outbox.relay import relay_outbox_messages

router = APIRouter(prefix="/api/v1/payments", tags=["payments"], dependencies=[Depends(get_api_key)])

@router.post("",
             response_model=PaymentResponse,
             status_code=status.HTTP_202_ACCEPTED,
             summary="Create Payment",
             responses={
                 400: {"description": "Invalid request data"},
                 404: {"description": "One or more items not found"},
                 500: {"description": "Server error"},
             },
)
async def create_payment(payload: PaymentCreateRequest, background_tasks: BackgroundTasks,
                         idempotency_key: str = Header(..., alias="idempotency-key"),
                         db: AsyncSession = Depends(get_db),
                         broker: RabbitBroker = Depends(get_broker)):
    payment = await PaymentService.create_payment(db, payload,  idempotency_key)

    background_tasks.add_task(relay_outbox_messages, broker)

    return PaymentResponse.model_validate(payment)

@router.get("/{payment_id}",
            response_model=PaymentResponse)
async def get_payment(payment_id: UUID, db: AsyncSession = Depends(get_db)):

    try:
        payment = await PaymentService.get_payment(db, payment_id)
        return PaymentResponse.model_validate(payment)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)