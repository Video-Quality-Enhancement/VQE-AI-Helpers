import pika
import os
from dotenv import load_dotenv

load_dotenv()
# parameters = pika.ConnectionParameters('localhost')
parameters = pika.URLParameters(os.getenv('AMQP_URL'))
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='hello', auto_delete=True)

channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()