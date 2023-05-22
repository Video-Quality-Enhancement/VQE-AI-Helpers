import time
from models import VideoEnhanceRequest
from models import EnhancedVideoResponse
from dotenv import load_dotenv
from consumers import video_enhance_consumer_720p
from producers import enhanced_video_producer

def enhance_video(video_enhance_request: VideoEnhanceRequest):
    print(video_enhance_request)
    time.sleep(2)
    enhanced_video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    status = "success"
    statusMessage = "Video enhanced successfully"
    enhanced_video_response = EnhancedVideoResponse(video_enhance_request, enhanced_video_url, status, statusMessage)
    enhanced_video_producer(enhanced_video_response)

def main():
    load_dotenv() # TODO: move this to a proper position
    video_enhance_consumer_720p(enhance_video)

if __name__ == '__main__':
    main()