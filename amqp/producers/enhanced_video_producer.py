from pika.adapters.blocking_connection import BlockingChannel
from models import EnhancedVideoResponse

def enhanced_video_producer(producerCh: BlockingChannel, enhanced_video_response: EnhancedVideoResponse):

    result = producerCh.queue_declare(queue="enhanced.video", durable=True)
    queue = result.method.queue

    body = enhanced_video_response.dumps()
    producerCh.basic_publish(exchange='', routing_key=queue, body=body)
    
    print("message sent", enhanced_video_response)