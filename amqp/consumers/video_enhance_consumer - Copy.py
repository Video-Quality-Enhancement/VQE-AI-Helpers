import os, sys
from models import VideoEnhanceRequest
from producers import enhanced_video_producer
from config import AMQPconnection


def video_enhance_consumer(queue_name: str, routing_key: str, enhance_video: callable):

    connection = AMQPconnection()
    consumerCh = connection.create_channel()
    producerCh = connection.create_channel()

    exchange = "video.enhance"
    consumerCh.exchange_declare(exchange=exchange, exchange_type="direct", durable=True)

    result = consumerCh.queue_declare(queue=queue_name, durable=True)

    consumerCh.queue_bind(exchange=exchange, queue=result.method.queue, routing_key=routing_key)

    consumerCh.basic_qos(prefetch_count=1) # 0 is no limit, 1

    def callback(ch, method, properties, body):
        video_enhance_request = VideoEnhanceRequest.loads(body)
        try:

            enhanced_video_response = enhance_video(video_enhance_request)
            enhanced_video_producer(producerCh, enhanced_video_response)

        except Exception as e:
            print(f"Exception: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)
    
    consumerCh.basic_consume(queue=result.method.queue, on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    
    try:
        consumerCh.start_consuming()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    finally:
        connection.close()