from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.outbox import OutboxEvent

class OutboxRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_unprocessed(self, limit: int = 10):
        query = (
            select(OutboxEvent)
            .where(OutboxEvent.processed == False)
            .limit(limit)
            .with_for_update(skip_locked=True)
        )
        results = await self.session.execute(query)
        return results.scalars().all()

    async def mark_as_processed(self, event_id):
        query = (
            update(OutboxEvent)
            .where(OutboxEvent.id == event_id)
            .values(processed=True)
        )

        await self.session.execute(query)
