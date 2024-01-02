import json
import pika
import requests

# RabbitMQ connection parameters
rabbitmq_host = "localhost"
rabbitmq_port = 5672
rabbitmq_queue = "data_receiver_queue"
login = "login"
password = "pass"
credentials = pika.PlainCredentials(login, password)
# Binance API endpoint
binance_api_url = "https://api.binance.com/api/v3/klines"

# RabbitMQ connection
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=rabbitmq_host, port=rabbitmq_port, credentials=credentials
    )
)
channel = connection.channel()
channel.queue_declare(queue=rabbitmq_queue)


def send_to_another_queue(response_json, time_period, suffix_key):
    # RabbitMQ connection
    another_connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=rabbitmq_host, port=rabbitmq_port, credentials=credentials
        )
    )
    another_channel = another_connection.channel()
    another_channel.queue_declare(queue="data_process_queue")

    # Convert data to a string representation (e.g., JSON)
    # message = str(data)

    message = {}
    message["key"] = suffix_key
    message["period"] = time_period
    message["value"] = response_json
    # print(f"message {message}")
    # Send the message to the queue
    another_channel.basic_publish(
        exchange="",
        routing_key="data_process_queue",
        body=json.dumps(message).encode("utf-8"),
    )

    # Close the connection
    another_connection.close()


# RabbitMQ message consumer
def process_message(ch, method, properties, msg):
    try:
        # Decode the message from RabbitMQ
        msg = json.loads(msg.decode())
        # print(f"msg {msg}")
        # print(f"msg {type(msg)}")
        get_klines_url = "https://api.binance.com/api/v3/klines"
        start_time, end_time = msg["range"].split(":", 1)
        params = {
            f"symbol": msg["symbol"],
            "startTime": start_time,
            "endTime": end_time,
            "interval": msg["period"],
            "limit": 1000,
        }

        # Make a request to the Binance API
        response = requests.get(get_klines_url, params=params)

        # Process the response
        if response.status_code == 200:
            # Do something with the response data
            data = response.json()
            send_to_another_queue(data, msg["period"], msg["range"])
            # print(data)

        # Acknowledge the message
        channel.basic_ack(delivery_tag=method.delivery_tag)
        channel.basic_qos(prefetch_count=10)  # Set prefetch count to 10
    except Exception as e:
        print(f"error {e}")
        print(f"error str>  {msg}")
        channel.basic_reject(delivery_tag=method.delivery_tag, requeue=False)


# Set the consumer callback function
channel.basic_consume(queue=rabbitmq_queue, on_message_callback=process_message)

# Start consuming messages from RabbitMQ
channel.start_consuming()
