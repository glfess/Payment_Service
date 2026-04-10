import uuid


from sqlalchemy import (
    Column,
    DateTime,
    Boolean,
    func,
    String,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.models.database import Base

class OutboxEvent(Base):
    __tablename__ = "outbox"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_type = Column(String, nullable=False)
    payload = Column(JSONB, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    processed = Column(Boolean, nullable=False, index=True)