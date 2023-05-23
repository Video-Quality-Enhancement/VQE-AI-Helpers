import pika, os

class AMQPconnection:

    def __init__(self):
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv("AMQP_URL")))
        self.channels = []
    
    def create_channel(self):
        channel = self.conn.channel()
        self.channels.append(channel)
        return channel

    def close(self):
        for channel in self.channels:
            channel.close()
        self.conn.close()