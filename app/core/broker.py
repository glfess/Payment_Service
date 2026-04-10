import os
from faststream.rabbit import RabbitBroker, RabbitQueue
from app.core.config import settings

payment_queue = RabbitQueue(
    "payments.new",
    durable=True,
    routing_key="payments.new",
    arguments={
        "x-dead-letter-exchange": "payments.dlx",
        "x-dead-letter-routing-key": "payments.failed"
    }
)

broker = RabbitBroker(settings.rabbitmq_url)

def get_broker():
    return broker