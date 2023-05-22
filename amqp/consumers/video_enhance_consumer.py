import pika, os, sys
from dotenv import load_dotenv
from models import VideoEnhanceRequest


def consumer(queue_name: str, routing_key: str, enhance_video: callable):

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv("AMQP_URL")))
    channel = connection.channel()

    exchange = "video.enhance"
    channel.exchange_declare(exchange=exchange, exchange_type="direct", durable=True)

    result = channel.queue_declare(queue=queue_name, durable=True)

    channel.queue_bind(exchange=exchange, queue=result.method.queue, routing_key=routing_key)

    channel.basic_qos(prefetch_count=0) # for our case 0 is best, as we never know which video is small and which is big

    def callback(ch, method, properties, body):
        print(body)
        video_enhance_request = VideoEnhanceRequest.loads(body)
        enhance_video(video_enhance_request)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    channel.basic_consume(queue=result.method.queue, on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    finally:
        connection.close()

def video_enhance_consumer_720p(enhance_video: callable):
    consumer("720p_queue", "720p", enhance_video)

def video_enhance_consumer_480p(enhance_video: callable):
    consumer("480p_queue", "480p", enhance_video)

def video_enhance_consumer_360p(enhance_video: callable):
    consumer("360p_queue", "360p", enhance_video)

def video_enhance_consumer_240p(enhance_video: callable):
    consumer("240p_queue", "240p", enhance_video)

def video_enhance_consumer_144p(enhance_video: callable):
    consumer("144p_queue", "144p", enhance_video)