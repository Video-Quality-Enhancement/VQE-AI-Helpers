import functools
import threading
import time
import pika
from pika.exchange_type import ExchangeType
import os
from dotenv import load_dotenv


def ack_message(ch, delivery_tag):
    """Note that `ch` must be the same pika channel instance via which
    the message being ACKed was retrieved (AMQP protocol constraint).
    """
    if ch.is_open:
        ch.basic_ack(delivery_tag)
        print("acknowledging message {}".format(delivery_tag))
    else:
        # Channel is already closed, so we can't ACK this message;
        # log and/or do something that makes sense for your app in this case.
        pass


def do_work(ch, delivery_tag, body):
    thread_id = threading.get_ident()
    print('Thread id: %s Delivery tag: %s Message body: %s', thread_id, delivery_tag, body)
    for i in range(120):
        print("working on ({})".format(i))
        time.sleep(1)
    cb = functools.partial(ack_message, ch, delivery_tag)
    ch.connection.add_callback_threadsafe(cb)


def on_message_callback(ch, method, properties, body):
    delivery_tag = method.delivery_tag
    t = threading.Thread(target=do_work, args=(ch, delivery_tag, body), daemon=True)
    t.start()


load_dotenv()
# Note: sending a short heartbeat to prove that heartbeats are still
# sent even though the worker simulates long-running work
# parameters = pika.ConnectionParameters('localhost')
parameters = pika.URLParameters(os.getenv('AMQP_URL'))
connection = pika.BlockingConnection(parameters)

channel = connection.channel()
channel.queue_declare(queue="hello", auto_delete=True)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_message_callback=on_message_callback, queue='hello')

try:
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
finally:
    connection.close()