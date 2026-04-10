from faststream.rabbit import RabbitBroker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from app.core.broker import payment_queue
from app.models.database import SessionLocal
from app.repository.outbox_repo import OutboxRepository

async def relay_outbox_messages(broker: RabbitBroker):
    print("relaying outbox messages")
    async with SessionLocal() as db:
        outbox_repo = OutboxRepository(db)
        events = await outbox_repo.get_unprocessed()

        print("found {events} events".format(events=len(events)))

        for event in events:
            try:
                await broker.publish(event.payload, queue=payment_queue)
                await outbox_repo.mark_as_processed(event.id)
                print("marked {event} as processed".format(event=event.id))
            except Exception as e:
                print(e)
                continue

        await db.commit()
        print("task finished")
