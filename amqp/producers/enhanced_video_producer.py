import pika, os
from dotenv import load_dotenv
from models import EnhancedVideoResponse

def enhanced_video_producer(enhanced_video_response: EnhancedVideoResponse):

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv("AMQP_URL")))
    channel = connection.channel()

    result = channel.queue_declare(queue="enhanced.video", durable=True)
    queue = result.method.queue

    body = enhanced_video_response.dumps()
    channel.basic_publish(exchange='', routing_key=queue, body=body)
    
    print("message sent", enhanced_video_response)
    connection.close()