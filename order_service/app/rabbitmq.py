import aio_pika
import os

RABBITMQ_URL = os.getenv("RABBITMQ_URL")


async def get_rabbitmq_connection():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    return connection


async def send_order_event(event_type: str, order_data: dict):
    connection = await get_rabbitmq_connection()
    async with connection:
        channel = await connection.channel()
        exchange = await channel.declare_exchange(
            "order_events", aio_pika.ExchangeType.TOPIC
        )

        # Publica uma mensagem no RabbitMQ
        await exchange.publish(
            aio_pika.Message(body=str(order_data).encode()),
            routing_key=f"order.{event_type}",
        )
