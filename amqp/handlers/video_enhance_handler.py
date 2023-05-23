from consumers import video_enhance_consumer
from services import enhance_720p_video

def video_enhance_handler_720p():
    queue = "720p_queue"
    routing_key = "720p"
    video_enhance_consumer(queue, routing_key, enhance_720p_video)

def video_enhance_handler_480p(enhance_video: callable):
    video_enhance_consumer("480p_queue", "480p", enhance_video)

def video_enhance_handler_360p(enhance_video: callable):
    video_enhance_consumer("360p_queue", "360p", enhance_video)

def video_enhance_handler_240p(enhance_video: callable):
    video_enhance_consumer("240p_queue", "240p", enhance_video)

def video_enhance_handler_144p(enhance_video: callable):
    video_enhance_consumer("144p_queue", "144p", enhance_video)