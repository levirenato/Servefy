import pika
import os
import time

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
params = pika.URLParameters(RABBITMQ_URL)


# Função para conectar ao RabbitMQ
def connect_to_rabbitmq():
    max_retries = 5
    retry_delay = 5
    for attempt in range(max_retries):
        try:
            connection = pika.BlockingConnection(params)
            channel = connection.channel()
            channel.exchange_declare(exchange="service_exchange", exchange_type="topic")
            print(f"Conexão com RabbitMQ estabelecida na tentativa {attempt + 1}")
            return connection, channel
        except pika.exceptions.AMQPConnectionError as e:
            print(
                f"Tentativa {attempt + 1} de {max_retries}: Conexão com RabbitMQ falhou, tentando novamente em {retry_delay} segundos... Detalhes do erro: {e}"
            )
            time.sleep(retry_delay)
    raise Exception("Não foi possível se conectar ao RabbitMQ após várias tentativas.")


# Variáveis globais para conexão e canal
connection, channel = connect_to_rabbitmq()


def publish_message(routing_key, message):
    global connection, channel
    try:
        if channel.is_closed:
            print("O canal está fechado, tentando reconectar...")
            connection, channel = connect_to_rabbitmq()

        channel.basic_publish(
            exchange="service_exchange", routing_key=routing_key, body=message
        )
    except pika.exceptions.StreamLostError as e:
        print(
            f"Conexão com RabbitMQ perdida, tentando reconectar... Detalhes do erro: {e}"
        )
        connection, channel = connect_to_rabbitmq()
        channel.basic_publish(
            exchange="service_exchange", routing_key=routing_key, body=message
        )
    except pika.exceptions.ChannelClosedByBroker as e:
        print(
            f"Canal fechado pelo broker, tentando reconectar... Detalhes do erro: {e}"
        )
        connection, channel = connect_to_rabbitmq()
        channel.basic_publish(
            exchange="service_exchange", routing_key=routing_key, body=message
        )
    except pika.exceptions.ConnectionClosed as e:
        print(
            f"Conexão com RabbitMQ fechada, tentando reconectar... Detalhes do erro: {e}"
        )
        connection, channel = connect_to_rabbitmq()
        channel.basic_publish(
            exchange="service_exchange", routing_key=routing_key, body=message
        )
